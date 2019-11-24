import psycopg2
from .db_connect import connect


def get_services(conn, transport_id):
    '''This function return all services that
    bind to getting transport_id'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM \
            services WHERE transport=%s" % (transport_id))
        services = cur.fetchall()
        return services
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()  


def get_sdt_loop_descriptors(conn, transport_id, service_id):
    '''This function return all ACTIVE descriptors that 
    binding for getting service_id and transport_id'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT descriptor_name FROM \
            sdt_loop WHERE transport=%s and \
            service=%s and is_active=%s" % (transport_id, service_id, True))
        sdt_loop_descriptors = cur.fetchall()
        return sdt_loop_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_sdt_descriptor_data(conn, descriptor_name, transport_id, service_id, dvb_table):
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


def sdt_des_sql_main(transport_id):

    # Main return list
    sdt_loop_list = [] 

    # Temporary list for combine descriptors of each service in one sub-list
    temp_list_all = [] 

    # Initiate structure of main return list
    sdt_loop_list.append({"ts": transport_id, "descriptors": []}) 

    conn = connect()

    # Get services id
    services = get_services(conn, transport_id) 

    for index, svc in enumerate(services):

        service_id = svc[0]

        # Get active descriptors for this service
        sdt_loop_descriptors = get_sdt_loop_descriptors(
                                conn, 
                                transport_id, 
                                service_id)

        if len(sdt_loop_descriptors) != 0:

            temp_list = []

            for descriptor in sdt_loop_descriptors:

                descriptor_name = descriptor[0]
                result = get_sdt_descriptor_data(
                        conn, 
                        descriptor_name, 
                        transport_id, 
                        service_id, 
                        "SDT")

                columns = result[0]
                data_all = result[1]

                for data in data_all:

                    dict_data = dict(zip(columns, data)) # Combine columns name and data
                    temp_list.append({descriptor_name: dict_data})

            temp_list_all.append(temp_list)
     
        else:
            print ("Not found any descriptors for SDT loop")

    # Add all descriptors to final main return list
    if len(temp_list_all) != 0:
        for i in temp_list_all:
            sdt_loop_list[-1]["descriptors"].append(i)
    else:
        print("Not found any descriptors in temp_list")
        sdt_loop_list[-1]["descriptors"].append([])

    conn.close()
    
    return sdt_loop_list

#sdt_des_sql_main(1)