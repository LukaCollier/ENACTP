from math import *
from random import randint
Mach=0.77
Macmax=0.8085
Npax= 185
Raction= 3250  #Nm
Alt= 330 #FL330
All =9 #dimension de l'allongement majoritairement utilisée dans l'aéronautique voircours SA1
AllA320 = 9.29
Cs=14.1e-6
Racm=6.019e6
g=9.81
V=Mach*299
RapPousPoids=0.31
ChargeAllaire=586

def degtorad(d):
    return d*2*pi/360

#carac aile
Fleche=24.434520 #degre
Eff =0.23
eprel = 13.9 # en %
Vril = 3 # en degre
Cal= 1 # en degre
diedre =5 #en degre

#seance 1 / calcul M0
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
    return 1.06*(1- 0.995*0.985*0.970*M3_M2(R,g,Cs,V,f)) #0.985=M2/M1


def allongementrandom(n):
    res=[randint(7,11) for i in range(n)]
    return sum(res)/len(res)

def Allongement(*g):
    pass

def fin(al):
    '''
    finesse de l'avion en croissière
    '''
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
    
    

print(trueM0(100000,Racm,g,Cs,V,fin(All)))

def M2_M1_ddim(Mac):
    return 1.0065-0.0325*Mac
def Mcarb_M0_ddim(R,g,Cs,V,f):
    return 1.06*(1- 0.995*M2_M1_ddim(Mach)*0.970*M3_M2(R,g,Cs,V,f))

def Mvide_M0_ddim(al,rpp,CA,Machmax,M0):
    return 0.32+0.6446*(M0**(-0.13))*(al**0.3)*(rpp**0.06)*(CA**(-0.05))*(Machmax**0.05)

def trueM0_ddim(Mi0,R,g,Cs,V,f,al,rpp,CA,Machmax):
    Meqmr=Mequipage(Npax)+Marchande(Npax)
    k=1-Mcarb_M0_ddim(R,g,Cs,V,f)-Mvide_M0_ddim(al,rpp,CA,Machmax,Mi0)
    tmp=Meqmr/k
    if prec(Mi0,tmp,0.003):
        returnMi0
    j=tmp
    while( not(prec(tmp,j,0.003))):
        j=tmp
        Meqmr=Mequipage(Npax)+Marchande(Npax)
        k=1-Mcarb_M0_ddim(R,g,Cs,V,f)-Mvide_M0_ddim(al,rpp,CA,Machmax,tmp)
        tmp=Meqmr/k
    return tmp
M0=(trueM0_ddim(100000,Racm,g,Cs,V,fin(All),All,RapPousPoids,ChargeAllaire,Macmax))
print(M0)

# Geometrie de la voilure
def envergure(M0,al):#b
    Sref=M0/ChargeAllaire
    return sqrt(al*Sref)


def CordeEmplanture(sref,b,eff): #Cemplanture
    return (2*sref)/(b*(1+eff))

def CordeSaumon(eff,Cemplanture):
    return eff*Cemplanture

def CordeAM(eff,Cemplanture) : #Cam
    return (2/3)*Cemplanture*(1+eff*(1+eff))/(1+eff)

def YCam(b,eff):
    return (b/6)*(1+2*eff)/(1+eff)

def Xcam(ycam,fleche):
    return ycam*tan(degtorad(fleche))

#Poussée

def poussee(M0,rpp):
    return M0*g*rpp

#fuselage

def longueurf(M0):
    return 0.287*(M0**0.43)

def Diamf(lf,rap): #choix rapport 10.5
    return rap/lf

def Xvoil(lf):

    return lf/3
