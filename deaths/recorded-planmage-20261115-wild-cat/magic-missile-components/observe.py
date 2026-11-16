import gdb,json

def reg(n):return int(gdb.parse_and_eval('(long)$'+n))
def turn():return int(gdb.parse_and_eval('*(int*)&turn'))
def emit(x):print('COMPONENT '+json.dumps(x),flush=True)
class Finish(gdb.FinishBreakpoint):
 def __init__(self,frame,data):
  super().__init__(frame,internal=True);self.data=data
 def stop(self):
  self.data.update(eax=reg('eax'),edx=reg('edx'),rax=reg('rax'));emit(self.data);return False
class Component(gdb.Breakpoint):
 def __init__(self,name,args):
  super().__init__(name,internal=True);self.name_=name;self.args=args
 def stop(self):
  if turn()!=411668:return False
  data={'function':self.name_,'turn':turn(),'args':{k:reg(v) for k,v in self.args.items()}}
  f=gdb.newest_frame().older();stack=[]
  for _ in range(6):
   if f is None:break
   stack.append(f.name());f=f.older()
  data['stack']=stack
  Finish(gdb.newest_frame(),data);return False
class Arm(gdb.Breakpoint):
 def stop(self):
  if turn()<411658:return False
  for name,args in [
   ('borg_rs::borg_fight_attack::borg_calculate_attack_effectiveness',{'attack':'esi'}),
   ('borg_rs::borg_fight_attack::borg_thrust_damage_one',{'monster':'esi'}),
   ('borg_rs::borg_fight_attack::melee_score',{'monster':'esi','x':'edx','y':'ecx','damage':'r8d'}),
   ('borg_rs::borg_fight_attack::borg_launch_bolt_aux_hack',{'monster':'esi','damage':'edx','type':'ecx','ammo':'r8d'}),
   ('borg_rs::borg_fight_attack::borg_launch_damage_one',{'monster':'esi','damage':'edx','type':'ecx','ammo':'r8d'}),
   ('borg_rs::borg_fight_attack::borg_attack_aux_spell_bolt',{'spell':'esi','radius':'edx','damage':'ecx','type':'r8d','range':'r9d'}),
   ('borg_rs::borg_danger::borg_danger_one_kill',{'y':'esi','x':'edx','horizon':'ecx','monster':'r8d','average':'r9d'})]:
   try:Component(name,args)
   except Exception as e:emit({'setup_error':name,'error':str(e)})
  self.enabled=False;emit({'armed_at':turn()});return False
Arm('ar_frame',internal=True)
