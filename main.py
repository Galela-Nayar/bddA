import psycopg2
import psycopg2.extras
from config import *
from requestFunction import *

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

    ################################ question 1 #############################################
    #liste des departements de la region données en 2 eme parametre
    print("liste des departements de la region iles de france")
    list_departements_region(cur, "11")

    #liste des communes de plus de X habitants (parametre 3) d'un département donné (parametre 2)
    print("liste des communes de plus de 25000 habitants du departement de la gironde")
    listComDepPopMin(cur, "33", "25000")

    #la region plus peuplee
    region_plus_peuplee(cur)

    #la region moins peuplee
    region_moins_peuplee(cur)


    ################################ question 2 #############################################



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

    

    sqlScript(conn, cur, 'sql_file/delete_table.sql')
    conn.close