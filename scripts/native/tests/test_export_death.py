"""Tests for tools/export-death.py on synthetic run directories.

Run: python3 -m unittest discover -s tools/tests
"""

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('export_death', HERE.parent / 'export-death.py')
ed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ed)


def make_run(base, name, dead=True, seed=101, keys='abc\n', **extra):
    run = Path(base) / name
    run.mkdir(parents=True)
    (run / 'summary.json').write_text(json.dumps({
        'seed': seed, 'race': 'Human', 'race_idx': 0, 'class': 'Warrior', 'class_idx': 0,
        'stop_reason': 'death' if dead else 'turns', 'game_turns': 12345, 'clevel': 4,
        'max_depth': 3, 'depth': 2, 'dead': dead, 'death_cause': 'a cave spider' if dead else '',
        'keys': 99, **extra}))
    (run / 'keys.log').write_text(keys)
    (run / 'messages.log').write_text('You die.\n')
    (run / 'config.txt').write_text('flags=-\nborg_txt_sha256=feed\n')
    return run


class ExportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.reg = self.base / 'deaths'
        os.environ['BORG_DEATH_RECORDS_DIR'] = str(self.reg)
        self.build = self.base / 'BUILD_ID'
        self.build.write_text('impl=c\ngit_rev=1234567\ngit_dirty=no\nbinary_sha256=beef\nsource_sha256=cafe\n')
        self.first_id = ed.death_id(ed.family_of('c', 101, 0, 0, 'cafe', 'feed'),
                                    ed.hashlib.sha256(b'abc\n').hexdigest())

    def tearDown(self):
        os.environ.pop('BORG_DEATH_RECORDS_DIR', None)
        self.tmp.cleanup()

    def test_yaml_settings_define_the_family_and_are_retained(self):
        run = make_run(self.base, 'yaml')
        user = run / 'user'
        user.mkdir()
        yaml = user / 'pborg.yaml'
        yaml.write_text('borg_reborn_core: borg-rs\n')
        digest = ed.sha256_file(yaml)
        (run / 'config.txt').write_text(f'pborg_yaml_sha256={digest}\n')
        case, status = ed.export(run, 'rust', self.build)
        self.assertEqual(status, 'exported')
        dossier = self.reg / case
        record = json.loads((dossier / 'record.json').read_text())
        self.assertEqual(record['identity']['pborg_yaml_sha256'], digest)
        self.assertEqual(record['encounter_family'], ed.family_of('rust', 101, 0, 0, 'cafe', digest))
        self.assertEqual((dossier / 'pborg.yaml').read_bytes(), yaml.read_bytes())
        yaml.write_text('borg_reborn_core: reborn\n')
        with self.assertRaisesRegex(SystemExit, 'pborg.yaml differs'):
            ed.export(run, 'rust', self.build)

    def test_alive_run_writes_nothing(self):
        run = make_run(self.base, 'alive', dead=False)
        self.assertEqual(ed.export(run, 'c', self.build), (None, 'not dead'))
        self.assertFalse(self.reg.exists() and any(self.reg.iterdir()))

    def test_synthetic_deaths_never_create_a_natural_registry(self):
        markers = [({'synthetic': True}, '', '-'),
                   ({'start_depth': 20}, '', '-'),
                   ({}, 'synthetic=1\n', '-'),
                   ({}, 'start_depth=20\n', '-'),
                   ({}, 'flags=menu,start-depth=20\n', '-'),
                   ({}, '', 'menu,start-depth=20'),
                   ({'synthetic': False}, 'synthetic=1\n', '-')]
        for index, (summary, config, flags) in enumerate(markers):
            with self.subTest(summary=summary, config=config, flags=flags):
                run = make_run(self.base, f'synthetic-{index}', **summary)
                with (run / 'config.txt').open('a') as stream:
                    stream.write(config)
                self.assertEqual(ed.export(run, 'rust', self.build, flags),
                                 (None, 'not natural: synthetic start'))
                self.assertFalse(self.reg.exists())

    def test_explicit_natural_marker_preserves_natural_export(self):
        run = make_run(self.base, 'natural', synthetic=False)
        with (run / 'config.txt').open('a') as stream:
            stream.write('synthetic=0\nstart_depth=0\n')
        self.assertEqual(ed.export(run, 'rust', self.build)[1], 'exported')

    def test_flag_variants_are_excluded_from_both_flag_sources(self):
        for index, flag in enumerate(('start-depth 20', 'start-depth', 'start_depth=20',
                                      'synthetic', 'menu, start-depth=20', 'Start-Depth=20')):
            for recorded in (False, True):
                with self.subTest(flag=flag, recorded=recorded):
                    run = make_run(self.base, f'variant-{index}-{recorded}')
                    if recorded:
                        (run / 'config.txt').write_text(f'flags={flag}\n')
                    self.assertEqual(ed.export(run, 'rust', self.build, '-' if recorded else flag),
                                     (None, 'not natural: synthetic start'))
        self.assertFalse(self.reg.exists())

    def test_malformed_option_receipts_fail_closed_without_registry_access(self):
        for index, options in enumerate(([1], [], 'true', 1, False)):
            run = make_run(self.base, f'options-{index}', game_options=options)
            self.assertEqual(ed.export(run, 'rust', self.build),
                             (None, 'not natural: malformed game_options'))
        self.assertFalse(self.reg.exists())

    def test_one_way_lineage_requires_native_boolean_pair_not_just_a_load(self):
        summary = dict(dead=True, stop_reason='death', death_cause='a cave spider', loaded=True)
        for options in ({}, {'birth_force_descend': True},
                        {'birth_force_descend': 'true', 'birth_no_recall': 'true'},
                        {'birth_force_descend': 1, 'birth_no_recall': 1}):
            self.assertIsNone(ed.not_natural(dict(summary, game_options=options)))

    def test_one_way_save_lineage_cannot_be_exported_as_an_ordinary_death(self):
        run = make_run(self.base, 'unmarked-loaded-one-way', loaded=True,
                       game_options=dict(birth_force_descend=True, birth_no_recall=True))
        case, reason = ed.export(run, 'rust', self.build)
        self.assertIsNone(case)
        self.assertIn('one-way birth options', reason)
        self.assertFalse(self.reg.exists())

    def test_death_writes_a_dossier(self):
        run = make_run(self.base, 'dead')
        case, what = ed.export(run, 'c', self.build, 'menu')
        self.assertEqual((case, what), (self.first_id, 'exported'))
        d = self.reg / case
        rec = json.loads((d / 'record.json').read_text())
        self.assertEqual(rec['terminal']['cause'], 'a cave spider')
        self.assertEqual(rec['terminal']['turn'], 12345)
        self.assertEqual(rec['identity']['flags'], 'menu')
        self.assertEqual(rec['identity']['binary_sha256'], 'beef')
        self.assertIn('keys.log', rec['attempts'][0]['raw_sha256'])
        self.assertTrue(rec['encounter_family'].startswith('start-'))
        self.assertEqual(json.loads((d / 'assessment.json').read_text())['classification'], 'unassessed')
        self.assertIn('a cave spider at turn 12345', (d / 'report.md').read_text())
        self.assertFalse((d / 'keys.log').exists(), 'raw logs are not copied into the dossier')

    def test_trace_and_parameters_go_into_the_dossier(self):
        # T2.4: the reborn Borg's params.json and the end of its trace.
        run = make_run(self.base, 'traced')
        (run / 'params.json').write_text('{"profile_sha256": "abc"}\n')
        (run / 'trace.jsonl').write_text(''.join(f'{{"think": {i}}}\n' for i in range(1, 251)))
        (run / 'config.txt').write_text('flags=-\nborg_txt_sha256=feed\nprofile_sha256=abc123\n')
        case, _ = ed.export(run, 'rust', self.build)
        d = self.reg / case
        tail = (d / 'trace-tail.jsonl').read_text().splitlines()
        self.assertEqual(len(tail), ed.TRACE_TAIL)
        self.assertEqual((tail[0], tail[-1]), ('{"think": 51}', '{"think": 250}'), 'the last thinks')
        self.assertEqual((d / 'params.json').read_text(), '{"profile_sha256": "abc"}\n')
        rec = json.loads((d / 'record.json').read_text())
        self.assertEqual(rec['identity']['profile_sha256'], 'abc123')
        self.assertEqual(rec['decision_trace'], {'file': 'trace-tail.jsonl', 'lines': 200, 'of': 250})
        self.assertIn('trace-tail.jsonl', rec['files_sha256'])
        self.assertIn('Decision trace: the last 200 of 250 thinks', (d / 'report.md').read_text())
        # A C run has neither: the record says so.
        c, _ = ed.export(make_run(self.base, 'untraced', seed=7), 'c', self.build)
        self.assertIsNone(json.loads((self.reg / c / 'record.json').read_text())['decision_trace'])

    def test_a_plan_run_keeps_the_plan_it_read(self):
        # Issue #3: a dossier is self-contained even if the source checkout's
        # plan file is edited later.
        run = make_run(self.base, 'planned')
        (run / 'user').mkdir()
        plan = '/dive 3\n'
        (run / 'user/errands_plan.txt').write_text(plan)
        with (run / 'config.txt').open('a') as f:
            f.write('borg_errands_plan=harness/plans/p.txt\n')
            f.write('borg_errands_plan_sha256=' + ed.sha256_file(run / 'user/errands_plan.txt') + '\n')
        case, _ = ed.export(run, 'rust', self.build)
        d = self.reg / case
        self.assertEqual((d / 'errands_plan.txt').read_text(), plan)
        self.assertIn('errands_plan.txt', json.loads((d / 'record.json').read_text())['files_sha256'])
        # A run without a plan gets no empty file.
        other, _ = ed.export(make_run(self.base, 'plain', seed=5), 'rust', self.build)
        self.assertFalse((self.reg / other / 'errands_plan.txt').exists())

    def test_named_core_trace_tail_is_preserved_and_hashed(self):
        run = make_run(self.base, 'core-trace')
        (run / 'params-core.json').write_text('[]\n')
        rows = [{'think': i, 'check': 'borg_caution', 'keys': [27]} for i in range(1, 251)]
        (run / 'trace-core.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
        case, _ = ed.export(run, 'rust', self.build)
        d = self.reg / case
        tail = [json.loads(l) for l in (d / 'trace-core-tail.jsonl').read_text().splitlines()]
        self.assertEqual(tail, rows[-200:])
        rec = json.loads((d / 'record.json').read_text())
        self.assertEqual(rec['core_decision_trace'], {'file': 'trace-core-tail.jsonl', 'lines': 200, 'of': 250})
        self.assertIsNone(rec['decision_trace'])
        self.assertIn('trace-core-tail.jsonl', rec['files_sha256'])
        self.assertIn('Core decision trace: the last 200 of 250 thinks', (d / 'report.md').read_text())

    def test_vendored_core_parameters_are_preserved_and_hashed(self):
        run = make_run(self.base, 'core')
        params = '[{"name":"caution_clw_min_loss","value":20}]\n'
        (run / 'params-core.json').write_text(params)
        with (run / 'config.txt').open('a') as f:
            f.write('params_core_sha256=' + ed.sha256_file(run / 'params-core.json') + '\n')
        case, _ = ed.export(run, 'rust', self.build)
        d = self.reg / case
        self.assertEqual((d / 'params-core.json').read_text(), params)
        rec = json.loads((d / 'record.json').read_text())
        self.assertEqual(rec['files_sha256']['params-core.json'], ed.sha256_file(run / 'params-core.json'))
        self.assertEqual(rec['identity']['params_core_sha256'], ed.sha256_file(run / 'params-core.json'))
        changed = dict(params_core_sha256='different')
        self.assertNotEqual(ed.run_family({}, changed, 'rust', 'source'),
                            ed.run_family({}, {}, 'rust', 'source'))

    def test_partial_suite_directory_is_recorded_as_final(self):
        run = make_run(self.base / 'out.partial.4242', 'dead')
        case, _ = ed.export(run, 'c', self.build)
        rec = json.loads((self.reg / case / 'record.json').read_text())
        self.assertEqual(rec['attempts'][0]['raw_directory'], str((self.base / 'out' / 'dead').resolve()))

    def test_repeat_is_not_a_new_case(self):
        ed.export(make_run(self.base, 'one'), 'c', self.build)
        self.assertEqual(ed.export(make_run(self.base, 'two'), 'c', self.build), (self.first_id, 'repeat'))
        self.assertEqual(len([d for d in self.reg.iterdir() if d.is_dir()]), 1)

    def test_interrupted_dossier_is_repaired_not_accepted(self):
        case, _ = ed.export(make_run(self.base, 'one'), 'c', self.build)
        d = self.reg / case
        (d / 'report.md').unlink()
        (d / 'assessment.json').unlink()
        record_before = (d / 'record.json').read_bytes()
        got = ed.export(make_run(self.base, 'two'), 'c', self.build)
        self.assertEqual(got, (case, 'repaired: assessment.json, report.md'))
        self.assertTrue((d / 'report.md').exists() and (d / 'assessment.json').exists())
        self.assertEqual((d / 'record.json').read_bytes(), record_before, 'existing files are kept')
        self.assertEqual(ed.export(make_run(self.base, 'three'), 'c', self.build), (case, 'repeat'))

    def test_missing_config_is_restored(self):
        case, _ = ed.export(make_run(self.base, 'one'), 'c', self.build)
        (self.reg / case / 'config.txt').unlink()
        self.assertEqual(ed.export(make_run(self.base, 'two'), 'c', self.build), (case, 'repaired: config.txt'))
        self.assertIn('borg_txt_sha256', (self.reg / case / 'config.txt').read_text())

    def test_filled_in_assessment_is_never_overwritten(self):
        case, _ = ed.export(make_run(self.base, 'one'), 'c', self.build)
        a = self.reg / case / 'assessment.json'
        a.write_text('{"classification": "assessed by a person"}')
        (self.reg / case / 'report.md').unlink()
        ed.export(make_run(self.base, 'two'), 'c', self.build)
        self.assertIn('assessed by a person', a.read_text())

    def test_stale_temporary_directory_is_removed(self):
        self.reg.mkdir(parents=True)
        (self.reg / '.tmp-D0001-c-seed101').mkdir()
        (self.reg / '.tmp-D0001-c-seed101' / 'record.json').write_text('{half')
        case, what = ed.export(make_run(self.base, 'one'), 'c', self.build)
        self.assertEqual((case, what), (self.first_id, 'exported'))
        self.assertFalse((self.reg / '.tmp-D0001-c-seed101').exists())

    def test_case_without_record_fails_loudly(self):
        (self.reg / 'D0001-c-seed101').mkdir(parents=True)
        with self.assertRaises(SystemExit):
            ed.export(make_run(self.base, 'one'), 'c', self.build)

    def test_rebuilt_binary_of_same_source_is_a_repeat(self):
        case, _ = ed.export(make_run(self.base, 'one'), 'c', self.build)
        rebuilt = self.base / 'BUILD_ID2'
        rebuilt.write_text('impl=c\ngit_rev=89abcde\ngit_dirty=yes\nbinary_sha256=0ther\nsource_sha256=cafe\n')
        self.assertEqual(ed.export(make_run(self.base, 'two'), 'c', rebuilt), (case, 'repeat'))

    def test_changed_source_is_a_new_family(self):
        ed.export(make_run(self.base, 'one'), 'c', self.build)
        changed = self.base / 'BUILD_ID2'
        changed.write_text('impl=c\ngit_rev=89abcde\ngit_dirty=no\nbinary_sha256=beef\nsource_sha256=d1ff\n')
        case, what = ed.export(make_run(self.base, 'two'), 'c', changed)
        self.assertEqual(what, 'exported')
        self.assertNotEqual(case, self.first_id)

    def test_main_aggregates_the_registry(self):
        run = make_run(self.base, 'dead')
        self.assertEqual(ed.main([str(run), '--impl', 'c', '--build-id', str(self.build)]), 0)
        index = json.loads((self.reg / 'index.json').read_text())
        self.assertEqual((index['cases'], index['distinct_starting_conditions']), (1, 1))
        self.assertIn(self.first_id, (self.reg / 'README.md').read_text())

    def test_only_natural_deaths_are_exported(self):
        for extra, flags in (({'stop_reason': 'turns'}, '-'), ({'cheat_live': True}, '-'), ({}, 'cheatlive'),
                             ({}, 'cheat,menu'), ({'death_cause': 'Quitting'}, '-'),
                             ({'death_cause': 'Retiring'}, '-'), ({'death_cause': 'Interrupting'}, '-'),
                             ({'death_cause': ''}, '-'), ({'death_cause': None}, '-')):
            run = make_run(self.base / f'case{len(list(self.base.iterdir()))}', 'r', **extra)
            case, what = ed.export(run, 'c', self.build, flags)
            self.assertIsNone(case, (extra, flags))
            self.assertTrue(what.startswith('not natural'), what)
        self.assertFalse(self.reg.exists() and any(d.is_dir() for d in self.reg.iterdir()))

    def test_saved_rng_ignores_the_seed_and_random_birth_uses_the_played_character(self):
        loaded = 'save=fixture.sav,keep-load-rng'
        a, _ = ed.export(make_run(self.base, 'a', seed=1, loaded=True), 'c', self.build, loaded)
        self.assertEqual(ed.export(make_run(self.base, 'b', seed=2, loaded=True), 'c', self.build, loaded),
                         (a, 'repeat'))
        # Re-review N7: keep-load-rng without a save has no effect; the seed counts.
        n1, _ = ed.export(make_run(self.base, 'n1', seed=1), 'c', self.build, 'keep-load-rng')
        n2, what_n2 = ed.export(make_run(self.base, 'n2', seed=2), 'c', self.build, 'keep-load-rng')
        self.assertNotEqual(n1, n2)
        self.assertEqual(what_n2, 'exported')
        b, what = ed.export(make_run(self.base, 'c', seed=3, played_race_idx=4, played_class_idx=5), 'c', self.build,
                            'random-birth')
        c, what2 = ed.export(make_run(self.base, 'd', seed=3, played_race_idx=6, played_class_idx=1), 'c', self.build,
                             'random-birth')
        fam = lambda case: json.loads((self.reg / case / 'record.json').read_text())['encounter_family']
        self.assertNotEqual(fam(b), fam(c), 'different played characters are different starts')
        # Re-review N8: the terminal record names the character played.
        term = json.loads((self.reg / b / 'record.json').read_text())['terminal']
        self.assertEqual((term['race_idx'], term['class_idx']), (4, 5))

    def test_a_save_loaded_through_extra_options_ignores_the_seed(self):
        # Re-review R3: run.sh ... -- -load FILE -keep-load-rng. borgh says
        # "loaded"; run.sh records the save's hash and keep_load_rng=1.
        def run(name, seed, save='5a7e'):
            r = make_run(self.base, name, seed=seed, loaded=True)
            (r / 'config.txt').write_text(f'flags=-\nborg_txt_sha256=feed\nsave_sha256={save}\nkeep_load_rng=1\n')
            return r
        a, _ = ed.export(run('a', 1), 'c', self.build)
        self.assertEqual(ed.export(run('b', 2), 'c', self.build), (a, 'repeat'))
        other, what = ed.export(run('c', 2, save='0ther'), 'c', self.build)
        self.assertEqual(what, 'exported', 'another save is another start')
        # Loaded but with the game's RNG reseeded: the seed counts.
        r1 = make_run(self.base, 'r1', seed=1, loaded=True)
        r2 = make_run(self.base, 'r2', seed=2, loaded=True)
        self.assertNotEqual(ed.export(r1, 'c', self.build)[0], ed.export(r2, 'c', self.build)[0])

    def test_a_repeat_repairs_a_stale_index(self):
        run = make_run(self.base, 'dead')
        args = [str(run), '--impl', 'c', '--build-id', str(self.build)]
        ed.main(args)
        (self.reg / 'index.json').unlink()
        (self.reg / 'README.md').unlink()
        ed.main([str(make_run(self.base, 'again')), '--impl', 'c', '--build-id', str(self.build)])
        self.assertEqual(json.loads((self.reg / 'index.json').read_text())['cases'], 1)
        self.assertTrue((self.reg / 'README.md').exists())

    def test_hash_ids_and_family(self):
        ed.export(make_run(self.base, 'one'), 'c', self.build)
        case, _ = ed.export(make_run(self.base, 'two', seed=102), 'rust', self.build)
        self.assertRegex(case, r'^D-[0-9a-f]{64}$')
        self.assertNotEqual(case, self.first_id)
        fam = {json.loads((d / 'record.json').read_text())['encounter_family']
               for d in self.reg.iterdir() if d.is_dir()}
        self.assertEqual(len(fam), 2, 'different seed and implementation: different start')

    def test_same_start_different_play_is_same_family(self):
        a, _ = ed.export(make_run(self.base, 'one'), 'c', self.build)
        b, what = ed.export(make_run(self.base, 'two', keys='other\n'), 'c', self.build)
        self.assertEqual(what, 'exported')
        fams = [json.loads((self.reg / c / 'record.json').read_text())['encounter_family'] for c in (a, b)]
        self.assertEqual(fams[0], fams[1])

    def test_separate_branch_registries_assign_the_same_ids_in_opposite_orders(self):
        one = make_run(self.base, 'one')
        two = make_run(self.base, 'two', keys='other\n')
        first = ed.export(one, 'c', self.build)[0]
        second = ed.export(two, 'c', self.build)[0]
        # Frozen version-1 vector: changing the encoding is an ID migration.
        self.assertEqual(first, 'D-e4223d59c64aa5703a8d5f6495685de8facf0852a4d96ddc0276aff446db7209')
        os.environ['BORG_DEATH_RECORDS_DIR'] = str(self.base / 'other-branch')
        self.assertEqual(ed.export(two, 'c', self.build)[0], second)
        self.assertEqual(ed.export(one, 'c', self.build)[0], first)
        self.assertNotEqual(first, second)

    def test_legacy_repeat_adds_metadata_without_rewriting_original_evidence(self):
        run = make_run(self.base, 'one')
        canonical, _ = ed.export(run, 'c', self.build)
        legacy = self.reg / 'D0099-c-seed101'
        (self.reg / canonical).rename(legacy)
        record = json.loads((legacy / 'record.json').read_text())
        record['id'] = legacy.name
        (legacy / 'record.json').write_text(json.dumps(record))
        (legacy / 'death-id.json').unlink()
        original = (legacy / 'record.json').read_bytes()
        case, result = ed.export(make_run(self.base, 'repeat'), 'c', self.build)
        self.assertEqual(case, legacy.name)
        self.assertEqual(result, 'repaired: death-id.json')
        self.assertEqual((legacy / 'record.json').read_bytes(), original)
        self.assertEqual(json.loads((legacy / 'death-id.json').read_text())['id'], canonical)

    def test_repeat_refuses_tampered_identity_metadata(self):
        run = make_run(self.base, 'one')
        case, _ = ed.export(run, 'c', self.build)
        path = self.reg / case / 'death-id.json'
        value = json.loads(path.read_text())
        value['id'] = 'D-' + '0' * 64
        path.write_text(json.dumps(value))
        before = (self.reg / case / 'record.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'differs'):
            ed.export(make_run(self.base, 'repeat'), 'c', self.build)
        self.assertEqual((self.reg / case / 'record.json').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
