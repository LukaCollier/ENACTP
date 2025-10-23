from math import *
from random import randint

# ---------------- Paramètres ----------------
Mach = 0.77
Macmax = 0.8085
Npax = 185
Raction = 3250  # Nm (valeur utilisée dans formules de consommation)
Alt = 330  # FL330
All = 9  # allongement de l'aile
AllA320 = 9.29
Cs = 14.1e-6
Racm = 6.019e6
g = 9.81
V = Mach * 299
RapPousPoids = 0.31
ChargeAllaire = 586

def degtorad(d):
    return d * 2 * pi / 360

# ---- caractéristiques aile ----
Fleche = 24.434520  # deg
Eff = 0.23
eprel = 13.9  # %
Vril = 3  # deg
Cal = 1  # deg
diedre = 5  # deg

# ---- empennage par défaut ----
allemph = 4.0
effemph = 0.6
flecheemph = 29.434520
epaisseurrelativeh = eprel

allempv = 2.0        # augmenté (recommandé)
effempv = 0.6
flecheempv = 40
epaisseurrelativev = eprel

# coefficients de volume par défaut (ajuster si besoin)
C_EH_DEFAULT = 1.00
C_EV_DEFAULT = 0.09   # augmenté de 0.09 -> 0.12 (valeur réaliste pour monocouloir)

# ---------------- Fonctions utilitaires / masse ----------------
def PNC(pax):
    return ceil(pax / 50)

def Mequipage(pax):
    return (PNC(pax) + 2) * 100

def Marchande(pax):
    return pax * 100

def Mvide(M0):
    return 0.97 * (M0 ** (-0.06))

def M3_M2(R, g_, Cs_, V_, f):
    val = - (R * g_ * Cs_) / (V_ * f)
    return exp(val)

def Mcarb_M0(R, g_, Cs_, V_, f):
    return 1.06 * (1 - 0.995 * 0.985 * 0.970 * M3_M2(R, g_, Cs_, V_, f))

def allongementrandom(n):
    res = [randint(7, 11) for i in range(n)]
    return sum(res) / len(res)

def Allongement(*g):
    pass

def fin(al):
    # finesse de l'avion en croisière
    return ((0.866 * 15.5) / sqrt(6)) * sqrt(al)

def prec(n, m, e):
    return abs(n - m) < e

def trueM0(Mi0, R, g_, Cs_, V_, f):
    Meqmr = Mequipage(Npax) + Marchande(Npax)
    k = 1 - Mcarb_M0(R, g_, Cs_, V_, f) - Mvide(Mi0)
    tmp = Meqmr / k
    if prec(Mi0, tmp, 0.003):
        return Mi0
    j = tmp
    while not prec(tmp, j, 0.003):
        j = tmp
        Meqmr = Mequipage(Npax) + Marchande(Npax)
        k = 1 - Mcarb_M0(R, g_, Cs_, V_, f) - Mvide(tmp)
        tmp = Meqmr / k
    return tmp

# version dimensionnelle
def M2_M1_ddim(Mac):
    return 1.0065 - 0.0325 * Mac

def Mcarb_M0_ddim(R, g_, Cs_, V_, f):
    return 1.06 * (1 - 0.995 * M2_M1_ddim(Mach) * 0.970 * M3_M2(R, g_, Cs_, V_, f))

def Mvide_M0_ddim(al, rpp, CA, Machmax, M0):
    return 0.32 + 0.6446 * (M0 ** (-0.13)) * (al ** 0.3) * (rpp ** 0.06) * (CA ** (-0.05)) * (Machmax ** 0.05)

def trueM0_ddim(Mi0, R, g_, Cs_, V_, f, al, rpp, CA, Machmax):
    Meqmr = Mequipage(Npax) + Marchande(Npax)
    k = 1 - Mcarb_M0_ddim(R, g_, Cs_, V_, f) - Mvide_M0_ddim(al, rpp, CA, Machmax, Mi0)
    tmp = Meqmr / k
    if prec(Mi0, tmp, 0.003):
        return Mi0
    j = tmp
    while not prec(tmp, j, 0.003):
        j = tmp
        Meqmr = Mequipage(Npax) + Marchande(Npax)
        k = 1 - Mcarb_M0_ddim(R, g_, Cs_, V_, f) - Mvide_M0_ddim(al, rpp, CA, Machmax, tmp)
        tmp = Meqmr / k
    return tmp

# ---------------- Géométrie voilure ----------------
def envergure(M0, al):
    Sref = M0 / ChargeAllaire
    return sqrt(al * Sref)

def CordeEmplanture(sref, b, eff):
    return (2 * sref) / (b * (1 + eff))

def CordeSaumon(eff, Cemplanture):
    return eff * Cemplanture

def CordeAM(eff, Cemplanture):
    return (2 / 3) * Cemplanture * (1 + eff + eff ** 2) / (1 + eff)  # correction formule (1+eff+eff^2)

def YCam(b, eff):
    return (b / 6) * (1 + 2 * eff) / (1 + eff)

def Xcam(ycam, fleche):
    return ycam * tan(degtorad(fleche))

# ---------------- Poussée / fuselage ----------------
def poussee(M0, rpp):
    # poussée totale N (P = M0*g*rpp)
    return M0 * g * rpp

def longueurf(M0):
    return 0.287 * (M0 ** 0.43)

def Diamf(lf, rap):
    return lf / rap

def Xvoil(lf):
    return lf / 3

# ---------------- Empennages (corrigé) ----------------
def compute_empennages(M0, All, eff_wing, Fleche_deg,
                       c_EH=C_EH_DEFAULT, c_EV=C_EV_DEFAULT,
                       AR_EH=allemph, AR_EV=allempv,
                       eff_eh=effemph, eff_ev=effempv,
                       fleche_eh=flecheemph, fleche_ev=flecheempv,
                       L_EV_factor=1.2,
                       tol=1e-3, max_iter=50):
    """
    Calcule la géométrie aile + empennages.
    Corrections appliquées :
     - S_EV calculée en utilisant l'envergure b (et non le MAC aile)
     - L_EV = L_EH * L_EV_factor (bras de levier pour EV), car bras pour lacet diffère
     - calcul des envergures et cordes des empennages via AR et effilement
    """

    # surface et géométrie aile
    Sref = M0 / ChargeAllaire
    b = envergure(M0, All)
    Cempl = CordeEmplanture(Sref, b, eff_wing)
    MAC = CordeAM(eff_wing, Cempl)

    # position voilure
    lf = longueurf(M0)
    x_voil = Xvoil(lf)
    ycam = YCam(b, eff_wing)
    x_cam_rel = Xcam(ycam, Fleche_deg)
    x_wing_quarter = x_voil + x_cam_rel

    # estimation initiale L_EH (bras 1/4 aile -> 1/4 empennage horizontal)
    L_EH = 0.4 * lf
    for _ in range(max_iter):
        # surface EH via coefficient de volume (standard)
        S_EH = (c_EH * Sref * MAC) / L_EH
        # position 1/4 empennage
        x_tail_quarter = x_wing_quarter + L_EH
        # on veut que le bord de fuite de l'empennage se situe à la fin du fuselage :
        # x_bord_fuite = x_tail_quarter + 0.25 * MAC_tail
        # on choisit MAC_tail = MAC (approx) si use_tail_chord_equal_MAC implicite
        MAC_tail = MAC
        x_bord_fuite = x_tail_quarter + 0.25 * MAC_tail
        erreur = lf - x_bord_fuite
        if abs(erreur) < tol:
            break
        L_EH += 0.5 * erreur

    # Bras de levier pour EV (plus long en général) :
    L_EV = L_EH * L_EV_factor

    # SURFACES : EV doit utiliser b (envergure) pour le volume vertical
    S_EV = (c_EV * Sref * b) / L_EV

    # Calcul des envergures des empennages à partir des AR
    b_EH = sqrt(AR_EH * S_EH)
    b_EV = sqrt(AR_EV * S_EV)

    # Cordes (approche trapezoïdale avec taper = eff)
    Cempl_EH = (2 * S_EH) / (b_EH * (1 + eff_eh))
    Csaumon_EH = eff_eh * Cempl_EH
    MAC_EH = (2 / 3) * Cempl_EH * (1 + eff_eh + eff_eh ** 2) / (1 + eff_eh)
    ycam_EH = (b_EH / 6) * (1 + 2 * eff_eh) / (1 + eff_eh)
    xcam_EH = Xcam(ycam_EH, fleche_eh)

    Cempl_EV = (2 * S_EV) / (b_EV * (1 + eff_ev))
    Csaumon_EV = eff_ev * Cempl_EV
    MAC_EV = (2 / 3) * Cempl_EV * (1 + eff_ev + eff_ev ** 2) / (1 + eff_ev)
    ycam_EV = (b_EV / 6) * (1 + 2 * eff_ev) / (1 + eff_ev)
    xcam_EV = Xcam(ycam_EV, fleche_ev)

    # résultat
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
        "L_EV": L_EV,
        "S_EH": S_EH,
        "S_EV": S_EV,
        "b_EH": b_EH,
        "b_EV": b_EV,
        "Cempl_EH": Cempl_EH,
        "Csaumon_EH": Csaumon_EH,
        "MAC_EH": MAC_EH,
        "xcam_EH": xcam_EH,
        "Cempl_EV": Cempl_EV,
        "Csaumon_EV": Csaumon_EV,
        "MAC_EV": MAC_EV,
        "xcam_EV": xcam_EV,
        "c_EH": c_EH,
        "c_EV": c_EV,
        "iterations": _ + 1,
        "erreur_finale": erreur
    }

    if L_EH <= 0:
        raise ValueError("L_EH calculé <= 0 : vérifie les hypothèses")

    return res

# affichage
def print_empennage_report(res):
    print("=== Résultats empennage ===")
    print(f"S_ref (surface aile estimée) : {res['Sref']:.3f} m²")
    print(f"Envergure aile (b) : {res['b']:.3f} m")
    print(f"Corde d'emplanture aile : {res['Cemplanture']:.3f} m")
    print(f"MAC aile : {res['MAC']:.3f} m")
    print(f"Position 1/4 CAM aile (depuis nez) : {res['x_wing_quarter']:.3f} m")
    print(f"Longueur fuselage lf : {res['lf']:.3f} m")
    print(f"Position 1/4 CAM empennage : {res['x_tail_quarter']:.3f} m")
    print(f"Bras de levier L_EH : {res['L_EH']:.3f} m")
    print(f"Bras de levier L_EV : {res['L_EV']:.3f} m")
    print(f"Surface empennage horizontal S_EH (c_EH={res['c_EH']}) : {res['S_EH']:.3f} m²")
    print(f"Envergure EH (b_EH) : {res['b_EH']:.3f} m")
    print(f"Cordes EH : empl={res['Cempl_EH']:.3f} m, saum={res['Csaumon_EH']:.3f} m, MAC_EH={res['MAC_EH']:.3f} m")
    print(f"Surface empennage vertical S_EV (c_EV={res['c_EV']}) : {res['S_EV']:.3f} m²")
    print(f"Hauteur EV (b_EV) : {res['b_EV']:.3f} m")
    print(f"Cordes EV : empl={res['Cempl_EV']:.3f} m, saum={res['Csaumon_EV']:.3f} m, MAC_EV={res['MAC_EV']:.3f} m")
    print("===========================")

# ---------------- Moteur ----------------
def LongeurMoteur(M0, rpp, macmax):
    P = poussee(M0, rpp) / 2
    return 0.49 * (P ** 0.4) * macmax

def diametreMoteur(M0, rpp, macmax, e):
    P = poussee(M0, rpp) / 2
    return 0.15 * (P ** 0.5) * macmax * (exp(0.04 * 6))  # BPR=6

def Diametrenacelle(Dmoteur):
    return 1.10 * Dmoteur

def Longueurentreeair(Dmoteur):
    return 0.6 * Dmoteur

def LongueurTot(Lmot, Lentreeair):
    return Lmot + Lentreeair

# ---------------- Main / rapport ----------------
def main():
    print("\n==================== CALCUL DES CARACTÉRISTIQUES DE L’AVION ====================\n")

    # MASSE
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

    # VOILURE
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
    print(f"CAM : {Cam:.3f} m")
    print(f"Position Xcam : {X_cam:.3f} m\n")

    # FUSELAGE
    Lf = longueurf(M0)
    Df = Diamf(Lf, 10.5)
    X_voil = Xvoil(Lf)

    print("=== FUSELAGE ===")
    print(f"Longueur du fuselage : {Lf:.3f} m")
    print(f"Diamètre du fuselage : {Df:.3f} m")
    print(f"Position de la voilure : {X_voil:.3f} m\n")

    # EMPENNAGES
    emp = compute_empennages(M0, All, Eff, Fleche)
    print_empennage_report(emp)

    # GROUPE MOTOPROPULSEUR
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

# exécution
tab = main()
