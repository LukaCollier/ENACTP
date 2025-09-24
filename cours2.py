from math import sqrt

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def move(self,dx,dy):
        self.x += dx
        self.y += dy
    def scale(self,k):
        self.x *= k
        self.y *= k

    def __abs__(self):
        return sqrt(self.x**2+self.y**2)

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    def __repr__(self):
        return f"{self.x} en x et {self.y} en y"


p1=Point(23,42)

p2=Point(-3,65)

p1.move(1,0)
print(p1)
p2.scale(2)
print(p2)
p3=Point(-3,0)

print(abs(p3))

print(p1+p2)


def nom_mois(date):
    MOIS=("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")
    return MOIS[date[1]-1]

print(nom_mois((17,9,2005)))

def periode(m1,m2):
    return tuple((nom_mois((1,i,0)) for i in range(m1,m2+1)))
def periode2(m1,m2):
    MOIS=("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")
    return MOIS[m1-1:m2]
print(periode(1,6))
print(periode(6,1))
def fact(n):
    if n==0 or n==1:
        return 1
    else:
        res = 1
        for i in range(2,n+1):
            res *=i
        return res

print(fact(4))
def pref(car,s):
    ncar=len(car)
    ns=len(s)
    if ncar>ns:
        return False
    n=min(ncar,ns)
    return car[:n]==s[:n]

def select(car):
    L=["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"]
    res=[]
    for i in L:
        if pref(car,i):
            res.append(i)
    return res

print(select("j"))
