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
        return columns, data
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def mapping(transport_id, services, service_descriptors):
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

    result = {"ts": transport_id, "services": []}

    for svc in services:

        id = svc[0]
        service_id = svc[1]

        for descriptors in service_descriptors:
            for i in descriptors:
                descriptor_name = get_dict_key(i)
                if i[descriptor_name]["service"] == id:
                    result["services"].append(
                        {
                            "id": id, 
                            "service_id": service_id, 
                            "descriptors": descriptors
                        }
                    )
                else:
                    pass
                break # Check only first descriptor and after break

    return result


def sdt_sql_main(transport_id):
    '''SDT SQL Main function'''

    conn = connect()

    transports_with_services = []

    descriptors = []

    # Temporary list for combine descriptors of each service in one sub-list
    service_descriptors = [] 

    services = get_services(conn, transport_id) # Get all services with data of this ts

    for svc in services:
        service_id = svc[0]
        active_descriptors = get_descriptors(conn, transport_id, service_id)

        if len(active_descriptors) != 0:

            temp_list = []

            for descriptor in active_descriptors:
                descriptor = descriptor[0]

                result = get_descriptor_data(
                            conn, 
                            descriptor, 
                            transport_id, 
                            service_id, 
                            "SDT")

                descriptor_columns = result[0]
                descriptor_data = result[1]

                for data in descriptor_data:

                    dict_data = dict(zip(descriptor_columns, data)) # Combine columns name and data
                    temp_list.append({descriptor: dict_data})

            service_descriptors.append(temp_list)

        else:
            print ("Not found any descriptors for SDT loop")

    mapped = mapping(transport_id, services, service_descriptors) # Mapping transport to services
    transports_with_services.append(mapped) # Append mapping to result list
    
    conn.close()

    return transports_with_services

