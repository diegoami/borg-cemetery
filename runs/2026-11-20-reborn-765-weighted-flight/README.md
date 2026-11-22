# Local threat-weighted stair flight evidence (#765)

These records cover the earlier local, directional arm described in
[borg-reborn-rs PR #769](https://github.com/diegoami/borg-reborn-rs/pull/769).
The separate [Zoo pilot #524](https://github.com/diegoami/borg-zoo/issues/524)
uses the later reviewed branch head.

The original source was `d8edf54655d80d29cc645d5a7a1616fab6d0ccac`. The
[build receipt](BUILD_ID), [manifest](manifest-600.txt) and
[600 outcome receipts](receipts.jsonl.gz) record the start identities and
key-stream and configuration hashes. The hard cap was 100,000 exact game
turns. Ten starts died and 590 reached the cap. The two timeouts and their
retries each represent one life.

## Reproduction

Build the original source with `harness/build.sh`. The pinned
[scratch runner](https://github.com/diegoami/borg-reborn-rs/blob/e4bcb70f58b3d63b06b2c8fb6ba0fcb106e21786/scratch-757/zrun.py)
takes the game directory and the source harness directory followed by
the output directory, seed, race index, class index and turn cap. Use the
row from the manifest and pass the following overrides.

```text
borg_param_caution_stairs_clean_path=3
borg_param_caution_desperate_fast_danger_percent=50
borg_param_caution_recall_cure_min_loss_percent=30
borg_param_caution_stairs_flight_ignore_danger=1
borg_param_caution_stairs_clean_path_flee=1
borg_param_caution_stairs_flight_threat_weight=5
```

Each dossier links its run directory by repository-relative path. The
compressed streams and configuration there expand to the recorded bytes.

## Natural deaths

| Seed | Class | Cause | Turn | Dossier |
| ---: | --- | --- | ---: | --- |
| 73008731 | Necromancer | a floating eye | 7,600 | [D-5bd6ea1ea2](../../deaths/D-5bd6ea1ea2c106e576571cb65624c5963d059ad63a7ecdefb06b3bf2cd17d6cf/README.md) |
| 138331922 | Ranger | a rock lizard | 3,267 | [D-ed962649d3](../../deaths/D-ed962649d39caaab684ef0451e3a0942638ff0b9f949bda1350aa8ef7bae8584/README.md) |
| 179371675 | Priest | a soldier | 70,783 | [D-795955076d](../../deaths/D-795955076d1aeaa6fe891941e9d4696d2c3b8bcb0ea2577a7a211a948dfaf37e/README.md) |
| 211798192 | Priest | a wild dog | 13,526 | [D-7c33602f6f](../../deaths/D-7c33602f6fbef09536e8603cc5d7129bc7ae818d142e6e298bd4c27965c358c6/README.md) |
| 229641482 | Priest | an acolyte | 16,239 | [D-a039106b3b](../../deaths/D-a039106b3be508c4124ead37e4af28a83f7f1706c2423d4a6fb9f1b96e057c90/README.md) |
| 312789942 | Necromancer | a fatal wound | 2,050 | [D-8a6005fa41](../../deaths/D-8a6005fa414c20689df70cccd30a396de350713ccd77ce34a3e22b676af8f6cb/README.md) |
| 347186112 | Ranger | a giant white mouse | 6,776 | [D-ca5888a7fe](../../deaths/D-ca5888a7fe30715020ac0bd87dfdddf1ef0f6edf8f97940c4fcc9f4d3a349b21/README.md) |
| 695838733 | Ranger | a grey mold | 3,193 | [D-3580baac6e](../../deaths/D-3580baac6ed2bdc6f3af46b4ba8a67e468ea39c2c8aa58be2e152c04abcb3651/README.md) |
| 1483603518 | Ranger | a crow | 2,807 | [D-e210e07e5c](../../deaths/D-e210e07e5ce7adc0fb35cb9f191c93ce9e78f1f1fbda744cee09541574a58e0d/README.md) |
| 2062721505 | Ranger | a floating eye | 11,477 | [D-998bdad808](../../deaths/D-998bdad8085feea35dd859a98dd05a52ad61d1f9b14ac55f3aa609b7aa6d24a0/README.md) |

## Wall-time attempts

Both initial attempts hit the 300-second wall limit. Each retry reached
100,000 turns. The original retry receipts retain their full key-log hashes.
A fresh replay from the same source and per-start configuration reproduced
each retained retry hash and began with the exact bytes of the corresponding
timeout log. The fresh-replay measurements below are per-game timings.
They include the entire game under the weighted setting.

| Seed | Exact prefix (bytes) | Replay user CPU (s) | Replay wall (s) |
| ---: | ---: | ---: | ---: |
| [23482467](timeouts/c400-23482467-6-6/attempts.json) | 131,072 | 34.65 | 35.32 |
| [149213750](timeouts/c400-149213750-7-8/attempts.json) | 65,536 | 234.82 | 235.62 |
