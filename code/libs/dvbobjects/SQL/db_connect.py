import psycopg2

def connect():
    '''This function connect to PSQL DB
    and return connection'''

    conn = None

    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="192.168.93.128",
            database="DVBCAST", 
            user="root", 
            password="root")
        return conn
    except:
        print ("Error")