import psycopg2
from .db_connect import connect

def get_dict_key(dictionary):
    '''This function get dict as arg
    and return it's key in string format'''

    for i in dictionary.keys():
        return i


def get_services(conn, transport_id):
    '''This function return services data 
    from services TABLE'''

    cur = conn.cursor()

    try:
        cur.execute("SELECT id, service_id FROM \
            services WHERE transport=%s" % transport_id)
        services = cur.fetchall()
        return services
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptors(conn, transport_id, service_id):
    '''This function return all ACTIVE descriptors that 
    binding for getting service_id and transport_id'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT descriptor_name FROM \
            sdt_loop WHERE transport=%s and \
            service=%s and is_active=%s" % (transport_id, service_id, True))
        active_descriptors = cur.fetchall()
        return active_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptor_data(conn, descriptor_name, transport_id, service_id, dvb_table):
    '''This function return data of getting descriptor'''

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM %s \
            WHERE transport=%s and service=%s \
            and dvb_table='%s'" % (descriptor_name, transport_id, service_id, dvb_table))
        data = cur.fetchall()
        columns = [i[0] for i in cur.description]

        if data != None and len(data) != 0:
            data = list(data[0]) # Modify tuple columns to list
        else:
            data = []

        result = { descriptor_name: dict(zip(columns, data)) }
        return result
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def mapping(conn, transport_id, services):
    '''This function map services and service descriptors 
    to transport. It's get transport_id, list of services with
    data in tupple and descriptors in list as args.
    For example:
    Input transport_id: 1
    Input services: [(service_1_data, ...), (service_2_data, ...), ...]
    Input descriptos: [[{descriptors_service_1}], [{descriptors_service2}], ...]
    
    Output result: 
        {
            "ts" 1, 
            "services": 
            [
                {
                    "id": 1,
                    "service_id": 100,
                    "descriptors": [ {descriptors_service_1} ]
                },
                {
                    "id": 2,
                    "service_id": 200,
                    "descriptors": [ {descriptors_service_2} ]
                },
                ...
            ]
        }
    '''

    result = []

    for svc in services:

        id = svc[0]
        service_id = svc[1]

        descriptors = get_descriptors(conn, transport_id, id) # Get active descriptors
        
        # Check descriptors
        if descriptors != None and len(descriptors) != 0:
            descriptors = [ get_descriptor_data(conn, i[0], transport_id, id, "SDT") for i in descriptors]
        else:
            descriptors = []

        result.append(
            {
                "id": id, 
                "service_id": service_id, 
                "descriptors": descriptors,          
            }
        )

    return result


def sql_api_sdt_actual(transport_id):
    '''SDT SQL Main function'''

    conn = connect()

    services = get_services(conn, transport_id) # Get all services with data of this ts

    return mapping(conn, transport_id, services)



