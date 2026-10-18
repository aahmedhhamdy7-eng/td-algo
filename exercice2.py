# Exercice 2 - Problème de transport : recherche taboue

# ---- 1. Données ----
COUT = [[5, 3, 4],      # coût de D1 vers M1, M2, M3
        [6, 7, 2]]      # coût de D2 vers M1, M2, M3

def cout_total(x):
    return sum(COUT[i][j] * x[i][j] for i in range(2) for j in range(3))

# ---- 2. Un mouvement = changer un peu les livraisons ----
def appliquer(x, mv):
    j1, j2 = mv
    y = [ligne[:] for ligne in x]    # on copie x
    y[0][j1] += 1                    # +1 container de D1 vers Mj1
    y[1][j2] += 1                    # +1 container de D2 vers Mj2
    y[0][j2] -= 1                    # -1 container de D1 vers Mj2
    y[1][j1] -= 1                    # -1 container de D2 vers Mj1
    return y

def mouvements_possibles(x):
    liste = []
    for j1 in range(3):
        for j2 in range(3):
            if j1 != j2 and x[0][j2] >= 1 and x[1][j1] >= 1:   # pas de quantité négative
                liste.append((j1, j2))
    return liste

# ---- 3. Recherche taboue ----
def recherche_taboue(x, nb_iter=8, duree=2):
    meilleur = x
    tabou = {}                       # mouvement interdit -> dernière itération d'interdiction
    for it in range(1, nb_iter + 1):
        choix = None
        for mv in mouvements_possibles(x):
            y = appliquer(x, mv)
            interdit = tabou.get(mv, 0) >= it
            if interdit and cout_total(y) >= cout_total(meilleur):
                continue             # mouvement tabou et pas meilleur que le record : on l'ignore
            if choix is None or cout_total(y) < cout_total(choix[1]):
                choix = (mv, y)      # meilleur voisin trouvé jusqu'ici
        mv, x = choix                # on se déplace vers le meilleur voisin
        tabou[(mv[1], mv[0])] = it + duree    # on interdit le mouvement inverse
        if cout_total(x) < cout_total(meilleur):
            meilleur = x
        print(f"it {it}: +1 sur D1->M{mv[0]+1} et D2->M{mv[1]+1} | x = {x} | coût = {cout_total(x)}")
    return meilleur

# ---- 4. Lancement ----
if _name_ == "_main_":
    x0 = [[4, 4, 0],        # solution de départ (coin Nord-Ouest)
          [0, 1, 8]]
    print("départ : x =", x0, "| coût =", cout_total(x0))
    best = recherche_taboue(x0)
    print("\nMeilleure solution :", best, "| coût =", cout_total(best))