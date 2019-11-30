import psycopg2
import datetime
from .db_connect import connect


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


def get_descriptors(conn, transport_id, service_id, is_event = False):
    '''This function return names of all ACTIVE 
    descriptors that binding for getting 
    service_id and transport_id.

    Ouput: [(descriptor1_name), (descriptor2_name), ...]

    If transport not exist function return empty list: []
    '''

    cur = conn.cursor()
    try:
        if is_event:
            cur.execute("SELECT descriptor_name FROM \
                eit_actual_schedule_loop WHERE transport=%s and \
                service=%s and is_event=%s \
                and is_active=%s" % (transport_id, service_id, True, True))
        else:
            cur.execute("SELECT descriptor_name FROM \
                eit_actual_schedule_loop WHERE transport=%s and \
                service=%s and is_event=%s \
                and is_active=%s" % (transport_id, service_id, False, True))

        active_descriptors = cur.fetchall()
        return active_descriptors
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_descriptor_data(conn, descriptor_name, transport_id, service_id, dvb_table, **kwargs):
    '''This function return column and data of getting descriptor
    as dictionary.

    Output: { "column1": data1, "column2": data2, ... }

    If data not exist function return empty dict: {}
    '''

    cur = conn.cursor()

    try:

        if not kwargs:
            cur.execute("SELECT * FROM %s \
                WHERE transport=%s and service=%s \
                and dvb_table='%s'" % (descriptor_name, 
                                        transport_id, 
                                        service_id, 
                                        dvb_table))

        elif kwargs and kwargs["event_id"]:

            cur.execute("SELECT * FROM %s WHERE transport=%s \
                and service=%s and event=%s \
                and dvb_table='%s'" % (descriptor_name, 
                                        transport_id, 
                                        service_id, 
                                        kwargs["event_id"], 
                                        dvb_table))
        
        # Get data and columns 
        data = cur.fetchall()
        columns = [i[0] for i in cur.description]

        if data != None and len(data) != 0:
            data = list(data[0]) # Modify tuple columns to list
        else:
            data = []

        result = { descriptor_name: dict(zip(columns, data)) }

        return result
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def get_actual_event(events, now_date, is_first=True, **kwargs):

    result = []

    if is_first:
        # Find first actual event
        for event in events:
            if event[4] <= now_date[3] <= event[4] + event[7]: # Доработать!!!!!!!!!!!!!!!
                result = list(event)
            else:
                pass
        return result

    elif is_first == False and kwargs:
        # Find second actual event        
        first_event_id = kwargs["first_event_id"]
        for event in events:
            if event[0] == first_event_id + 1:
                result = list(event)
            else:
                pass
        return result
    else:
        pass


def get_events(conn, transport_id, service_id):
    ''''''

    cur = conn.cursor()

    # date = get_date()
    # print (date)
    now_date = (2019, 11, 24, 9, 0, 0)

    actual_schedule_events = []

    event_descriptors = get_descriptors(conn, transport_id, service_id, True) # Get active event descriptors

    try:
        cur.execute("SELECT * FROM event \
            WHERE transport=%s and service=%s" % (transport_id, service_id))
        events = cur.fetchall()

        if events != None and len(events) != 0:

            # Get first actual event with event descriptors
            first_event = get_actual_event(events, now_date, True)
            if first_event != None and len(first_event) != 0:
                first_event_id = first_event[0]
                descriptors = [ get_descriptor_data(conn, i[0], transport_id, service_id, "EIT", event_id = first_event_id) for i in event_descriptors ]
                actual_schedule_events.append({"event": first_event, "descriptors": descriptors})
                
                # Get second actual event with event descriptors        
                second_event = get_actual_event(events, now_date, False, first_event_id = first_event_id)
                if second_event != None and len(second_event) != 0:
                    second_event_id = second_event[0]
                    descriptors = [ get_descriptor_data(conn, i[0], transport_id, service_id, "EIT", event_id = second_event_id) for i in event_descriptors ]
                    actual_schedule_events.append({"event": second_event, "descriptors": descriptors})

            else:
                pass
        return actual_schedule_events
    except psycopg2.Error as e:
        print (e)
    finally:
        cur.close()


def mapping(conn, transport_id, services):
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

    #result = {"ts": transport_id, "services": []}
    result = []

    # Mapping descriptors to services
    for svc in services:

        id = svc[0]
        service_id = svc[1]

        events = get_events(conn, transport_id, id) # Get events
        
        descriptors = get_descriptors(conn, transport_id, id) # Get active descriptors

        # Check descriptors
        if descriptors != None and len(descriptors) != 0:
            descriptors = [ get_descriptor_data(conn, i[0], transport_id, id, "EIT") for i in descriptors]
        else:
            descriptors = []

        result.append(
            {
                "id": id, 
                "service_id": service_id, 
                "descriptors": descriptors,
                "events": events           
            }
        )

    result = {"ts": transport_id, "services": result} # Add for other because need key "ts"

    return result



def eit_oth_pf_sql_main(transport_id):

    conn = connect()

    services = get_services(conn, transport_id)

    return mapping(conn, transport_id, services)