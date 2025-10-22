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
    
    

#print(trueM0(100000,Racm,g,Cs,V,fin(All)))

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
#M0=(trueM0_ddim(100000,Racm,g,Cs,V,fin(All),All,RapPousPoids,ChargeAllaire,Macmax))
#print(M0)

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
    return lf/rap

def Xvoil(lf):

    return lf/3


#empennage conventionnel

#empennage horizontal
allemph = 4
effemph = 0.6
flecheemph = 24.434520 + 5
epaisseurrelativeh = eprel
#empennage vertical
allempv = 1.6
effempv = 0.6
flecheempv = 40
epaisseurrelativev = eprel


#positionnement et dimension de l'empennage
C_EH_DEFAULT = 1.00
C_EV_DEFAULT = 0.09

def compute_empennages(M0, All, eff_wing, Fleche_deg,
                       c_EH=C_EH_DEFAULT, c_EV=C_EV_DEFAULT,
                       use_tail_chord_equal_MAC=True,
                       tol=1e-3, max_iter=50):
    """
    Calcule la géométrie de l'aile et des empennages en ajustant L_EH
    pour que le bord de fuite de l'empennage horizontal soit positionné
    exactement à l'extrémité arrière du fuselage.

    Hypothèses :
      - Sref = M0 / ChargeAllaire (comme dans envergure)
      - L'empennage horizontal utilise la même MAC que l'aile
        si use_tail_chord_equal_MAC == True
      - La flèche et l'effilement sont ceux de l'aile (simplification)
    """

    # Surface de référence
    Sref = M0 / ChargeAllaire

    # Géométrie de l'aile
    b = envergure(M0, All)
    Cempl = CordeEmplanture(Sref, b, eff_wing)
    MAC = CordeAM(eff_wing, Cempl)

    # Position de la voilure
    lf = longueurf(M0)              # longueur totale du fuselage
    x_voil = Xvoil(lf)              # position de la voilure depuis le nez
    ycam = YCam(b, eff_wing)
    x_cam_rel = Xcam(ycam, Fleche_deg)
    x_wing_quarter = x_voil + x_cam_rel

    # Choix de la corde de l'empennage
    MAC_tail = MAC if use_tail_chord_equal_MAC else MAC  # (placeholder)

    # Estimation initiale du bras de levier (40 % de la longueur du fuselage)
    L_EH = 0.4 * lf

    # Boucle d'ajustement
    for _ in range(max_iter):
        S_EH = (c_EH * Sref * MAC) / L_EH
        x_tail_quarter = x_wing_quarter + L_EH
        x_bord_fuite = x_tail_quarter + 0.25 * MAC_tail
        erreur = lf - x_bord_fuite
        if abs(erreur) < tol:
            break
        L_EH += 0.5 * erreur 
    S_EV = (c_EV * Sref * MAC) / L_EH

    # Résultats finaux
    res = {
        "Sref": Sref,
        "b": b,
        "Cemplanture": Cempl,
        "MAC": MAC,
        "x_voil": x_voil,
        "x_wing_quarter": x_wing_quarter,
        "lf": lf,
        "x_tail_quarter": x_tail_quarter,
        "L_EH": L_EH,
        "S_EH": S_EH,
        "S_EV": S_EV,
        "c_EH": c_EH,
        "c_EV": c_EV,
        "iterations": _ + 1,
        "erreur_finale": erreur
    }

    # Vérification de cohérence
    if L_EH <= 0:
        raise ValueError("L_EH calculé <= 0 : vérifie les hypothèses (fuselage trop court ou positions).")

    return res


# Fonction d'affichage pratique
def print_empennage_report(res):
    print("=== Résultats empennage ===")
    print(f"S_ref (surface aile estimée) : {res['Sref']:.3f} m²")
    print(f"Envergure b : {res['b']:.3f} m")
    print(f"Corde d'emplanture : {res['Cemplanture']:.3f} m")
    print(f"MAC (moyenne aérodynamique) : {res['MAC']:.3f} m")
    print(f"Position 1/4 CAM aile (depuis nez) : {res['x_wing_quarter']:.3f} m")
    print(f"Longueur fuselage lf : {res['lf']:.3f} m")
    print(f"Position 1/4 CAM empennage (visée) : {res['x_tail_quarter']:.3f} m")
    print(f"Bras de levier L_EH : {res['L_EH']:.3f} m")
    print(f"Surface empennage horizontal S_EH (c_EH={res['c_EH']}) : {res['S_EH']:.3f} m²")
    print(f"Surface empennage vertical S_EV (c_EV={res['c_EV']}) : {res['S_EV']:.3f} m²")
    print("===========================")

All_used = All  # allongement
eff_wing = Eff
Fleche_deg = Fleche

#res = compute_empennages(M0, All_used, eff_wing, Fleche_deg)
#print_empennage_report(res)

#dimension moteur
def LongeurMoteur(M0,rpp,macmax):
    P=poussee(M0,rpp)
    return 0.49*(P**0.4)*macmax

def diametreMoteur(M0,rpp,macmax,e):
    P=poussee(M0,rpp)
    return 0.15*(P**0.5)*macmax*(exp(0.04*6)) #BPR=6

def Diametrenacelle(Dmoteur):
    return 1.10*Dmoteur

def Longueurentreeair(Dmoteur):
    return 0.6*Dmoteur

def LongueurTot(Lmot,Lentreeair):
    return Lmot+Lentreeair



def main():
    print("\n==================== CALCUL DES CARACTÉRISTIQUES DE L’AVION ====================\n")

    # === MASSE ===
    M0 = trueM0_ddim(100000, Racm, g, Cs, V, fin(All), All, RapPousPoids, ChargeAllaire, Macmax)
    M_equipage = Mequipage(Npax)
    M_marchande = Marchande(Npax)
    M_vide = Mvide_M0_ddim(All, RapPousPoids, ChargeAllaire, Macmax, M0) * M0
    M_carb = M0 - (M_equipage + M_marchande + M_vide)

    print("=== MASSE ===")
    print(f"Masse maximale au décollage (M0) : {M0:,.1f} kg")
    print(f"Masse à vide : {M_vide:,.1f} kg")
    print(f"Masse marchande : {M_marchande:,.1f} kg")
    print(f"Masse équipage : {M_equipage:,.1f} kg")
    print(f"Masse carburant estimée : {M_carb:,.1f} kg\n")

    # === VOILURE ===
    Sref = M0 / ChargeAllaire
    b = envergure(M0, All)
    Cempl = CordeEmplanture(Sref, b, Eff)
    Csaumon = CordeSaumon(Eff, Cempl)
    Cam = CordeAM(Eff, Cempl)
    Y_cam = YCam(b, Eff)
    X_cam = Xcam(Y_cam, Fleche)

    print("=== VOILURE ===")
    print(f"Surface de référence Sref : {Sref:.3f} m²")
    print(f"Envergure b : {b:.3f} m")
    print(f"Corde d’emplanture : {Cempl:.3f} m")
    print(f"Corde de saumon : {Csaumon:.3f} m")
    print(f"Corde aérodynamique moyenne (CAM) : {Cam:.3f} m")
    print(f"Position du centre aérodynamique moyen (Xcam) : {X_cam:.3f} m\n")

    # === FUSELAGE ===
    Lf = longueurf(M0)
    Df = Diamf(Lf, 10.5)  # rapport longueur/diamètre ≈ 10.5
    X_voil = Xvoil(Lf)

    print("=== FUSELAGE ===")
    print(f"Longueur du fuselage : {Lf:.3f} m")
    print(f"Diamètre du fuselage : {Df:.3f} m")
    print(f"Position de la voilure : {X_voil:.3f} m\n")

    # === EMPENNAGES ===
    emp = compute_empennages(M0, All, Eff, Fleche)
    print_empennage_report(emp)

    # === MOTEUR ===
    Lmot = LongeurMoteur(M0, RapPousPoids, Macmax)
    Dmot = diametreMoteur(M0, RapPousPoids, Macmax, eprel)
    Dnac = Diametrenacelle(Dmot)
    Lentree = Longueurentreeair(Dmot)
    Ltot = LongueurTot(Lmot, Lentree)
    Pouss = poussee(M0, RapPousPoids)

    print("=== GROUPE MOTOPROPULSEUR ===")
    print(f"Poussée totale : {Pouss:,.1f} N")
    print(f"Longueur moteur : {Lmot:.3f} m")
    print(f"Diamètre moteur : {Dmot:.3f} m")
    print(f"Diamètre nacelle : {Dnac:.3f} m")
    print(f"Longueur entrée d’air : {Lentree:.3f} m")
    print(f"Longueur totale moteur + entrée d’air : {Ltot:.3f} m\n")

    print("==================== FIN DU RAPPORT ====================\n")

    # === Regrouper toutes les valeurs dans un dictionnaire pour réutilisation ===
    caract = {
        "M0": M0,
        "M_equipage": M_equipage,
        "M_marchande": M_marchande,
        "M_vide": M_vide,
        "M_carb": M_carb,
        "voilure": {
            "Sref": Sref,
            "b": b,
            "Cempl": Cempl,
            "Csaumon": Csaumon,
            "Cam": Cam,
            "X_cam": X_cam
        },
        "fuselage": {
            "Lf": Lf,
            "Df": Df,
            "X_voil": X_voil
        },
        "empennages": emp,
        "moteur": {
            "Pouss": Pouss,
            "Lmot": Lmot,
            "Dmot": Dmot,
            "Dnac": Dnac,
            "Lentree": Lentree,
            "Ltot": Ltot
        }
    }

    return caract

tab=main()

    
