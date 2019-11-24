import psycopg2
from .db_connect import connect

def main():
    conn = connect()

    cur = conn.cursor()

    cur.execute("SELECT * FROM service_list_descriptor;")

    result = cur.fetchall()

    print (result)

main()