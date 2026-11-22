import sys,os,glob
root=sys.argv[1]; seen=set()
for m in sorted(glob.glob(root+'/**/messages.log',recursive=True)):
    L=[l.rstrip('\n').split(' ',3) for l in open(m,errors='replace')]
    L=[x for x in L if len(x)==4 and x[1].isdigit()]
    if not L: continue
    dead=any(x[3]=='You die.' for x in L[-60:])
    if not dead: continue
    end=int(L[-1][1])
    tail=[x for x in L if int(x[1])>=end-int(sys.argv[2])]
    harm=sum('You fail to harm' in x[3] for x in tail)
    stun=sum('You have been stunned' in x[3] or 'heavily stunned' in x[3] or 'knocked out' in x[3] for x in tail)
    harm_all=sum('You fail to harm' in x[3] for x in L)
    if harm or stun:
        parts=m.split('/'); key='/'.join(parts[-4:-1])
        print(f"{harm:3d} fail-to-harm, {stun} stun msgs in last 100 turns (whole game {harm_all}) | death turn {end} | {key}")
