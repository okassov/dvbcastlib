import psycopg2
from .db_connect import connect


def get_bat_transports(conn, bat_object_id):
    '''This function return DISTINCT (NOT DUPLICATE) transport id's
    from bat_to_services TABLE'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT transport, transport_id FROM \
            bouquet_to_transports WHERE bouquet=%s" % bat_object_id)
        transports = cur.fetchall()
        print (transports)
        return transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_services(conn, service_id):
    '''This function return services data 
    from services TABLE'''

    cur = conn.cursor()

    try:
        cur.execute("SELECT id, service_id FROM \
            services WHERE id=%s" % service_id)
        services = cur.fetchone()
        return services
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptors(conn, bat_object_id, transport_id=None, is_first = False):
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
                bat_first_loop WHERE bouquet=%s \
                and is_active=%s" % (bat_object_id, True))
        else:
            cur.execute("SELECT descriptor_name FROM \
                bat_second_loop WHERE bouquet=%s and transport=%s \
                and is_active=%s" % (bat_object_id, transport_id, True))

        active_descriptors = cur.fetchall()
        return active_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptor_data(conn, descriptor_name, bat_object_id, dvb_table, transport_object_id=None, is_first = False):

    cur = conn.cursor()
    try:
        if is_first:

            loop_descriptors = [] # Append to this list descriptors with many data

            cur.execute("SELECT * FROM %s WHERE bouquet=%s \
                and dvb_table='%s'" % (descriptor_name, bat_object_id, dvb_table))
            data = cur.fetchall()
            columns = [i[0] for i in cur.description]

            temp_data = []
            
            if data != None and len(data) != 0:
                if descriptor_name in loop_descriptors: # Because many services
                    for value in data:
                        temp_data.append(dict(zip(columns, list(value))))
                    result = { descriptor_name: temp_data }
                else:
                    result = { descriptor_name: dict(zip(columns, list(data[0]))) }
            else:
                result = { descriptor_name: dict(zip(columns, [])) }

        else:

            loop_descriptors = [
                "service_list_descriptor",
                "nds_e2_descriptor",
                "nds_e4_descriptor"
            ] # Append to this list descriptors with many data

            cur.execute("SELECT * FROM %s WHERE bouquet=%s \
                and transport=%s and dvb_table='%s'" % (descriptor_name, 
                                                        bat_object_id, 
                                                        transport_object_id, 
                                                        dvb_table))

            data = cur.fetchall()

            columns = [i[0] for i in cur.description]

            temp_data = []

            if data != None and len(data) != 0:
                if descriptor_name in loop_descriptors: # Because many services
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


def mapping(conn, bat_object_id, bouquet_id, transports):
    
    first_loop_descriptors = get_descriptors(conn, bat_object_id, None, True)

    # Mapping NIT first loop descriptors
    if first_loop_descriptors != None and len(first_loop_descriptors) != 0:
        first_loop_descriptors = [ 
            get_descriptor_data(
                conn, 
                i[0], 
                bat_object_id,  
                "BAT",
                None,
                True
            ) for i in first_loop_descriptors 
        ]
    else:
        first_loop_descriptors = []


    result = { 
                "bat": bat_object_id, 
                "bouquet_id": bouquet_id, 
                "descriptors": first_loop_descriptors, 
                "transports": [] 
             }

    # Mapping descriptors to services
    for transport in transports:

        cur = conn.cursor()

        transport_object_id = transport[0] # Index of transport in database
        transport_id = transport[1] # Index of transport in network

        second_loop_descriptors = get_descriptors(
            conn, 
            bat_object_id, 
            transport_object_id, 
            False
        )

        # Check descriptors
        if second_loop_descriptors != None and len(second_loop_descriptors) != 0:

            second_loop_descriptors = [ 
                get_descriptor_data(
                    conn, 
                    i[0], 
                    bat_object_id, 
                    "BAT", 
                    transport_object_id,
                    False
                ) for i in second_loop_descriptors 
            ]

        else:
            second_loop_descriptors = []

        result["transports"].append(
            {
                "id": transport_object_id, 
                "transport_id": transport_id,
                "descriptors": second_loop_descriptors       
            }
        )

    return result




def sql_api_bat(bat_object_id, bouquet_id):
    conn = connect()
    transports = get_bat_transports(conn, bat_object_id)

    if transports != None and transports != 0:
        return mapping(conn, bat_object_id, bouquet_id, transports)
    else:
        print ("Error! Not found any transports mapping to this bouquet.")
        pass

