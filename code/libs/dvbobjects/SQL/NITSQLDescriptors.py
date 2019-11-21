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


def get_first_loop_descriptors(conn, network_id):
    '''This function return DISTINCT (NOT DUPLICATE) transport id's
    from nit_to_services TABLE'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT descriptor_name FROM \
            nit_first_loop WHERE network=%s" % network_id)
        first_loop_descriptors = cur.fetchall()
        return first_loop_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_second_loop_descriptors(conn, transport_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT descriptor_name FROM \
            nit_second_loop WHERE transport=%s" % transport_id)
        second_loop_descriptors = cur.fetchall()
        return second_loop_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_descriptor_data(conn, loop, descriptor_name, item_id, dvb_table):
    cur = conn.cursor()
    try:
        if loop == "first":
            cur.execute("SELECT * FROM %s \
                WHERE network=%s and dvb_table='%s'" % (descriptor_name, item_id, dvb_table))
            data = cur.fetchall()
            columns = [i[0] for i in cur.description]
            return columns, data
        elif loop == "second":
            cur.execute("SELECT * FROM %s \
                WHERE transport=%s and dvb_table='%s'" % (descriptor_name, item_id, dvb_table))
            data = cur.fetchall()
            columns = [i[0] for i in cur.description]
            #print (data)
            return columns, data
        else:
            print ("Error! Please give correct loop")
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def nit_des_sql_main(network_id, ts_id_list):

    first_loop_list = []
    second_loop_list = []

    conn = connect()

    first_loop_descriptors = get_first_loop_descriptors(conn, network_id)


    if len(first_loop_descriptors) != 0:
        for descritor in first_loop_descriptors:

            result = get_descriptor_data(conn, "first", descritor[0], network_id, "NIT")
            columns = result[0]
            data_all = result[1]

            for data in data_all:

                dict_data = dict(zip(columns, data))
                first_loop_list.append({descritor[0]: dict_data})

    else:
        print ("Not found any descriptors for NIT first loop")

    for ts_id in ts_id_list:
        second_loop_descriptors = get_second_loop_descriptors(conn, ts_id["ts"])

        if len(second_loop_descriptors) != 0:

            second_loop_list.append({"ts": ts_id["ts"], "descriptors": []})

            for descritor in second_loop_descriptors:

                result = get_descriptor_data(conn, "second", descritor[0], ts_id["ts"], "NIT")
                columns = result[0]
                data_all = result[1]

                for data in data_all:

                    dict_data = dict(zip(columns, data))
                    #print (second_loop_list)
                    second_loop_list[-1]["descriptors"].append({descritor[0]: dict_data})
                    # second_loop_list.append({"ts": ts_id["ts"], "descriptors": {descritor[0]: dict_data}})
                        
        else:
            print ("Not found any descriptors for NIT second loop")

    conn.close()

    #print (second_loop_list)

    return first_loop_list, second_loop_list