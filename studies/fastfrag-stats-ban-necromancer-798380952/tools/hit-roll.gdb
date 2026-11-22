set pagination off
set confirm off
set $in = 0
break make_ranged_throw if *(unsigned int*)&turn >= 93800
commands
silent
set $in = 1
printf "make_ranged_throw turn=%u\n", *(unsigned int*)&turn
continue
end
break random_chance_check if $in == 1
commands
silent
printf "  random_chance_check num=%d den=%d\n", (int)($rdi & 0xffffffff), (int)($rdi >> 32)
set $in = 0
continue
end
break monster_is_obvious if $in == 1
commands
silent
printf "  monster_is_obvious called\n"
continue
end
run
