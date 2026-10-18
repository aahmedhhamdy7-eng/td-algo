# Exercice 3 - Voyageur de commerce : recherche taboue et recuit simulé
import math, random

# ---- 1. Données ----
ROUTES = {(1, 2): 14, (1, 3): 15, (1, 8): 17,
          (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
          (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
          (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
          (5, 6): 15, (5, 7): 18, (6, 7): 9, (7, 8): 13}

def distance(a, b):
    return ROUTES.get((a, b)) or ROUTES.get((b, a)) or 100   # 100 = route inexistante

def longueur(tour):
    return sum(distance(tour[i], tour[(i + 1) % 8]) for i in range(8))

def deplacer(tour, p, q):        # retire la ville en position p et la remet en position q
    t = tour[:]
    ville = t.pop(p)
    t.insert(q, ville)
    return t

def texte(tour):
    return "-".join(map(str, tour + [tour[0]]))

# ---- 2. Recherche taboue ----
def recherche_taboue(depart, nb_iter=8, duree=3):
    courant = meilleur = depart
    tabou = {}                   # ville interdite -> dernière itération d'interdiction
    for it in range(1, nb_iter + 1):
        choix = None
        for p in range(1, 8):            # la ville 1 (position 0) ne bouge pas
            for q in range(1, 8):
                if p == q:
                    continue
                voisin = deplacer(courant, p, q)
                ville = courant[p]
                interdit = tabou.get(ville, 0) >= it
                if interdit and longueur(voisin) >= longueur(meilleur):
                    continue             # tabou et pas meilleur que le record : on ignore
                if choix is None or longueur(voisin) < longueur(choix[0]):
                    choix = (voisin, ville)
        courant, ville = choix           # on prend le meilleur voisin
        tabou[ville] = it + duree        # cette ville ne bouge plus pendant 'duree' itérations
        if longueur(courant) < longueur(meilleur):
            meilleur = courant
        print(f"it {it}: ville {ville} déplacée | {texte(courant)} | longueur = {longueur(courant)}")
    return meilleur

# ---- 3. Recuit simulé ----
def recuit_simule(depart, temperatures, graine=3):
    random.seed(graine)                  # même résultat à chaque exécution
    courant = meilleur = depart
    for k, T in enumerate(temperatures, start=1):
        p, q = random.sample(range(1, 😎, 2)         # voisin au hasard
        voisin = deplacer(courant, p, q)
        delta = longueur(voisin) - longueur(courant)
        if delta <= 0:                               # voisin meilleur : on accepte toujours
            proba, u, accepte = 1, None, True
        else:                                        # voisin moins bon : on accepte parfois
            proba = math.exp(-delta / T)
            u = random.random()
            accepte = u < proba
        if accepte:
            courant = voisin
        if longueur(courant) < longueur(meilleur):
            meilleur = courant
        print(f"it {k}: T={T} | voisin {texte(voisin)} ({longueur(voisin)}) | delta={delta:+d} | "
              f"p={proba:.3f} | u={'-' if u is None else f'{u:.3f}'} | "
              f"{'accepté' if accepte else 'rejeté'} | courant = {longueur(courant)}")
    return meilleur

# ---- 4. Lancement ----
if _name_ == "_main_":
    depart = [1, 2, 3, 4, 5, 6, 7, 8]
    print("Départ :", texte(depart), "| longueur =", longueur(depart))

    print("\n=== Recherche taboue ===")
    best = recherche_taboue(depart)
    print("Meilleur circuit :", texte(best), "| longueur =", longueur(best))

    print("\n=== Recuit simulé (5 itérations) ===")
    best = recuit_simule(depart, [20, 15, 10, 5, 2])
    print("Meilleur circuit :", texte(best), "| longueur =", longueur(best))