import psycopg2
from .db_connect import connect


def get_all_networks():
    '''This function return only active
    DVB tables'''
    
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, network_id FROM networks")
        networks = cur.fetchall()
        return networks
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_all_transports():
    '''This function return only active
    DVB tables'''
    
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, transport_id FROM transports")
        transports = cur.fetchall()
        return transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_all_bouquets():
    '''This function return only active
    DVB tables'''
    
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, bouquet_id, network_id FROM bats")
        bouquets = cur.fetchall()
        return bouquets
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()