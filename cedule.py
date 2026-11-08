import random



CAPACITES = [20, 15, 35, 40, 15, 15, 10]          # MW par unité
NB_INTERVALLES_MAINT = [2, 2, 1, 1, 1, 1, 1]      # intervalles requis
DEMANDE = [80, 90, 65, 70]                        # MW par intervalle
CAPACITE_TOTALE = sum(CAPACITES)                  # 150 MW

N_UNITES = len(CAPACITES)
N_INTERVALLES = len(DEMANDE)
TAILLE_GENE = N_INTERVALLES                       # 4 bits par gène

# Maintenances possibles par unité (intervalles consécutifs)
MAINT_2_INTERVALLES = [(1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 1)]
MAINT_1_INTERVALLE = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
POSSIBLES = [
    MAINT_2_INTERVALLES if n == 2 else MAINT_1_INTERVALLE
    for n in NB_INTERVALLES_MAINT
]



def creer_chromosome():
   
    chromo = []
    for options in POSSIBLES:
        chromo.extend(random.choice(options))
    return chromo


def gene(chromo, i):
   
    return tuple(chromo[i * TAILLE_GENE:(i + 1) * TAILLE_GENE])


def set_gene(chromo, i, bits):
    chromo[i * TAILLE_GENE:(i + 1) * TAILLE_GENE] = list(bits)


def afficher(chromo):
    return " ".join("".join(map(str, gene(chromo, i))) for i in range(N_UNITES))


# fonction objective
def reserves(chromo):
   
    res = []
    for t in range(N_INTERVALLES):
        p_perdue = sum(
            CAPACITES[u] * chromo[u * TAILLE_GENE + t] for u in range(N_UNITES)
        )
        res.append(CAPACITE_TOTALE - p_perdue - DEMANDE[t])
    return res


def fitness(chromo):
   
    return max(0, min(reserves(chromo)))



#SÉLECTION PAR LOTERIE (roulette wheel)

def selection_loterie(population, fits):
  
    total = sum(fits)
    if total == 0:
        return random.choice(population)[:], random.choice(population)[:]

    def tirer():
        point = random.uniform(0, total)
        cumul = 0.0
        for indiv, f in zip(population, fits):
            cumul += f
            if cumul >= point:
                return indiv[:]
        return population[-1][:]

    return tirer(), tirer()



def croisement(p1, p2, p_croisement):
 
    if random.random() < p_croisement:
        bloc = random.randint(1, N_UNITES - 1)     # point de croisement
        cut = bloc * TAILLE_GENE
        return p1[:cut] + p2[cut:], p2[:cut] + p1[cut:]
    return p1[:], p2[:]


def mutation_inversion(chromo, p_mutation):
    
    for i in range(N_UNITES):
        if random.random() < p_mutation:
            set_gene(chromo, i, gene(chromo, i)[::-1])


def mutation_remplacement(chromo, p_mutation):
    """Remplace un gène par un autre gène valide (exemple du cours)."""
    for i in range(N_UNITES):
        if random.random() < p_mutation:
            courant = gene(chromo, i)
            autres = [o for o in POSSIBLES[i] if o != courant]
            set_gene(chromo, i, random.choice(autres))


def mutation_echange(chromo, p_mutation):
    
    for i in range(N_UNITES):
        if random.random() < p_mutation:
            candidats = [j for j in range(N_UNITES)
                         if j != i and POSSIBLES[j] == POSSIBLES[i]]
            if candidats:
                j = random.choice(candidats)
                gi, gj = gene(chromo, i), gene(chromo, j)
                set_gene(chromo, i, gj)
                set_gene(chromo, j, gi)


MUTATIONS = {
    "inversion": mutation_inversion,
    "remplacement": mutation_remplacement,
    "echange": mutation_echange,
}


#ALGORITHME GÉNÉTIQUE

def algorithme_genetique(
    taille_pop=45,          
    n_generations=100,
    p_croisement=0.8,
    p_mutation=0.1,
    type_mutation="inversion",
    elitisme=True,
    graine=None,
):
    if graine is not None:
        random.seed(graine)
    muter = MUTATIONS[type_mutation]

    population = [creer_chromosome() for _ in range(taille_pop)]
    historique_best, historique_moy = [], []
    meilleur = max(population, key=fitness)[:]

    for _ in range(n_generations):
        fits = [fitness(c) for c in population]

        best_gen = population[fits.index(max(fits))]
        if fitness(best_gen) > fitness(meilleur):
            meilleur = best_gen[:]
        historique_best.append(max(fits))
        historique_moy.append(sum(fits) / len(fits))

        nouvelle = [meilleur[:]] if elitisme else []
        while len(nouvelle) < taille_pop:
            p1, p2 = selection_loterie(population, fits)
            e1, e2 = croisement(p1, p2, p_croisement)
            muter(e1, p_mutation)
            muter(e2, p_mutation)
            nouvelle.extend([e1, e2])
        population = nouvelle[:taille_pop]

    return meilleur, historique_best, historique_moy



# AFFICHAGE / TESTS

def rapport(chromo):
    print("Chromosome :", afficher(chromo))
    res = reserves(chromo)
    for t in range(N_INTERVALLES):
        unites = [u + 1 for u in range(N_UNITES)
                  if chromo[u * TAILLE_GENE + t] == 1]
        print(f"  Intervalle {t + 1} : unités en maintenance {unites or '-'}"
              f" | réserve = {res[t]} MW")
    print("  Performance (plus petite réserve) =", fitness(chromo), "MW")


if _name_ == "_main_":
    
    exemple = [int(b) for b in "0110001100011000010000101000"]
    print("=== Exemple du cours ===")
    rapport(exemple)       

    
    print("\n=== Comparaison des mutations (20 exécutions chacune) ===")
    courbes = {}
    for nom in MUTATIONS:
        scores = []
        for essai in range(20):
            b, hb, hm = algorithme_genetique(type_mutation=nom, graine=essai)
            scores.append(fitness(b))
            if essai == 0:
                courbes[nom] = (hb, hm)
        print(f"{nom:13s}: moyenne = {sum(scores) / len(scores):5.2f} MW"
              f" | meilleur = {max(scores)} MW")

   
    print("\n=== Meilleure cédule (sélection loterie + mutation inversion) ===")
    best, hist_best, hist_moy = algorithme_genetique(
        type_mutation="inversion", graine=42)
    rapport(best)
