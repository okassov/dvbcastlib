import psycopg2
from .db_connect import connect

def get_first_loop_descriptors(conn, bat_id):
    '''This function return transport id's
    from nit_to_services TABLE'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT descriptor_name FROM \
            bat_first_loop WHERE bat=%s and is_active=%s" % (bat_id, True))
        first_loop_descriptors = cur.fetchall()
        return first_loop_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_second_loop_descriptors(conn, transport_id, bat_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT descriptor_name FROM \
            bat_second_loop WHERE transport=%s and bat=%s and is_active=%s" % (transport_id, bat_id, True))
        second_loop_descriptors = cur.fetchall()
        #print (second_loop_descriptors)
        return second_loop_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_descriptor_data(conn, loop, descriptor_name, item_id, dvb_table, bat_id = None, ):
    cur = conn.cursor()
    try:
        if loop == "first":
            cur.execute("SELECT * FROM %s \
                WHERE bat=%s and dvb_table='%s'" % (descriptor_name, item_id, dvb_table))
            data = cur.fetchall()
            columns = [i[0] for i in cur.description]
            return columns, data
        elif loop == "second":
            cur.execute("SELECT * FROM %s \
                WHERE bat=%s and transport=%s and dvb_table='%s'" % (descriptor_name, bat_id, item_id, dvb_table))
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


def bat_des_sql_main(bat_id, ts_id_list):

    #print (ts_id_list)

    first_loop_list = []
    second_loop_list = []

    conn = connect()

    first_loop_descriptors = get_first_loop_descriptors(conn, bat_id)


    if first_loop_descriptors != None and len(first_loop_descriptors) != 0:
        for descritor in first_loop_descriptors:

            result = get_descriptor_data(conn, "first", descritor[0], bat_id, "BAT")
            columns = result[0]
            data_all = result[1]

            for data in data_all:

                dict_data = dict(zip(columns, data))
                first_loop_list.append({descritor[0]: dict_data})

    else:
        print ("Not found any descriptors for BAT first loop")

    for ts_id in ts_id_list:
        second_loop_descriptors = get_second_loop_descriptors(conn, ts_id["ts"], bat_id)

        if second_loop_descriptors != None and len(second_loop_descriptors) != 0:

            second_loop_list.append({"ts": ts_id["ts"], "descriptors": []})

            for descritor in second_loop_descriptors:

                result = get_descriptor_data(conn, "second", descritor[0], ts_id["ts"], "BAT", bat_id)
                columns = result[0]
                data_all = result[1]

                for data in data_all:

                    dict_data = dict(zip(columns, data))
                    #print (second_loop_list)
                    second_loop_list[-1]["descriptors"].append({descritor[0]: dict_data})
                    # second_loop_list.append({"ts": ts_id["ts"], "descriptors": {descritor[0]: dict_data}})
                        
        else:
            print ("Not found any descriptors for BAT second loop")

    conn.close()

    #print (second_loop_list)

    return first_loop_list, second_loop_list