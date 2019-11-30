import psycopg2
from .db_connect import connect


def get_transports(conn, network_object_id):
    '''This function return DISTINCT (NOT DUPLICATE) transport id's
    from nit_to_services TABLE'''

    cur = conn.cursor()

    try:
        cur.execute("SELECT id, transport_id FROM \
            transports WHERE network=%s" % network_object_id)
        transports = cur.fetchall()
        return transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_services(conn, transport_id):
    '''This function return services data 
    from services TABLE. If transport exist
    and have services function return list
    with tupples.

    Output: [(id1, service_id1), (id2, service_id2), ...]

    If transport not exist function return empty list: []
    '''

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


def get_descriptors(conn, object_id, is_first = False):
    '''This function return names of all ACTIVE 
    descriptors that binding for getting 
    service_id and transport_id.

    Ouput: [(descriptor1_name), (descriptor2_name), ...]

    If transport not exist function return empty list: []
    '''

    cur = conn.cursor()
    try:
        if is_first:
            cur.execute("SELECT descriptor_name FROM \
                nit_first_loop WHERE network=%s \
                and is_active=%s" % (object_id, True))
        else:
            cur.execute("SELECT descriptor_name FROM \
                nit_second_loop WHERE transport=%s \
                and is_active=%s" % (object_id, True))

        active_descriptors = cur.fetchall()
        return active_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptor_data(conn, descriptor_name, object_id, dvb_table, is_first = False):

    cur = conn.cursor()
    try:
        if is_first:
            cur.execute("SELECT * FROM %s \
                WHERE network=%s and dvb_table='%s'" % (descriptor_name, object_id, dvb_table))
            data = cur.fetchall()
            columns = [i[0] for i in cur.description]

            temp_data = []
            
            if data != None and len(data) != 0:
                if descriptor_name == "multilingual_network_descriptor": # Because many services
                    for value in data:
                        temp_data.append(dict(zip(columns, list(value))))
                    result = { descriptor_name: temp_data }
                else:
                    result = { descriptor_name: dict(zip(columns, list(data[0]))) }
            else:
                result = { descriptor_name: dict(zip(columns, [])) }

        else:
            cur.execute("SELECT * FROM %s \
                WHERE transport=%s and dvb_table='%s'" % (descriptor_name, object_id, dvb_table))
            data = cur.fetchall()

            columns = [i[0] for i in cur.description]

            temp_data = []

            if data != None and len(data) != 0:
                if descriptor_name == "service_list_descriptor": # Because many services
                    for value in data:
                        temp_data.append(dict(zip(columns, list(value))))
                    result = { descriptor_name: temp_data }
                else:
                    result = { descriptor_name: dict(zip(columns, list(data[0]))) }
            else:
                result = { descriptor_name: dict(zip(columns, [])) }
        
        return result

    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def mapping(conn, network_object_id, network_id, transports):
    '''This function map services and service descriptors 
    to transport. It's get transport_id, list of services with
    data in tupple and descriptors in list as args.
    For example:
    Input transport_id: 1
    Input services: [(service_1_data, ...), (service_2_data, ...), ...]
    Input descriptors: [[{descriptors_service_1}], [{descriptors_service2}], ...]
    Input events: [(actual_event_1), (actual_event_2)]
    
    Output result: 
        {
            "ts" 1, 
            "services": 
            [
                {
                    "id": 1,
                    "service_id": 100,
                    "descriptors": [ {descriptors_service_1} ],
                    "events": [(actual_event_1), (actual_event_2)]
                },
                {
                    "id": 2,
                    "service_id": 200,
                    "descriptors": [ {descriptors_service_2} ],
                    "events": [(actual_event_1), (actual_event_2)]
                },
                ...
            ]
        }
    '''

    first_loop_descriptors = get_descriptors(conn, network_object_id, True)

    # Mapping NIT first loop descriptors
    if first_loop_descriptors != None and len(first_loop_descriptors) != 0:
        first_loop_descriptors = [ get_descriptor_data(conn, i[0], network_object_id, "NIT", True) for i in first_loop_descriptors ]
    else:
        first_loop_descriptors = []


    result = { "network": network_object_id, "network_id": network_id, "descriptors": first_loop_descriptors, "transports": [] }

    # Mapping descriptors to services
    for transport in transports:

        id = transport[0] # Index of transport in database
        transport_id = transport[1] # DVB transport id

        second_loop_descriptors = get_descriptors(conn, id, False)

        # Check descriptors
        if second_loop_descriptors != None and len(second_loop_descriptors) != 0:
            second_loop_descriptors = [ get_descriptor_data(conn, i[0], id, "NIT", False) for i in second_loop_descriptors ]
        else:
            second_loop_descriptors = []

        result["transports"].append(
            {
                "id": id, 
                "transport_id": transport_id, 
                "descriptors": second_loop_descriptors       
            }
        )

    return result


def nit_sql_main(network_object_id, network_id):
    conn = connect()

    transports = get_transports(conn, network_object_id)

    return mapping(conn, network_object_id, network_id, transports)
