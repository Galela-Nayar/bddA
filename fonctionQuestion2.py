from fonctionQuestion1 import *

def create_vue_population_departement_par_annee(cur):
    cur.execute("""
        CREATE OR REPLACE VIEW population_departement AS
        SELECT d.dep, d.libelle AS departement, 
            SUM(p.p19_pop) AS pop_2019, 
            SUM(p.p13_pop) AS pop_2013,
            SUM(p.p08_pop) AS pop_2008
        FROM departement d
        JOIN commune c ON c.dep = d.dep
        JOIN population_stat p ON p.codgeo = c.com
        WHERE p.codgeo IN (SELECT com FROM commune WHERE dep = d.dep)
        GROUP BY d.dep, d.libelle;
    """)

def create_vue_population_region_par_annee(cur):
    cur.execute("""
        CREATE OR REPLACE VIEW population_region AS
        SELECT r.reg, r.libelle AS region, 
            SUM(p.p19_pop) AS pop_2019, 
            SUM(p.p13_pop) AS pop_2013,
            SUM(p.p08_pop) AS pop_2008
        FROM region r
        JOIN departement d ON d.reg = r.reg
        JOIN commune c ON c.dep = d.dep
        JOIN population_stat p ON p.codgeo = c.com
        WHERE p.codgeo IN (SELECT com FROM commune WHERE dep IN (SELECT dep FROM departement WHERE reg = r.reg))
        GROUP BY r.reg, r.libelle;
    """)

# Vue pour agréger les statistiques par département
def create_vue_stat_departement(cur):
    cur.execute("""
        CREATE OR REPLACE VIEW stat_departement AS
        SELECT d.dep, d.libelle AS departement, 
            SUM(p.p19_pop) AS pop_2019, 
            SUM(p.p13_pop) AS pop_2013,
            SUM(p.p08_pop) AS pop_2008,
            SUM(p.nais1319) AS nais_1319,
            SUM(p.nais0813) AS nais_0813,
            SUM(p.dece1319) AS dece_1319,
            SUM(p.dece0813) AS dece_0813
        FROM departement d
        JOIN commune c ON c.dep = d.dep
        JOIN population_stat p ON p.codgeo = c.com
        GROUP BY d.dep, d.libelle;
    """)


# Vue pour agréger les statistiques par région
def create_vue_stat_region(cur):
    cur.execute("""
        CREATE OR REPLACE VIEW stat_region AS
        SELECT r.reg, r.libelle AS region, 
            SUM(p.p19_pop) AS pop_2019, 
            SUM(p.p13_pop) AS pop_2013,
            SUM(p.p08_pop) AS pop_2008,
            SUM(p.nais1319) AS nais_1319,
            SUM(p.nais0813) AS nais_0813,
            SUM(p.dece1319) AS dece_1319,
            SUM(p.dece0813) AS dece_0813
        FROM region r
        JOIN departement d ON d.reg = r.reg
        JOIN commune c ON c.dep = d.dep
        JOIN population_stat p ON p.codgeo = c.com
        GROUP BY r.reg, r.libelle;
    """)


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