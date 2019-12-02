import psycopg2
from .db_connect import connect


def get_active_dvb_tables():
    '''This function return only active
    DVB tables'''
    
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT dvb_table FROM dvb_active_tables \
            WHERE is_active=%s" % True)
        dvb_tables = cur.fetchall()
        return dvb_tables
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

