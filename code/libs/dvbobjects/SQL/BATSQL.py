import psycopg2

bat_to_transports = []

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


def get_bat_ts(conn, bat_id):
    '''This function return DISTINCT (NOT DUPLICATE) transport id's
    from bat_to_services TABLE'''

    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT transport_id FROM bat_to_transports WHERE bat_id=%s" % bat_id)
        bat_transports = cur.fetchall()
        return bat_transports
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_bat_svc(conn, svc_id):
    '''This function return services data 
    from services TABLE'''

    cur = conn.cursor()

    try:
        cur.execute("SELECT service_id, service_type FROM services WHERE id=%s" % svc_id)
        svc = cur.fetchone()
        return svc
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def bat_ts_list(conn, ts_list):
    '''This function generate and return list
    for BAT Generation. Get transports list as ARG'''

    for ts in ts_list:

        cur = conn.cursor()

        cur.execute("SELECT service_id FROM bat_to_transports WHERE transport_id=%s" % ts[0])

        bat_to_transports.append({"ts": ts[0], "services": []})

        while True:
            next_row = cur.fetchone()
            if next_row:
                service_data = get_bat_svc(conn, next_row[0])
                for i in bat_to_transports:
                    if i["ts"] == ts[0]:
                        i["services"].append(
                            {
                                "sid": service_data[0], 
                                "type": service_data[1], 
                                "lcn": service_data[1]
                            }
                        )
                    else:
                        pass
            else:
                break
        cur.close()


def bat_sql_main():

    conn = connect()

    bat_ts_list(conn, get_bat_ts(conn, 1))

    return bat_to_transports