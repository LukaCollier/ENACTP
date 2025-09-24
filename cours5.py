def avg(s):
    if len(s) == 0:
        raise ValueError("nullos seq vide")
    return sum(s)/len(s)

def get_type(s):
    try:
        int(s)
        return "int"
    except ValueError:
        try:
            float(s)
            return "float"
        except ValueError:
            return "str"

class InputError(Exception):
    pass

def input_int(question,nmin,nmax,nfois):
    if nfois<=0:
        raise InputError("max attemps reached")
    try:
        n = int(input(f'\n{question}  {nmin} et {nmax-1} ?\n n = '))
        if  n>=nmax or n<nmin:
            return input_int(question,nmin,nmax,nfois-1)
        else :
            print("bravo")
    except ValueError:
        return input_int(question,nmin,nmax,nfois-1)


def input_int_prof(question,nmin,nmax,nfois):
    for _ in range(nfois):
        try:
            n = int(input(question))
            if nmin <= n <nmax:
                return n
        except ValueError:
            pass
    raise InputError("Nombre max d'essais atteint")
    
'''
jeu de test pour input_int:

- a / b / 456 / -1024 / 15.5

- test/ int / 5
'''
'''
#print(avg(set()))
print(avg({1,2,3,5,6,7,8786,1,13}))
print(get_type("5"))
print(get_type("5.5"))
print(get_type("r"))
input_int_prof("donne un entier entre ",0,100,5)
'''

class Poly:

    def __init__(self,coef):
        if len(coef)==0:
            raise ValueError("pas de coefficients en entrée")
        elif coef[-1]==0:
            raise ValueError("0 à la fin (inutile)")
        else:
            self.coef=coef
    def __repr__(self):
        return f"{self.coef}"
    def deg(self):
        return len(self.coef)

    
    def eval(self,x):
        res=0
        for (i,j) in enumerate(self.coef):
            res+= j*(x**i)
        return res

    def horner(self,x):
        res=0
        l=list(reversed(self.coef))[:-1]
        for a in l:
            res= (res + a)*x
        return res + self.coef[0]
    def eval_compr(self,x):
        return sum([j*(x**i) for i,j in enumerate(self.coef)])

    

p=Poly([1,2,3,456,5])
print(p.deg())

print(p.eval(2))
print(p.horner(2))
print(p.eval_compr(2))
p
#p=Poly([1,2,3,4,6,0])
#p=Poly([])
