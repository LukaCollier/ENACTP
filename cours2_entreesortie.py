def logenac(s):
    s=s.lower()
    pn=s.split(maxsplit=1)
    n=''.join(pn[1].split())
    p=pn[0].split('-')
    return n[:6]+(pn[0][:2] if len(p) < 2 else p[0][0]+p[1][0] )


print(logenac("Luka Collier"))
print(logenac("Pierre-Simon de Laplace"))


def sous_sequence(s1,s2):
    n1=len(s1)
    n2=len(s2)
    if (n1>n2):
        return False
    else:
        tmp=s2
        for c in s1:
            flg=False
            for (i,c2) in enumerate(tmp):
                if c==c2:
                    flg=True
                    tmp=tmp[(i+1):]
                    break
            if not(flg):
                return False
        return True

print(sous_sequence("ienac","indépendance"))

