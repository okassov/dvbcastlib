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


###############
# Network API #
###############


def get_all_networks():
    '''This function return all networks'''
    
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


def get_network(network_object_id):
    '''This function return network with
    getting network_object_id'''

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, network_id FROM networks \
            WHERE id=%s" % network_object_id)
        network = cur.fetchone()
        return network
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_sdt_network(transport_object_id):
    '''This function return network with
    getting transport_object_id for sdt'''

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT network FROM transports \
            WHERE id=%s" % transport_object_id)
        network = cur.fetchone()
        return network
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


#################
# Transport API #
#################


def get_all_transports():
    '''This function return all transports
    of all networks'''
    
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


def get_all_network_transports(network_object_id):
    '''This function return all transports
    of one network'''
    
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, transport_id FROM transports \
            WHERE network=%s" % network_object_id)
        transports = cur.fetchall()
        return transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_transport(transport_object_id):
    '''This function return transport with
    getting transport_object_id'''

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, transport_id FROM transports \
            WHERE id=%s" % transport_object_id)
        transport = cur.fetchone()
        return transport
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close() 


def get_sdt_other_transports(except_transport_object_id):
    '''This function return all transports except
    getting except_transport_object_id in one network.'''

    conn = connect()
    cur = conn.cursor()

    network_object_id = get_sdt_network(except_transport_object_id)[0]

    try:
        cur.execute("SELECT id, transport_id FROM transports \
            WHERE network=%s and id<>%s" % (network_object_id, except_transport_object_id))
        transports = cur.fetchall()
        return transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close() 


###############
# Bouquet API #
###############


def get_all_bouquets():
    '''This function return only active
    DVB tables'''
    
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, bouquet_id, network_id FROM bouquets")
        bouquets = cur.fetchall()
        return bouquets
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_bouquet(bouquet_object_id):
    '''This function return transport with
    getting network_object_id'''

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, bouquet_id, network_id FROM bouquets \
            WHERE id=%s" % bouquet_object_id)
        bouquet = cur.fetchone()
        return bouquet
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close() 