#!/usr/bin/env python3
"""Animate the last game turns before a zoo death, from verified replays.

  python3 scripts/animate_death.py CASE --turns 1000 --source-root SRC

CASE is a death dossier exported from a borg-zoo run: a directory, a case ID
or ID prefix (D-02cc...), or an alias. --source-root is optional: by default
the source is the cemetery cache's checkout of the dossier's commit, the one
the case's ./build.sh makes, and it is built on first use exactly as
./build.sh does. Either way the build must have the dossier's source hash.

1. The game is rerun once from birth, the way the zoo ran it (the zoo path of
   scripts/native/rerun-death.py). Its keys.log must equal the dossier's
   recorded key stream, otherwise nothing is drawn.
2. Up to --frames key positions are chosen evenly, one per distinct game turn,
   among the keys played in the last --turns game turns. The death is the
   final frame. Game turns are the unit the dossier reports: at normal speed
   one player turn is 10 game turns.
3. Each frame is a separate rerun that stops after that many keys and dumps the
   terminal (borgh -keys N -screen). Its keys.log must be exactly that prefix
   of the verified stream, otherwise the frame is dropped and the reason is
   recorded.
4. The GIF shows each screen with the game messages up to that key, beside
   the turn, depth, HP and level from the state log.

Output (default CASE/media/): last-<X>-turns.gif and last-<X>-turns.json, the
receipt with every frame's key position, turn and hashes, and every dropped
frame. The dossier's README links them after `scripts/register_deaths.py`.
A replay and its original are the same life, not another sample.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from extract_scenarios import states  # noqa: E402
from capture_episode_media import screen, sample  # noqa: E402


def rerun_module():
    spec = importlib.util.spec_from_file_location('rerun_death', ROOT / 'scripts/native/rerun-death.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_case(query):
    path = Path(query)
    if path.is_dir():
        return path.resolve()
    deaths = ROOT / 'deaths'
    matches = sorted(d for d in deaths.glob(f'{query}*') if d.is_dir())
    if len(matches) == 1:
        return matches[0].resolve()
    from death_ids import resolve
    try:
        return Path(resolve(ROOT, query)).resolve()
    except ValueError:
        pass
    raise SystemExit(f'animate_death: no single dossier matches {query!r}'
                     + (f' ({len(matches)} match)' if matches else ''))


def source_checkout(commit, cache=None):
    """The cache checkout of COMMIT that a case's ./build.sh uses, built if needed."""
    import case_replay
    cache = Path(cache).resolve() if cache else case_replay.default_cache()
    case_replay.original_build(cache, {'program': 'borg-reborn-rs', 'source': commit})
    return cache / 'sources' / 'borg-reborn-rs' / commit


def messages(path):
    """[(key index, turn, text, is a Borg note)] from a borgh messages.log.
    A line tagged with key index i was written while key i + 1 was played, so
    a frame stopped after N keys shows the lines tagged below N."""
    out = []
    if path.exists():
        for line in path.read_text(errors='replace').splitlines():
            parts = line.split(' ', 3)
            if len(parts) == 4 and parts[0].isdigit():
                note = parts[3].startswith('#')
                out.append((int(parts[0]), parts[1], parts[3][1:].strip() if note else parts[3], note))
    return out


def select(rows, death_turn, turns, frames):
    """Key positions to draw: the last TURNS game turns, one per distinct turn."""
    window = [r for r in rows if r['turn'] >= death_turn - turns]
    return sample(window, max(1, frames - 1)) if window else []


def render(frames, target, title, notes):
    from PIL import Image, ImageDraw, ImageFont
    font_path = Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
    font = ImageFont.truetype(str(font_path), 14) if font_path.exists() else ImageFont.load_default(size=14)
    images = []
    for frame in frames:
        canvas = Image.new('RGB', (1260, 580), '#11151c')
        draw = ImageDraw.Draw(canvas)
        state = frame.get('state') or {}
        draw.text((16, 12), title, font=font, fill='#71d9ff')
        draw.text((16, 34), f"Turn {frame['turn']} ({frame['before_death']} before death) | key {frame['key_position']} | "
                            f"depth {state.get('depth', '?')} | HP {state.get('hp', '?')}/{state.get('max_hp', '?')} | "
                            f"{frame['phase']}", font=font, fill='#ffd787')
        for row, line in enumerate(frame['screen'].splitlines()[:26]):
            draw.text((16, 70 + row * 17), line[:80], font=font, fill='#e0e7ef')
        draw.line((690, 64, 690, 540), fill='#394757')
        shown = [m for m in notes if m[0] < frame['key_position']]
        for top, label, wanted, colour in ((70, 'GAME MESSAGES (latest last)', False, '#e0e7ef'),
                                           (306, 'BORG NOTES (latest last)', True, '#9fb3c8')):
            draw.text((706, top), label, font=font, fill='#ffd787')
            for i, (_, turn, text, _) in enumerate([m for m in shown if m[3] == wanted][-12:]):
                draw.text((706, top + 22 + i * 17), f'{turn:>6} {text}'[:76], font=font, fill=colour)
        draw.text((16, 552), 'Each frame is a rerun from birth whose keys match the original game; timing is for viewing.',
                  font=font, fill='#a8b4c3')
        images.append(canvas.convert('P', palette=Image.Palette.ADAPTIVE))
    images[0].save(target, save_all=True, append_images=images[1:],
                   duration=[700] * (len(images) - 1) + [2500], loop=0, disposal=2)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case', help='dossier directory, case ID or ID prefix')
    ap.add_argument('--turns', type=int, required=True, help='game turns before the death to animate')
    ap.add_argument('--frames', type=int, default=24, help='frames, the death included (3..60)')
    ap.add_argument('--source-root', type=Path,
                    help='borg-reborn-rs checkout at the dossier commit with build/rust built '
                         '(default: the cache checkout ./build.sh makes, built if needed)')
    ap.add_argument('--cache', type=Path, help='cemetery build cache (default as ./build.sh)')
    ap.add_argument('--out', type=Path, help='output directory (default CASE/media)')
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1)
    a = ap.parse_args(argv)
    if not 3 <= a.frames <= 60 or a.turns < 1:
        ap.error('--frames must be 3..60 and --turns at least 1')
    case = resolve_case(a.case)
    rd = rerun_module()
    p = rd.plan(case)
    rd.ROOT = (a.source_root or source_checkout(p['git_rev'], a.cache)).resolve()
    if not p['zoo']:
        raise SystemExit(f'animate_death: {case.name} is not a zoo dossier (config.txt has no zoo_profile)')
    build = rd.read_kv(rd.ROOT / 'build/rust/BUILD_ID')
    if build.get('source_sha256') != p['source_sha256']:
        raise SystemExit(f"animate_death: build/rust is source {str(build.get('source_sha256'))[:12]}, the death's is "
                         f"{str(p['source_sha256'])[:12]}: check out {p['git_rev']} and run harness/build.sh")
    record = json.loads((case / 'record.json').read_text())
    out = (a.out or case / 'media').resolve()
    name = f'last-{a.turns}-turns'
    receipt = {'schema': 'borg-cemetery/last-turns-animation@1', 'case': case.name, 'turns': a.turns,
               'seed': p['seed'], 'source_commit': p['git_rev'], 'keys_sha256': p['keys_sha256'],
               'method': 'zoo rerun from birth, stopped after N keys (-keys N -screen); each frame\'s keys '
                         'are the verified original prefix', 'frames': [], 'dropped': []}
    with tempfile.TemporaryDirectory(prefix='cemetery-animate-') as tmp:
        tmp = Path(tmp)
        full = tmp / 'full'
        rd.run_zoo(p, full, {}, 0, extra=['-screen'])
        run = full / 'run'
        if not (run / 'keys.log').exists() or sha256(run / 'keys.log') != p['keys_sha256']:
            raise SystemExit(f"animate_death: the rerun of {case.name} does not reproduce its recorded keys; "
                             'nothing drawn (see ' + str(run / 'stderr.log') + ')')
        keys = (run / 'keys.log').read_bytes().splitlines(keepends=True)
        rows = states(run / 'state.log')
        notes = messages(run / 'messages.log')
        death_turn = record['terminal'].get('turn') or rows[-1]['turn']
        chosen = [r for r in select(rows, death_turn, a.turns, a.frames) if r['line'] < len(keys)]

        def frame(row):
            where = tmp / f"key-{row['line']}"
            rd.run_zoo(p, where, {}, 0, extra=['-keys', row['line'], '-screen'])
            got = (where / 'run/keys.log').read_bytes() if (where / 'run/keys.log').exists() else b''
            if got != b''.join(keys[:row['line']]):
                return None, f"key {row['line']}: the replay's keys are not the original prefix"
            terminal = screen(where / 'run/stderr.log')
            if terminal is None:
                return None, f"key {row['line']}: no terminal dump"
            return {'key_position': row['line'], 'turn': row['turn'], 'before_death': death_turn - row['turn'],
                    'phase': 'verified replay', 'state': {k: row[k] for k in ('depth', 'hp', 'max_hp')},
                    'screen': terminal, 'keys_sha256': hashlib.sha256(got).hexdigest()}, None

        with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
            for (result, error) in pool.map(frame, chosen):
                if result:
                    receipt['frames'].append(result)
                else:
                    receipt['dropped'].append(error)
        last = screen(run / 'stderr.log')
        if last:
            receipt['frames'].append({'key_position': len(keys), 'turn': death_turn, 'before_death': 0,
                                      'phase': 'death (full verified rerun)', 'screen': last,
                                      'state': {k: rows[-1][k] for k in ('depth', 'hp', 'max_hp')} if rows else {},
                                      'keys_sha256': p['keys_sha256']})
        if not receipt['frames']:
            raise SystemExit(f"animate_death: no frame could be verified: {receipt['dropped'][:3]}")
        out.mkdir(parents=True, exist_ok=True)
        title = (f"{record.get('character', 'Borg')} | seed {p['seed']} | {record.get('raw_cause')} at turn {death_turn} "
                 f"| last {a.turns} game turns")
        render(receipt['frames'], out / f'{name}.gif', title, notes)
    receipt.update(gif=f'{name}.gif', gif_sha256=sha256(out / f'{name}.gif'),
                   status='partial' if receipt['dropped'] else 'complete')
    for f in receipt['frames']:
        f.pop('screen')
    (out / f'{name}.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'case': case.name, 'gif': str(out / f'{name}.gif'), 'frames': len(receipt['frames']),
                      'dropped': len(receipt['dropped']), 'status': receipt['status']}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
