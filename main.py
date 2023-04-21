import psycopg2
import psycopg2.extras
from config import *
from fonctionQuestion1 import *
from fonctionQuestion2 import *
from fonctionQuestion3 import *

def connectBdd(nameBdd, userBdd, passwordBdd):
    # Try to connect to an existing database
    print('Connexion à la base de données...')
    try:
        conn = psycopg2.connect("host=localhost dbname="+nameBdd+" user="+userBdd+" password="+passwordBdd)
        return conn
    except Exception as e :
        exit("Connexion impossible à la base de données: " + str(e))



def sqlScript(conn, cur, script_file):
    with open(script_file, 'r') as f:
        sql = f.read()
        cur.execute(sql)
        conn.commit()



#remplis les tables avec le fichier file sur la table "table"
def fillTable(file, table, cur, columns, sep=';'):
    with open(file, 'r') as csvfile:
        try:
            cur.copy_from(csvfile, table, sep=sep, columns=columns)
        except Exception as e:
            exit("copy_from exception : "+str(e))


def saisir_chaine(message):
    chaine = input(message)
    return chaine

if __name__ == "__main__":
    conn = connectBdd(NAMEBDD, USERBDD, PASSWORDBDD)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #creation des tables
    sqlScript(conn, cur, 'sql_file/create_table.sql')

    #remplissage des tables
    fillTable('csv_file/region.csv', "region", cur, ['reg', 'libelle'], sep=',')
    fillTable('csv_file/departement.csv', "departement", cur, ['dep', 'reg', 'libelle'], sep=',')
    fillTable('csv_file/commune.csv', "commune", cur, ['com', 'dep', 'libelle'], sep=',')
    fillTable('csv_file/chefLieuRegion.csv', "chef_lieu_region", cur, ['reg', 'chef_lieu'], sep=',')
    fillTable('csv_file/chefLieuDepartement.csv', "chef_lieu_departement", cur, ['dep', 'chef_lieu'], sep=',')
    fillTable('csv_file/population_stat.csv', "population_stat", cur, ['codgeo', 'p19_pop', 'p13_pop', 'p08_pop', 'nais1319', 'nais0813', 'dece1319', 'dece0813'], sep=',')
    conn.commit()

    ################################ question 1 #############################################
    #liste des departements de la region données (region en 2eme parametre)
    region = saisir_chaine("saisisez la numero de la region pour avoir la listes de ses departement : ")
    print("liste des departements de la region "+region+" :")
    list_departements_region(cur, region)

    #liste des communes de plus de X habitants (parametre 3) d'un département donné (parametre 2)
    print("pour la liste des communes de plus de X habitants du departement Y :")
    x=saisir_chaine("saisisez la population minimum X: ")
    y=saisir_chaine("saisisez le departement Y: ")
    listComDepPopMin(cur, y, x)

    #la region plus peuplee de france
    region_plus_peuplee(cur)

    #la region moins peuplee de france
    region_moins_peuplee(cur)

    print("\n")

    ################################ question 2 #############################################

    #creation des vues
    create_vue_population_departement_par_annee(cur)
    create_vue_population_region_par_annee(cur)
    conn.commit()

    #### pour ces requetes ils prennent un peu plus de temps a cause du grand nombres de données 
    #### avec les jointures.(donc je les laisses commentés a vous de voir si vous voulez les affichés)
    
    ##affiche la population des départements pour les différentes années
    #print("la population des départements sur les différentes années")
    # cur.execute("select * from population_departement;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1])
    # print(res)

    ##affiche la population des régions pour les différentes années
    #print("la population des regions sur les différentes années")
    # cur.execute("select * from population_region;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1])
    # print(res)


    # Vue pour agréger les statistiques par departement
    create_vue_stat_departement(cur)
    # Vue pour agréger les statistiques par région
    create_vue_stat_region(cur)
    conn.commit()

    region = saisir_chaine("saisisez le numero de la region dont vous voulez voir les statistiques :")
    affiche_statistique_par_region(cur, region)

    dep = saisir_chaine("saisisez le numero du departement dont vous voulez voir les statistiques :")
    affiche_statistique_par_departement(cur, dep)




    ################################ question 3 #############################################

    #modification préalable de la structure de la base pour accueillir ces nouvelles informations.
    cur.execute("""
        ALTER TABLE departement ADD COLUMN pop_departement FLOAT;
    """)
    cur.execute("""
        ALTER TABLE region ADD COLUMN pop_region FLOAT;
    """)
    conn.commit()
    maj_pop_dep_reg(cur)
    cur.execute("CALL calcul_pop_departement_region();")
    conn.commit()





    # #affiche les region
    # cur.execute("select * from region;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1])
    # print(res)

    # # affiche les communes
    # cur.execute("select * from commune;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1,2])
    # print(res)

    # #affiche les departements
    # print("\n")
    # cur.execute("select * from departement;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1,2])
    # print(res)

    # #affiche les chef lieu de region
    # cur.execute("select * from chef_lieu_region;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1])
    # print(res)

    # #affiche les chef lieu de de departement
    # cur.execute("select * from chef_lieu_departement;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1])
    # print(res)

    # #affiche les statistiques de la population (2008 a 2019)
    # cur.execute("select * from population_stat;")
    # rows = cur.fetchall()
    # res = rowsToString(rows, [0,1,2,3,4,5,6,7])
    # print(res)

    

    #sqlScript(conn, cur, 'sql_file/delete_table.sql')
    conn.close