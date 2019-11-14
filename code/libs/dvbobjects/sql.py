import psycopg2


nit_first_loop = []
nit_second_loop = []

print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(
    host="192.168.93.128",
    database="DVBCAST", 
    user="root", 
    password="root")

cur = conn.cursor()

print('PostgreSQL database version:')
cur.execute("SELECT * FROM networks")

rows = cur.fetchall()

for row in rows:
    print (row)


cur.close()

