# Replay inputs

One folder per death, named by seed. Each folder replays the zoo game exactly, with no zoo artifact and no GitHub token. It holds:
- `config.txt` and `zoo-death.json`: the cell, the commit in `build.ref`, the key hash in `play_sha256`;
- `user/`: the cell's `borg.txt` with its settings, the scary list, and any plan;
- the zoo's `messages.log`, `state.log` and `keys.log`, to compare against.

```sh
git clone https://github.com/diegoami/borg-cemetery && cd borg-cemetery
runs/replay-zoo-death.sh <this folder>/<SEED>                     # clones borg-reborn-rs at the death's commit, builds, replays, checks the keys
runs/replay-zoo-death.sh <this folder>/<SEED> /tmp/w ~/borg-reborn-rs   # the same game on your own checkout (a branch to test)
```

With the death's commit the script prints "same game as the zoo". With a changed checkout it says whether the game still matches. If it doesn't, diff `run/messages.log` against this folder's `messages.log`. Lines read: message index, game turn, type, text.
