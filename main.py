import psycopg2
import psycopg2.extras
from config import *
import csv

def connectBdd(nameBdd, userBdd, passwordBdd):
    # Try to connect to an existing database
    print('Connexion à la base de données...')
    try:
        conn = psycopg2.connect("host=pgsql dbname="+nameBdd+" user="+userBdd+" password="+passwordBdd)
        return conn
    except Exception as e :
        exit("Connexion impossible à la base de données: " + str(e))


def fillTable(file, table, cur, columns, sep=';'):
    with open(file, 'r') as csvfile:
        try:
            cur.copy_from(csvfile, table, sep=sep, columns=columns)
        except Exception as e:
            exit("copy_from exception : "+str(e))

def sqlRequest(conn, cur, cmd):
    try:
        cur.execute("""
        %s
        """,(cmd))
    except Exception as e:
        cur.close()
        conn.close()
        exit("error when try to get : " + cmd + "e: " + str(e))

def regionToString(rows):
    page=''
    for d in rows :
        page+= str(d['idregion']) + " : " + str(d['nomregion'])+"\n"
    return page

if __name__ == "__main__":
    print("welcome to postate ...")
    conn = connectBdd(NAMEBDD, USERBDD, PASSWORDBDD)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    fillTable('./csv_file/region.csv', "region", cur, ['idregion', 'nomregion'], sep=',')
    cur.execute("select * from region;")
    rows = cur.fetchall()
    res = regionToString(rows)
    print(res)