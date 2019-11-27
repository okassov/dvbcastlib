import psycopg2
import datetime
from .db_connect import connect

def get_dict_key(dictionary):
    '''This function get dict as arg
    and return it's key in string format'''

    for i in dictionary.keys():
        return i

def get_date():
    '''This function return data 
    for TDT table'''

    date = datetime.datetime.now()
    now_date = int(date.year)
    now_month = int(date.strftime("%m"))
    now_day = int(date.strftime("%d"))
    now_hour_hex = int(date.strftime("%H"))
    now_min_hex = int(date.strftime("%M"))
    now_sec_hex = int(date.strftime("%S"))

    return (now_date, now_month, now_day, now_hour_hex, now_min_hex, now_sec_hex)

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
            eit_actual_schedule_loop WHERE transport=%s and \
            service=%s and is_event=%s and is_active=%s" % (transport_id, service_id, False, True))
        active_descriptors = cur.fetchall()
        return active_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptor_data(conn, descriptor_name, transport_id, service_id, dvb_table, **kwargs):
    '''This function return data of getting descriptor'''

    cur = conn.cursor()

    try:
        if not kwargs["event_id"]:
            cur.execute("SELECT * FROM %s \
                WHERE transport=%s and service=%s \
                and dvb_table='%s'" % (descriptor_name, transport_id, service_id, dvb_table))
        elif kwargs["event_id"] and kwargs["event_id"] != None:
            cur.execute("SELECT * FROM %s \
                WHERE transport=%s and service=%s and event=%s \
                and dvb_table='%s'" % (descriptor_name, transport_id, service_id, event_id, dvb_table))
        else:
            print ("Error! Cannot get descriptor data")
        data = cur.fetchall()
        columns = [i[0] for i in cur.description]
        return columns, data
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()

def get_events(conn, transport_id, service_id):
    ''''''

    cur = conn.cursor()

    # date = get_date()
    # print (date)
    now_date = (2019, 11, 24, 9, 0, 0)

    actual_schedule_events = []
    try:
        cur.execute("SELECT * FROM event \
            WHERE transport=%s and service=%s" % (transport_id, service_id))
        events = cur.fetchall()

        # Find first actual event
        for event in events:
            # if (event[4] + event[7]) == now_date[3]:

            if event[4] <= now_date[3] <= event[4] + event[7]:
                actual_schedule_events.append(event)    
            else:
                pass

        # Find second actual event        
        if len(actual_schedule_events) != 0:
            first_event_id = actual_schedule_events[0][0]
            for event in events:
                if event[0] == first_event_id + 1:
                    actual_schedule_events.append(event)
                else:
                    pass

        return actual_schedule_events
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def mapping(transport_id, services, service_descriptors, service_events):
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

    result = {"ts": transport_id, "services": []}

    # Mapping descriptors to services
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
                            "descriptors": descriptors,
                        }
                    )
                else:
                    pass
                break # Check only first descriptor and after break

    # Mapping EPG events to services 
    for svc in result["services"]:
        for event in service_events:
            id = event[0][14] # id from event tupple (1, 2019, 11, 24, 9, 0, 0, 0, 30, 0, 'EIT', 'second', 1, 1, 1)
            if id == svc["id"]:
                svc["events"] = event
            else:
                pass
    
    return result


def eit_sql_main(transport_id, **kwargs):
    '''SDT SQL Main function'''

    conn = connect()

    transports_with_services = []
    descriptors = []
    events = []

    # Temporary list for combine descriptors of each service in one sub-list
    service_descriptors = [] 

    services = get_services(conn, transport_id) # Get all services with data of this ts

    for svc in services:
        service_id = svc[0]

        actual_events = get_events(conn, transport_id, service_id)
        if actual_events != None and len(actual_events) != 0:       
            events.append(actual_events)
        else:
            pass

        active_descriptors = get_descriptors(conn, transport_id, service_id)

        if active_descriptors != None and len(active_descriptors) != 0:

            temp_list = []

            for descriptor in active_descriptors:
                descriptor = descriptor[0]
                print (descriptor)

                result = get_descriptor_data(
                            conn, 
                            descriptor, 
                            transport_id, 
                            service_id, 
                            "EIT")

                descriptor_columns = result[0]
                descriptor_data = result[1]

                for data in descriptor_data:

                    dict_data = dict(zip(descriptor_columns, data)) # Combine columns name and data
                    temp_list.append({descriptor: dict_data})

            service_descriptors.append(temp_list)

        else:
            print ("Not found any descriptors for EIT loop")


    mapped = mapping(transport_id, services, service_descriptors, events) # Mapping transport to services
    transports_with_services.append(mapped) # Append mapping to result list
    
    conn.close()

    return transports_with_services
