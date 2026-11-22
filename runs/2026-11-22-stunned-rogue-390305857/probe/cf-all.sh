set -u
for spec in 78746:stairs_down 78756:quaff_csw 78765:quaff_csw 78765:quaff_clw 78807:phase 78823:phase 78849:phase; do
  t=${spec%%:*}; a=${spec#*:}
  CF_PROBE=1 CF_TURN=$t CF_ACTION=$a ${WORK:?set WORK to a scratch dir}/replay.sh /home/user/borg-reborn-rs/.worktrees/yeek-cf-scratch/build/rust/game/angband ${WORK:?set WORK to a scratch dir}/cf-$t-$a 100000
done
