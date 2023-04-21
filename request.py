def rowsToString(rows, indices):
    page=''
    for d in rows:
        line = ' | '.join([f"{col}: {d[col]}" for col in d.keys()])
        page += '\n' + line + '\n'
    return page

#liste des departements de la region données en 2 eme parametre
def list_departements_region(cur, region_num):
    cur.execute("""
        SELECT d.dep, d.libelle
        FROM region r, departement d
        WHERE r.reg = d.reg AND r.reg = %s;
    """, (region_num,))
    rows = cur.fetchall()
    if len(rows) == 0:
        print(f"Aucun département trouvé pour la région {region_num}.")
    else:
        res = rowsToString(rows, [0,1])
        print(res)

#liste des communes de plus de X habitants (parametre 3) d'un département donné (parametre 2)
def listComDepPopMin(cur, departement_num, population_min):
    cur.execute("""
        SELECT c.com, c.libelle, p.p19_pop
        FROM commune c, population_stat p
        WHERE c.com = p.codgeo AND c.dep = %s AND p.p19_pop >= %s
        ORDER BY p.p19_pop DESC;
    """, (departement_num, population_min))
    rows = cur.fetchall()
    if len(rows) == 0:
        print(f"Aucune commune trouvée pour le département {departement_num} ayant une population supérieure ou égale à {population_min}.")
    else:
        res = rowsToString(rows, [0,1,3])
        print(res)


def region_plus_peuplee(cur):
    cur.execute("""
        SELECT r.libelle, SUM(p.p19_pop) AS population
        FROM region r
        INNER JOIN departement d ON r.reg = d.reg
        INNER JOIN commune c ON d.dep = c.dep
        INNER JOIN population_stat p ON c.com = p.codgeo
        GROUP BY r.libelle
        ORDER BY population DESC
        LIMIT 1;
    """)
    row = cur.fetchone()
    print(f"La région la plus peuplée de france est {row['libelle']} avec une population totale de {row['population']} habitants.")


def region_moins_peuplee(cur):
    cur.execute("""
        SELECT r.libelle, SUM(p.p19_pop) AS population
        FROM region r
        INNER JOIN departement d ON r.reg = d.reg
        INNER JOIN commune c ON d.dep = c.dep
        INNER JOIN population_stat p ON c.com = p.codgeo
        GROUP BY r.libelle
        ORDER BY population ASC
        LIMIT 1;
    """)
    row = cur.fetchone()
    print(f"La région la moins peuplée de france est {row['libelle']} avec une population totale de {row['population']} habitants.")


def affiche_statistique_par_region(cur, region=None):
    if region is None:
        # Si aucune région n'est spécifiée, on récupère les valeurs pour toutes les régions
        cur.execute(f"SELECT * FROM stat_region;")
    else:
        # Sinon, on récupère les valeurs pour la région spécifiée
        cur.execute(f"SELECT * FROM stat_region WHERE reg = '{region}';")
    
    rows = cur.fetchall()    
    if len(rows) == 0:
        print(f"Pas de statistique trouvé pour la région {region}")
    else:
        res = rowsToString(rows, [0,1,3])
        print(res)

def affiche_statistique_par_departement(cur, departement=None):
    if departement is None:
        # Si aucun département n'est spécifié, on récupère les valeurs pour tous les départements
        cur.execute(f"SELECT * FROM stat_departement;")
    else:
        # Sinon, on récupère les valeurs pour le département spécifié
        cur.execute(f"SELECT * FROM stat_departement WHERE dep = '{departement}';")
    
    rows = cur.fetchall()    
    if len(rows) == 0:
        print(f"Pas de statistique trouvé pour le département {departement}")
    else:
        res = rowsToString(rows, [0,1,3])
        print(res)