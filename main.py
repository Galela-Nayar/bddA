import psycopg2
import psycopg2.extras
from config import *
import csv

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


def sqlRequest(conn, cur, cmd):
    try:
        cur.execute("""
        %s
        """,(cmd))
    except Exception as e:
        cur.close()
        conn.close()
        exit("error when try to get : " + cmd + "e: " + str(e))


def fillTable(file, table, cur, columns, sep=';'):
    with open(file, 'r') as csvfile:
        try:
            cur.copy_from(csvfile, table, sep=sep, columns=columns)
        except Exception as e:
            exit("copy_from exception : "+str(e))


def rowsToString(rows, indices):
    page=''
    for d in rows:
        line = ' | '.join([str(d[i]) for i in indices])
        page += line + '\n'
    return page
    


if __name__ == "__main__":
    conn = connectBdd(NAMEBDD, USERBDD, PASSWORDBDD)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #creation des tables
    sqlScript(conn, cur, 'sql_file/create_table.sql')

    #remplissage des tables
    fillTable('csv_file/region.csv', "region", cur, ['reg', 'libelle'], sep=',')
    fillTable('csv_file/commune.csv', "commune", cur, ['com', 'dep', 'libelle'], sep=',')
    fillTable('csv_file/departement.csv', "departement", cur, ['dep', 'reg', 'libelle'], sep=',')
    fillTable('csv_file/chefLieuRegion.csv', "chef_lieu_region", cur, ['reg', 'chef_lieu'], sep=',')
    fillTable('csv_file/chefLieuDepartement.csv', "chef_lieu_departement", cur, ['dep', 'chef_lieu'], sep=',')

    #affiche les region
    cur.execute("select * from region;")
    rows = cur.fetchall()
    res = rowsToString(rows, [0,1])
    print(res)

    # affiche les commune
    cur.execute("select * from commune;")
    rows = cur.fetchall()
    res = rowsToString(rows, [0,1,2])
    print(res)

    #affiche les departements
    print("\n")
    cur.execute("select * from departement;")
    rows = cur.fetchall()
    res = rowsToString(rows, [0,1,2])
    print(res)

    #affiche les chef lieu de region
    cur.execute("select * from chef_lieu_region;")
    rows = cur.fetchall()
    res = rowsToString(rows, [0,1])
    print(res)

    #affiche les chef lieu de de departement
    cur.execute("select * from chef_lieu_departement;")
    rows = cur.fetchall()
    res = rowsToString(rows, [0,1])
    print(res)

    

    sqlScript(conn, cur, 'sql_file/delete_table.sql')
    conn.close