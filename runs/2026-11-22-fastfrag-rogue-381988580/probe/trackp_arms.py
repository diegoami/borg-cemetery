# Named-case runs on borg-reborn-rs track-p (608d9fed = track-p 9085c266 + PRs #920-#924)
# through borg-zoo's own adapter: build, borg.txt, argv, as a zoo cell.
import sys, json, copy, hashlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '/home/user/borg-zoo')
from pathlib import Path
from zoo import catalogue as cat_mod, borgrs
cat = cat_mod.catalogue()
SRC = '/home/user/borg-reborn-rs/.worktrees/T911'
REF = '608d9fed67f3' 
import subprocess
REF = subprocess.check_output(['git', '-C', SRC, 'rev-parse', 'HEAD'], text=True).strip()
spec = copy.deepcopy(cat['specimens']['specimens']['4.2.6-reborn-rust-fast-fragile-7f8c6b80'])
spec['ref'] = REF; spec['label'] = 'local: track-p + #920-#924'
spec['scary_lists'] = {'scary_monsters.txt': hashlib.sha256(open(SRC + '/harness/scary_monsters.txt', 'rb').read()).hexdigest()}
NAME = '4.2.6-reborn-rust-trackp-907-911-local'
cat['specimens']['specimens'][NAME] = spec
ALL = {'borg_param_caution_desperate_fast_haste': 1, 'borg_param_danger_observed_haste': 1,
       'borg_param_caution_desperate_walk_cost_percent': 100, 'borg_param_caution_heal_lethal_over_max': 1,
       'borg_param_caution_heal_outmatched_before_walk': 1, 'borg_param_caution_winning_fight_margin_percent': 20,
       'borg_param_caution_winning_fight_group_percent': 100, 'borg_param_caution_scary_take_distance': 5}
for base in ('reborn-fastfrag-ctl', 'reborn-fastfrag-stats-ban'):
    p = copy.deepcopy(cat['profiles'][base]); p['settings'].update(ALL); cat['profiles'][base + '+all'] = p
mode, build, work = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
if mode == 'build':
    print(borgrs.build(spec, SRC, build)['binary_sha256']); sys.exit()
seeds = [int(s) for s in sys.argv[4].split(',')]
profiles = sys.argv[5].split(',')
suite = cat['suites']['classes-1800-big']
def one(job):
    prof, seed = job
    cell = {'specimen': NAME, 'profile': prof, 'suite': 'classes-1800-big', 'seed': seed}
    cell['race'], cell['class'] = cat_mod.character(suite, seed)
    rec = borgrs.run_cell(cell, build, work, cat, keep=True)
    d = work / cat_mod.cell_key(cell)
    s = json.loads((d / 'summary.json').read_text())
    notes = sum(1 for l in open(d / 'messages.log', errors='replace')
                if any(t in l for t in ('(#908)', '(#911)', 'Healing (outmatched)')))
    return {'profile': prof, 'seed': seed, 'character': f"{cell['race']} {cell['class']}", 'outcome': s['stop_reason'],
            'turn': s['game_turns'], 'cause': s.get('death_cause'), 'clevel': s['clevel'], 'max_depth': s['max_depth'],
            'keys_sha256': rec['play_sha256'], 'config_sha256': rec['config_sha256'], 'new_rule_notes': notes}
jobs = [(p, s) for s in seeds for p in profiles]
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(one, jobs):
        print(json.dumps(r), flush=True)
