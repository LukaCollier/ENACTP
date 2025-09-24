from math import *
from random import randint
Mach=0.77
Npax= 185
Raction= 3250  #Nm
Alt= 330 #FL330
All =8.93 #random
Cs=14.1e-6
Racm=6.019e6
g=9.81
V=Mach*299
def PNC(pax):
    return ceil(pax/50)

def Mequipage(pax):
    return (PNC(pax)+2)*100
def Marchande(pax):
    return pax*100

def Mvide(M0):
    return 0.97 * (M0**(-0.06))


def M3_M2(R,g,Cs,V,f):
    '''
    R= Raction
    V=vitesse de croissère (m/s)
    g=9.81 m/s-2
    f = finesse de l'avion
    Cs = conso spécifique
    '''
    val = - (R*g*Cs)/(V*f)
    return exp(val)

def Mcarb_M0(R,g,Cs,V,f):
    return 1.06*(1- 0.995*0.985*0.970*M3_M2(R,g,Cs,V,f))

def allongementrandom(n):
    res=[randint(7,11) for i in range(n)]
    return sum(res)/len(res)

def Allongement(*g):
    pass

def fin(al):
    return ((0.866*15.5)/sqrt(6))*sqrt(al)
def prec(n,m,e):
    return abs(n-m)<e
def trueM0(Mi0,R,g,Cs,V,f):
    Meqmr=Mequipage(Npax)+Marchande(Npax)
    k=1-Mcarb_M0(R,g,Cs,V,f)-Mvide(Mi0)
    tmp=Meqmr/k
    if prec(Mi0,tmp,0.003):
        returnMi0
    j=tmp
    while( not(prec(tmp,j,0.003))):
        j=tmp
        Meqmr=Mequipage(Npax)+Marchande(Npax)
        k=1-Mcarb_M0(R,g,Cs,V,f)-Mvide(tmp)
        tmp=Meqmr/k
    return tmp
    
    
#trueM0(100000,Racm,g,Cs,V,fin(All))