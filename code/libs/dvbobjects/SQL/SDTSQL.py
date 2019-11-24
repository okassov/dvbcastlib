import psycopg2
from .db_connect import connect


# def get_transports(conn, network_id):
#     '''This function return transport id's
#     from nit_to_services TABLE'''

#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT transport_id FROM \
#             transports WHERE network=%s" % network_id)
#         transports = cur.fetchall()
#         return transports
#     except psycopg2.Error as e:
#         print (e)
#     finally:
#         cur.close()


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


def mapping(transport_id, services):
    '''This function map service_ids to transport.
    It's get transport_id and list of services with
    data in tupple as args.
    For example:
    Input transport_id: 1
    Inpurt services: [(service_1_data, ...), (service_2_data, ...), ...]
    
    Output result: {"ts" 1, "services": [service_1_data, service_2_data]}
    '''

    result = {"ts": transport_id, "services": []}

    for svc in services:

        id = svc[0]
        service_id = svc[1]

        result["services"].append({"id": id, "service_id": service_id})

    return result


def sdt_sql_main(transport_id):
    '''BAT SQL Main function'''

    conn = connect()

    transports_with_services = []

    # transports = get_transports(conn, network_id) # Get all transports of network

    services = get_services(conn, transport_id) # Get all services with data of this ts
    mapped = mapping(transport_id, services) # Mapping transport to services
    transports_with_services.append(mapped) # Append mapping to result list
    
    conn.close()

    return transports_with_services


#sdt_sql_main(1)
