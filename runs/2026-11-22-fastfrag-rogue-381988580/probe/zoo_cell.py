# The zoo adapter call used to rebuild the cell (run from a borg-zoo checkout; paths are this session's).
# "build" builds borg-reborn-rs 7f8c6b80 at the zoo's path; "run" plays the cell with logs kept.
import sys, json, hashlib
sys.path.insert(0, '/home/user/borg-zoo')
from pathlib import Path
from zoo import catalogue as cat_mod, borgrs
cat = cat_mod.catalogue()
spec_name = '4.2.6-reborn-rust-fast-fragile-7f8c6b80'
spec = cat['specimens']['specimens'][spec_name]
mode, out_build, work = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
if mode == 'build':
    print(borgrs.build(spec, '/home/runner/work/borg-zoo/borg-zoo/source', out_build)['binary_sha256'])
else:
    prof = sys.argv[4] if len(sys.argv) > 4 else 'reborn-fastfrag-stats-ban'
    cell = {'specimen': spec_name, 'profile': prof, 'suite': 'classes-1800-big', 'seed': 381988580}
    suite = cat['suites']['classes-1800-big']
    cell['race'], cell['class'] = cat_mod.character(suite, 381988580)
    print(cell)
    rec = borgrs.run_cell(cell, out_build, work, cat, keep=True)
    print(json.dumps({k: rec.get(k) for k in ('outcome','death_cause','game_turns','keys_sha256','play_sha256','config_sha256')}, default=str))
    print(sorted(rec.keys()))
