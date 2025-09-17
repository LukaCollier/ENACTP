"""
      Utilities for simulation module
"""
__author__ = "conversy"

import math


def min_dist_time(x0, y0, route):
    """ Obtenir la distance minimale d'un point à une route
        et le temps correspondant dans la simu """

    #### Version normale
    # min_dist = 100000
    # rmin_dist_time = -1
    # for index, xy in enumerate(route):
    #     dist = math.hypot(xy.x-x0, xy.y-y0)
    #     if dist < min_dist:
    #         min_dist = dist
    #         rmin_dist_time = index

    # if rmin_dist_time == -1:
    #     return

    #### Version liste en compréhension
    min_dist, rmin_dist_time = min((dist, rtime)
        for (rtime, dist) in enumerate(math.hypot(xy.x - x0, xy.y - y0) for xy in route))

    # On recherche le temps de la simu correspondant au plot le plus proche du curseur.
    # Explication (mettre if True pour afficher les étapes) :
    if False:
        print()
        print(x0, y0)

        # Calcul de distance entre le point courant (x0, y0) et chaque plot de la route du vol
        # (on pourrait optimiser en ne faisant pas de sqrt dans hypot)
        print("step 1", [math.hypot(xy.x - x0, xy.y - y0) for xy in route])
        # Récupération du temps relatif rtime (i.e. l'indice dans la route) de cette distance
        print("step 2",
            [(rtime, dist) for (rtime, dist) in enumerate([math.hypot(xy.x - x0, xy.y - y0) for xy in route])])
        # On va prendre le min des distances, du coup il faut inverser (rtime, dist) en (dist, rtime)
        print("step 3",
            [(dist, rtime) for (rtime, dist) in enumerate(math.hypot(xy.x - x0, xy.y - y0) for xy in route)])
        # On prend le min, et voilà, magique !
        print("step 4",
            min((val, idx) for (idx, val) in enumerate(math.hypot(xy.x - x0, xy.y - y0) for xy in route)))

    return rmin_dist_time
