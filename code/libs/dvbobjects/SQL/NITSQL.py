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


def get_nit_ts(conn, nit_id):
    '''This function return DISTINCT (NOT DUPLICATE) transport id's
    from nit_to_services TABLE'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT transport_id FROM \
            transports WHERE network=%s" % nit_id)
        nit_transports = cur.fetchall()
        return nit_transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_nit_svc(conn, ts_id):
    '''This function return services data 
    from services TABLE'''

    cur = conn.cursor()

    try:
        cur.execute("SELECT service_id, service_type FROM \
            services WHERE transport=%s" % ts_id)
        svc = cur.fetchall()
        return svc
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def nit_ts_list(conn, ts_list, result_list):
    '''This function generate and return list
    for BAT Generation. Get transports list and 
    nit_id as ARG'''

    for ts in ts_list:

        cur = conn.cursor()

        result_list.append({"ts": ts[0], "services": []})

        service_data = get_nit_svc(conn, ts[0])

        for svc in service_data:
            for i in result_list:
                if i["ts"] == ts[0]:
                    i["services"].append(
                        {
                            "sid": svc[0], 
                            "type": svc[1], 
                            "lcn": svc[1]
                        }
                    )
                else:
                    pass
    return result_list


def nit_sql_main(nit_id):
    '''BAT SQL Main function'''

    nit_to_transports = []

    conn = connect()

    result = nit_ts_list(conn, get_nit_ts(conn, nit_id), nit_to_transports)
    
    conn.close()

    return result