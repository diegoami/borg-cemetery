import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_batch as runner
import extract_scenarios as scenarios
import archive_records
import compare_batches
import run_scenario
import capture_episode_media


FIXTURE = '''import hashlib, json, os, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parent
if sys.argv[1] == 'build':
    game = root / 'build/rust/game'
    game.mkdir(parents=True)
    (game / 'angband').write_bytes(b'fixture binary')
    rev = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    (game.parent / 'BUILD_ID').write_text('impl=rust\\ngit_rev=' + rev +
        '\\ninputs_dirty=no\\nsource_sha256=fixture\\nrustc=fixture\\ncc=fixture\\nbinary_sha256=' + hashlib.sha256(b'fixture binary').hexdigest() + '\\n')
else:
    toolkit = pathlib.Path(os.environ.get('BORG_CEMETERY_DIR', '/missing'))
    assert (toolkit / 'scripts/native/API_VERSION').read_text().strip() == '1'
    out, seed, race, cls, turns = sys.argv[2:7]
    out = pathlib.Path(out)
    out.mkdir()
    seed = int(seed)
    summary = dict(seed=seed + (seed == 103), loaded=False, race_idx=int(race),
        class_idx=int(cls), menu_letters=True, dead=seed != 104,
        stop_reason='turns' if seed == 104 else 'death', game_turns=50,
        death_cause='fixture monster', calendar='fixed', game_options={'cheat_live': False})
    (out / 'summary.json').write_text(json.dumps(summary))
    (out / 'process.json').write_text(json.dumps({'status': 'timeout' if seed == 102 else 'exited'}))
    (out / 'keys.log').write_text('40 1 68 0\\n')
    (out / 'state.log').write_text('10 1,1 d1/1 hp10/10 sp0/0\\n30 1,1 d1/1 hp2/10 sp0/0\\n40 1,1 d1/1 hp1/10 sp0/0\\n')
    (out / 'trace.jsonl').write_text(json.dumps({'turn': 40, 'choice': 'retreat'}) + '\\n')
    if os.environ.get('BORG_OBSERVATION_LOG'):
        pathlib.Path(os.environ['BORG_OBSERVATION_LOG']).write_text(json.dumps(
            {'turn': 10, 'inventory': [{'desc': 'a potion', 'number': 1}], 'equipment': [], 'spells': []}) + '\\n')
'''


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'fixture'
        self.source.mkdir()
        (self.source / 'harness').mkdir()
        (self.source / 'fixture.py').write_text(FIXTURE)
        for name, action in [('build', 'build'), ('run', 'run')]:
            (self.source / f'harness/{name}.sh').write_text(f'python3 fixture.py {action} "$@"\n')
        for args in [('init', '-q'), ('config', 'user.email', 'fixture@example.org'),
                     ('config', 'user.name', 'Fixture'), ('add', '.'), ('commit', '-qm', 'fixture')]:
            subprocess.run(['git', '-C', str(self.source), *args], check=True)

    def batch(self, seeds='101,102,103,104'):
        args = runner.parse_args(['--program', 'borg-reborn-rs', '--ref', 'HEAD',
                                  '--seeds', seeds, '--out', str(self.root / 'batch')])
        original = runner.command

        def local_command(argv, **kwargs):
            if 'fetch' in argv:
                argv = [str(self.source) if x.startswith('https://github.com/') else x for x in argv]
            return original(argv, **kwargs)

        with patch.object(runner, 'command', side_effect=local_command), \
                patch.dict(os.environ, {'BORG_CEMETERY_DIR': '/stale-inherited-checkout'}):
            rc = runner.run_batch(args)
        return rc, args.out

    def test_original_evidence_and_failure_categories(self):
        rc, batch = self.batch()
        self.assertEqual(rc, 1)
        expected = {101: 'death', 102: 'timeout', 103: 'identity_mismatch', 104: 'turn_cap'}
        for seed, status in expected.items():
            record = batch / 'records' / f'seed-{seed}'
            rec = runner.read_json(record / 'run.json')
            self.assertEqual(rec['seed'], seed)
            self.assertEqual(rec['status'], status)
            self.assertEqual(len(rec['source_commit']), 40)
            self.assertEqual((record / 'death-report.md').exists(), status == 'death')
            self.assertFalse((record / 'keys.log').exists())
            self.assertIn('keys.log', rec['hashes'])
            self.assertIn('observations.jsonl.gz', rec['hashes'])
            import gzip
            self.assertIn('a potion', gzip.decompress((batch / 'evidence' / record.name / 'observations.jsonl.gz').read_bytes()).decode())
            self.assertFalse((batch / 'evidence' / record.name / 'observations.jsonl').exists())

    def test_fetch_failure_keeps_seeds(self):
        args = runner.parse_args(['--program', 'borg-rs', '--ref', 'missing',
                                  '--seeds', '0,4294967295', '--out', str(self.root / 'failed')])
        with patch.object(runner, 'command', return_value=1):
            self.assertEqual(runner.run_batch(args), 1)
        manifest = runner.read_json(args.out / 'records/batch.json')
        self.assertEqual(manifest['seeds'], [0, 4294967295])
        self.assertEqual(manifest['status'], 'failed')
        self.assertTrue((args.out / 'records/seed-0/run.json').exists())

    def test_extract_sequence_merges_terminal_low_hp_into_death(self):
        _, batch = self.batch('101')
        result = scenarios.extract(batch / 'evidence/seed-101', batch / 'records/seed-101',
                                   batch / 'records/seed-101/analysis')
        self.assertEqual([e['kind'] for e in result['events']], ['death'])
        event = result['events'][0]
        self.assertEqual(event['start']['turn'], 10)
        sequence = json.loads((batch / 'records/seed-101/analysis/event-1/sequence.json').read_text())
        self.assertTrue(any(e.get('decision', {}).get('choice') == 'retreat' for e in sequence))
        self.assertEqual(event['scenario']['status'], 'missing_checkpoint')
        self.assertFalse(event['scenario']['borg_memory_restored'])
        self.assertTrue((batch / 'records/seed-101/README.md').is_file())
        self.assertTrue((batch / 'records/seed-101/analysis/README.md').is_file())
        landing = batch / 'records/seed-101/analysis/event-1/README.md'
        self.assertIn('**Seed: `101`**', landing.read_text())

    def test_archive_appends_and_never_replaces(self):
        _, batch = self.batch('101')
        remote = self.root / 'archive.git'
        subprocess.run(['git', 'init', '--bare', '-q', str(remote)], check=True)
        for launcher in (batch / 'records').rglob('*.sh'):
            launcher.chmod(0o644)  # Actions artifact downloads strip executable bits.
        original = subprocess.run

        def local_git(argv, **kwargs):
            argv = [str(remote) if x.startswith('https://github.com/') else x for x in argv]
            return original(argv, **kwargs)

        with patch.dict(os.environ, GITHUB_RUN_ID='12', GITHUB_RUN_ATTEMPT='1', GITHUB_REPOSITORY='fixture/repo'):
            with patch.object(archive_records.subprocess, 'run', side_effect=local_git):
                archive_records.archive(batch / 'records')
                os.environ['GITHUB_RUN_ATTEMPT'] = '2'
                archive_records.archive(batch / 'records')
                with self.assertRaisesRegex(RuntimeError, 'already archived'):
                    archive_records.archive(batch / 'records')
        listing = subprocess.check_output(['git', '--git-dir', str(remote), 'ls-tree', '-r', '--name-only', 'results'], text=True)
        self.assertIn('runs/12-1/batch.json', listing)
        self.assertIn('runs/12-2/batch.json', listing)
        mode = subprocess.check_output(['git', '--git-dir', str(remote), 'ls-tree', 'results',
                                        'runs/12-1/seed-101/watch.sh'], text=True)
        self.assertTrue(mode.startswith('100755 '), mode)

    def test_validation(self):
        for seeds in ['1,1', '-1', '4294967296', 'bad', '']:
            with self.subTest(seeds=seeds), self.assertRaises(SystemExit):
                runner.parse_args(['--program', 'borg-rs', '--ref', 'HEAD', '--seeds', seeds,
                                   '--out', str(self.root / 'invalid')])

    def test_legacy_summary_and_reject_loaded_game(self):
        summary = dict(seed=1, race_idx=0, class_idx=0, menu_letters=True,
                       dead=False, stop_reason='turns')
        self.assertEqual(runner.outcome(summary, {}, 0, 1, 0, 0), 'turn_cap')
        summary['loaded'] = True
        self.assertEqual(runner.outcome(summary, {}, 0, 1, 0, 0), 'identity_mismatch')

    def test_comparison_requires_matching_identity_and_shows_regressions(self):
        _, batch = self.batch('101,104')
        baseline = batch / 'records'
        candidate = self.root / 'candidate'
        import shutil
        shutil.copytree(baseline, candidate)
        for seed, status in [(101, 'turn_cap'), (104, 'death')]:
            path = candidate / f'seed-{seed}/run.json'
            rec = runner.read_json(path)
            rec['status'] = status
            runner.write_json(path, rec)
        result = compare_batches.compare(baseline, candidate)
        self.assertEqual(result['rescued'], 1)
        self.assertEqual(result['newly_killed'], 1)
        manifest = runner.read_json(candidate / 'batch.json')
        manifest['source_commit'] = 'another-source'
        runner.write_json(candidate / 'batch.json', manifest)
        with self.assertRaisesRegex(ValueError, 'source_commit'):
            compare_batches.compare(baseline, candidate)

    def test_adaptive_boundary_precedes_long_decline_and_recovery_separates_episodes(self):
        def row(turn, hp):
            return dict(turn=turn, hp=hp, max_hp=100, line=turn)
        rows = [row(10, 100), row(20, 100), row(30, 100), row(50, 60),
                row(200, 20), row(210, 80), row(220, 85), row(230, 90), row(250, 15)]
        found = scenarios.events(rows, dict(dead=True, stop_reason='death', game_turns=260))
        self.assertEqual(len(found), 2)
        self.assertEqual(found[0]['start']['turn'], 30)
        self.assertEqual(found[0]['resolution'], 'recovered_to_stable')
        self.assertEqual(found[0]['end']['turn'], 230)
        self.assertEqual(found[1]['kind'], 'death')
        self.assertEqual(found[1]['start']['turn'], 230)
        self.assertGreater(found[0]['turn'] - found[0]['start']['turn'], 30)

    def test_repeated_keys_do_not_establish_stability_and_threat_overrides_hp(self):
        rows = [dict(turn=1, hp=100, max_hp=100, line=i) for i in range(1, 5)]
        rows.append(dict(turn=50, hp=1, max_hp=100, line=5))
        self.assertEqual(scenarios.events(rows, {})[0]['start_basis'], 'no_stable_boundary_observed')
        rows = [dict(turn=t, hp=100, max_hp=100, line=t) for t in (10, 20, 30, 40)]
        decisions = [dict(value=dict(turn=1, threat=dict(p_death=0.5, worst=150)))]
        event = scenarios.events(rows, dict(dead=True, stop_reason='death', game_turns=50), decisions)[0]
        self.assertEqual(event['start_basis'], 'no_stable_boundary_observed')
        danger = scenarios.events(rows, {}, decisions)[0]
        self.assertEqual(danger['kind'], 'near_death_candidate')
        self.assertEqual(danger['trigger_reason'], 'estimated_lethal_risk')
        self.assertEqual(danger['trigger']['hp'], 100)

    def test_curates_earlier_save_and_verifies_hashes_before_trial(self):
        raw = self.root / 'raw'
        (raw / 'checkpoints').mkdir(parents=True)
        (raw / 'checkpoints/start.save').write_bytes(b'original saved engine state')
        checkpoint = dict(file='start.save', game_turn=100, keys=10, seed=7, race_idx=0, class_idx=0)
        (raw / 'checkpoints/index.jsonl').write_text(json.dumps(checkpoint) + '\n')
        identity = dict(seed=7, race_idx=0, class_idx=0, program='borg-rs')
        event = dict(start=dict(turn=130, line=15), kind='death', turn=400)
        dest = self.root / 'scenario'
        saved = scenarios.curate_save(raw, identity, event, dest)
        self.assertEqual(saved['status'], 'ready_for_restart_trials')
        self.assertEqual(saved['checkpoint_lead_turns'], 30)
        import gzip
        self.assertEqual(gzip.decompress((dest / 'start.save.gz').read_bytes()), b'original saved engine state')
        (dest / 'start.save.gz').write_bytes(b'corruption')
        result = self.root / 'trial'
        self.assertEqual(run_scenario.run_scenario(self.source, dest, result), 1)
        self.assertIn('hash mismatch', runner.read_json(result / 'trial.json')['error'])

    def test_scenario_comparison_preserves_failures_and_checks_shared_start(self):
        baseline = dict(scenario_sha256='scenario', save_sha256='save',
                        startup_contract='fresh_borg_saved_engine_rng', horizon_engine_turns=100,
                        status='death')
        candidate = dict(baseline, status='survived_horizon')
        self.assertEqual(run_scenario.compare_trials(baseline, candidate)['result'], 'rescued')
        candidate['status'] = 'timeout'
        self.assertEqual(run_scenario.compare_trials(baseline, candidate)['result'], 'inconclusive')
        candidate['save_sha256'] = 'different'
        with self.assertRaisesRegex(ValueError, 'save_sha256'):
            run_scenario.compare_trials(baseline, candidate)

    def test_screenshot_capture_rejects_divergent_replay_prefix(self):
        _, batch = self.batch('101')
        raw = batch / 'evidence/seed-101'
        identity = runner.read_json(batch / 'records/seed-101/run.json')
        event = scenarios.events(scenarios.states(raw / 'state.log'), runner.read_json(raw / 'summary.json'))[0]
        (raw / 'keys.log').write_text('999 1 0 0\n')
        media = self.root / 'media'
        result = capture_episode_media.capture(batch / 'source', raw, identity, event, media, max_frames=3)
        self.assertEqual(result['status'], 'unavailable')
        self.assertTrue(any('prefix mismatch' in error for error in result['errors']))
        self.assertFalse((media / 'episode.gif').exists())


if __name__ == '__main__':
    unittest.main()
