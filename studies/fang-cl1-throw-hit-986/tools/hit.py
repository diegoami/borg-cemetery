import gdb, os
gdb.execute("set pagination off")
LOG = os.environ["HITLOG"]; state = {"on": False, "info": ""}
def reg(n): return int(gdb.parse_and_eval(f"(long)${n}"))
class Fin(gdb.FinishBreakpoint):
    def __init__(s, f): super().__init__(f, internal=True)
    def stop(s):
        rax = reg("rax")
        ok = int(gdb.parse_and_eval(f"*(unsigned char*){rax}")); dmg = int(gdb.parse_and_eval(f"*(int*)({rax}+4)"))
        turn = int(gdb.parse_and_eval("*(int*)&turn"))
        open(LOG, "a").write(f"THROW turn={turn} {state['info']} success={ok} dmg={dmg}\n"); state["on"] = False; return False
class M(gdb.Breakpoint):
    def stop(s):
        state["on"] = True; state["info"] = "no-hit_chance-call"; Fin(gdb.newest_frame()); return False
class H(gdb.Breakpoint):
    def stop(s):
        if not state["on"]: return False
        v = reg("rdi"); num = v & 0xffffffff; den = (v >> 32) & 0xffffffff
        state["info"] = f"engine_chance={num}/{den}={100*num/den:.2f}%"; return False
M("make_ranged_throw"); H("random_chance_check")
gdb.execute("run")
