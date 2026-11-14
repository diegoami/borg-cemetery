#!/usr/bin/env python3
"""Capture genuine terminal screens at verified positions in the original run."""
import argparse
import os
from pathlib import Path
import tempfile
import time

from episode_inventory import description, observations
from extract_scenarios import events, jsonlines, states
from run_batch import command, digest, git, kv, read_json, write_json


def screen(stderr):
    text = stderr.read_text(errors='replace') if stderr.exists() else ''
    if '---- screen ----\n' not in text:
        return None
    text = text.rsplit('---- screen ----\n', 1)[1]
    if '\n----------------' not in text:
        return None
    return text.split('\n----------------', 1)[0]


def sample(rows, count):
    # Screens include prompts and are not synonymous with a Borg decision.
    unique = {r['turn']: r for r in rows}
    rows = list(unique.values())
    if len(rows) <= count:
        return rows
    return [rows[round(i * (len(rows) - 1) / (count - 1))] for i in range(count)]


def render_gif(frames, target, inventory, decisions, seed):
    from PIL import Image, ImageDraw, ImageFont
    font_path = Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
    font = ImageFont.truetype(str(font_path), 14) if font_path.exists() else ImageFont.load_default(size=14)
    output = []
    for frame in frames:
        canvas = Image.new('RGB', (1210, 560), '#11151c')
        draw = ImageDraw.Draw(canvas)
        turn = frame['turn']
        draw.text((16, 12), f"Seed {seed} | turn {turn} | {frame['phase']}", font=font, fill='#71d9ff')
        draw.text((16, 38), 'Actual terminal screen, monochrome; original input/state prefix verified', font=font, fill='#a8b4c3')
        for row, line in enumerate(frame['screen'].splitlines()):
            draw.text((16, 76 + row * 17), line, font=font, fill='#e0e7ef')
        known = next((o for o in reversed(inventory) if o['turn'] <= turn), None)
        decision = next((d['value'] for d in reversed(decisions) if d['value'].get('turn', turn + 1) <= turn), {})
        draw.line((705, 70, 705, 520), fill='#394757')
        draw.text((724, 76), 'BORG INVENTORY (last observed)', font=font, fill='#ffd787')
        if known:
            draw.text((724, 100), f"Observation turn {known['turn']}", font=font, fill='#a8b4c3')
            for i, item in enumerate(known['pack'][:15]):
                draw.text((724, 127 + i * 19), description(item)[:55], font=font, fill='#e0e7ef')
        else:
            draw.text((724, 108), 'Not recorded in this run', font=font, fill='#a8b4c3')
        draw.text((724, 437), f"Mode: {decision.get('mode', 'not recorded')}", font=font, fill='#71d9ff')
        choice = str(decision.get('choice', 'not recorded'))
        for i in range(2):
            draw.text((724, 461 + i * 19), choice[i * 53:(i + 1) * 53], font=font, fill='#e0e7ef')
        draw.text((16, 532), 'Screens are sampled; timing is for viewing. Inventory and thoughts may precede the screenshot.',
                  font=font, fill='#a8b4c3')
        output.append(canvas.convert('P', palette=Image.Palette.ADAPTIVE))
    if output:
        output[0].save(target, save_all=True, append_images=output[1:],
                       duration=[450] * (len(output) - 1) + [1800], loop=0, disposal=2)


def capture(source, raw, identity, event, dest, profile=None, max_frames=24, deadline=None):
    dest.mkdir(parents=True, exist_ok=False)
    receipt = dict(schema='borg-cemetery/episode-media@1', status='unavailable',
                   seed=identity.get('seed'), source_commit=identity.get('source_commit'),
                   frames=[], errors=[], independent_lives=0,
                   method='same pinned executable replayed from birth to verified key/state prefixes')
    write_json(dest / 'media.json', receipt)
    try:
        build = kv(source / 'build/rust/BUILD_ID')
        if (git(source, 'rev-parse', 'HEAD') != identity['source_commit'] or
                build['git_rev'] != identity['source_commit'] or
                digest(source / 'build/rust/game/angband') != identity['binary_sha256']):
            raise ValueError('preview source or executable does not match the original run')
        all_rows = states(raw / 'state.log')
        start = event['start']
        if not start:
            raise ValueError('no observed episode boundary')
        original_keys = (raw / 'keys.log').read_bytes().splitlines(keepends=True)
        original_states = (raw / 'state.log').read_bytes().splitlines(keepends=True)
        end = event['end'] or all_rows[-1]
        selected = sample([r for r in all_rows if start['line'] <= r['line'] <= end['line']], max_frames - 1)
        inventory = list(observations(raw))
        decisions = list(jsonlines(raw / 'trace.jsonl'))
        with tempfile.TemporaryDirectory(prefix='cemetery-preview-') as tmp:
            for i, row in enumerate(selected):
                remaining = (deadline - time.monotonic()) if deadline else 30
                if remaining <= 1:
                    receipt['errors'].append('preview time budget exhausted')
                    break
                replay = Path(tmp) / f'frame-{i}'
                env = dict(os.environ, BORG_IMPL='rust', TZ='UTC', LANG='C.UTF-8', LC_ALL='C.UTF-8',
                           RUN_TIMEOUT_SECONDS=str(min(30, int(remaining))), CHECKPOINT_EVERY='0',
                           BORG_DEATH_RECORDS_DIR=str(Path(tmp) / 'diagnostic-deaths'))
                for name in ('ANGBAND_BIN', 'BORG_PROFILE', 'BORG_OBSERVATION_LOG', 'BORG_RECORD_DIR',
                             'BORG_TOOLKIT_NATIVE', 'BORGH_DATA_ROOT', 'STALL_TIMEOUT_SECONDS', 'SAVE_ROOT'):
                    env.pop(name, None)
                if profile:
                    env['BORG_PROFILE'] = str(profile.resolve())
                rc = command(['bash', 'harness/run.sh', str(replay), str(identity['seed']),
                              str(identity['race_idx']), str(identity['class_idx']), str(identity['turns']),
                              f"menu,key-limit={row['line']}"], cwd=source, env=env,
                             log=Path(tmp) / f'frame-{i}.log', timeout=min(35, remaining))
                if rc or not (replay / 'keys.log').exists() or not (replay / 'state.log').exists():
                    receipt['errors'].append(f"frame {i}: replay failed ({rc})")
                    continue
                keys = (replay / 'keys.log').read_bytes()
                state = (replay / 'state.log').read_bytes()
                if keys != b''.join(original_keys[:row['line']]) or state != b''.join(original_states[:row['line']]):
                    receipt['errors'].append(f"frame {i}: original key/state prefix mismatch")
                    continue
                terminal = screen(replay / 'stderr.log')
                if terminal is None:
                    receipt['errors'].append(f"frame {i}: terminal dump unavailable")
                    continue
                name = f'frame-{len(receipt["frames"]):03d}.txt'
                (dest / name).write_text(terminal + '\n')
                receipt['frames'].append(dict(turn=row['turn'], key_position=row['line'],
                                               phase='verified replay', screen=terminal, file=name,
                                               keys_sha256=digest(replay / 'keys.log'),
                                               state_sha256=digest(replay / 'state.log')))
        terminal = screen(raw / 'stderr.log')
        if terminal and event['kind'] == 'death':
            (dest / 'death.txt').write_text(terminal + '\n')
            receipt['frames'].append(dict(turn=event['turn'], phase='original death',
                                           screen=terminal, file='death.txt',
                                           stderr_sha256=digest(raw / 'stderr.log')))
        if receipt['frames']:
            render_gif(receipt['frames'], dest / 'episode.gif', inventory, decisions, identity['seed'])
            receipt.update(status='partial' if receipt['errors'] else 'complete', gif='episode.gif',
                           gif_sha256=digest(dest / 'episode.gif'))
    except Exception as exc:
        receipt['errors'].append(str(exc))
    finally:
        write_json(dest / 'media.json', receipt)
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('batch', type=Path)
    p.add_argument('--max-frames', type=int, default=24)
    p.add_argument('--budget-seconds', type=int, default=300)
    a = p.parse_args()
    if not 3 <= a.max_frames <= 40 or not 1 <= a.budget_seconds <= 600:
        p.error('max-frames must be 3..40; budget-seconds must be 1..600')
    batch = a.batch.resolve()
    deadline = time.monotonic() + a.budget_seconds
    for record in sorted((batch / 'records').glob('seed-*')):
        identity = read_json(record / 'run.json')
        if identity.get('status') not in ('death', 'turn_cap', 'stopped'):
            continue
        raw = batch / 'evidence' / record.name
        terminal = read_json(raw / 'summary.json')
        if identity['status'] != 'death':
            terminal['dead'] = False
        selected = events(states(raw / 'state.log'), terminal, list(jsonlines(raw / 'trace.jsonl')))
        for number, event in enumerate(selected, 1):
            profile = batch / 'records/profile.txt'
            capture(batch / 'source', raw, identity, event, raw / 'media' / f'event-{number}',
                    profile if profile.is_file() else None, a.max_frames, deadline)


if __name__ == '__main__':
    main()
