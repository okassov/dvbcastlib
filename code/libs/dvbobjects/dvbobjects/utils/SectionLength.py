#! /usr/bin/env python

import os
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.BAT import *
from dvbobjects.PSI.EIT import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *
from SQL.NITSQLDescriptors import *
from handlers.NITHandlers import *
from handlers.BATHandlers import *
from handlers.SDTHandlers import *
from handlers.EITHandlers import *
from handlers.DefaultHandlers import *

# For BAT sections
bat_ts_for_sections = []
bat_descriptor_for_sections = []

# For NIT sections
nit_ts_for_sections = []
nit_descriptor_for_sections = []

# For SDT Actual sections
sdt_act_for_sections = []

# For SDT Other sections
sdt_oth_for_sections = []

eit_sched_for_sections = []
eit_act_pf_for_sections = []
eit_oth_pf_for_sections = []


def split_to_section(items_list, descriptors, parts=2):
    '''This function divide item list into 
    2 parts, divide this item descriptors and
    return.
    For example:

    Input item_list: 
        [ ts1, ts2, ts3 ]
    Input descriptors: 
        [ 
            [first_loop], 
            [second_loop-ts1, second_loop-ts2, second_loop-ts3] 
        ]
    
    After divide it will be:

    Output split_items:
        [ [ ts1 ], [ ts2, ts3 ] ]
    Output split_descriptors: 
        [ 
            [ [first_loop], [second_loop-ts1] ], 
            [ [first_loop], [second_loop-ts2, second_loop-ts3] ]
        ]

    '''
    #print (items_list)
    split_descriptors = []

    first_loop_descriptors = descriptors[0]
    second_loop_descriptors = descriptors[1]

    length = len(items_list)

    split_items = [ items_list[i*length // parts: (i+1)*length // parts] for i in range(parts) ]
    
    # Create empty lists in split_descritors list = count of sections 
    for i in range(len(split_items)):
        split_descriptors.append([])

    for index, chunk in enumerate(split_items):
        split_descriptors[index].insert(0, first_loop_descriptors) #Insert first loop into descriptor chunk
        split_descriptors[index].insert(1, []) #Pre-insert empty list for second loop into descriptor chunk
        for item in chunk:
            for descriptor in second_loop_descriptors:
                if descriptor["ts"] == item["ts"]:
                    split_descriptors[index][1].append(descriptor)
                else:
                    pass
    return (split_items, split_descriptors)


def split_to_section_sdt(items_list, parts=2):
    '''This function divide item list into 
    2 parts, divide this item descriptors and
    return.
    For example:

    Input item_list: 
        [ ts1, ts2, ts3 ]
    Input descriptors: 
        [ 
            [first_loop], 
            [second_loop-ts1, second_loop-ts2, second_loop-ts3] 
        ]
    
    After divide it will be:

    Output split_items:
        [ [ ts1 ], [ ts2, ts3 ] ]
    Output split_descriptors: 
        [ 
            [ [first_loop], [second_loop-ts1] ], 
            [ [first_loop], [second_loop-ts2, second_loop-ts3] ]
        ]
    {'ts': 1, 'services': [{'id': 1, 'service_id': 300}, {'id': 2, 'service_id': 301}, {'id': 3, 'service_id': 302}, {'id': 4, 'service_id': 303}, {'id': 5, 'service_id': 304}, {'id': 6, 'service_id': 305}, {'id': 7, 'service_id': 306}, {'id': 8, 'service_id': 307}, {'id': 9, 'service_id': 308}, {'id': 10, 'service_id': 309}, {'id': 11, 'service_id': 310}, {'id': 12, 'service_id': 311}, {'id': 13, 'service_id': 312}, {'id': 14, 'service_id': 313}, {'id': 15, 'service_id': 314}, {'id': 16, 'service_id': 315}, {'id': 17, 'service_id': 316}, {'id': 18, 'service_id': 317}, {'id': 19, 'service_id': 318}, {'id': 20, 'service_id': 319}, {'id': 21, 'service_id': 320}, {'id': 22, 'service_id': 321}, {'id': 23, 'service_id': 322}, {'id': 24, 'service_id': 323}, {'id': 25, 'service_id': 324}, {'id': 26, 'service_id': 325}, {'id': 27, 'service_id': 326}, {'id': 28, 'service_id': 327}, {'id': 29, 'service_id': 328}, {'id': 30, 'service_id': 329}]}
    '''

    length = len(items_list)
    result = []
    split_items = [ items_list[i*length // parts: (i+1)*length // parts] for i in range(parts) ]

    for index, i in enumerate(split_items):
        result.insert(index, [{"ts": 1, "services": []}])
        for j in i:
            result[index][0]["services"].append(j)

    return result


def event_chunks_list(alist, parts=2):
    '''This function divide EIT event list into 
    chunks lists with len == 2'''

    chunks = [alist[i:i+parts] for i in range(0,len(alist),parts)]

    return chunks


def sec_len(first_loop, second_loop = []):
    '''This function calculate section length.
    Get first_loop descriptors and second_loop 
    descriptors as args. Return section length'''

    if len(second_loop) != 0:

        # pack first_loop_descriptors
        fl_bytes = b"".join(
            map(lambda x: x.pack(),
            first_loop))

        # pack second_loop_descriptors
        sl_bytes = b"".join(
            map(lambda x: x.pack(),
            second_loop))

        print ("Calculated length ===> " + str(len(fl_bytes) + len(sl_bytes)))

        return len(fl_bytes) + len(sl_bytes)

    else:

        # pack only first_loop_descriptors
        fl_bytes = b"".join(
            map(lambda x: x.pack(),
            first_loop))

        print ("Calculated length ===> " + str(len(fl_bytes)))
        return len(fl_bytes)


def bat_loops(transports_list, *args, **kwargs):
    '''Function get 2 list args with transports and services,
    and return length of loops.
    Args:
    transports_list = [ts_id1, ts_id2, ...]
    services_list = [[[ts_id1_sid1, ts_id1_sid1_type], [ts_id1_sid1, ts_id1_sid1_type], ...]]
    Return:
    (sec_len, bdl, tdl)'''

    bouquet_descriptor_loop = []
    transport_stream_loop = []

    first_loop_descriptors = kwargs["descriptors"][0]
    second_loop_descriptors = kwargs["descriptors"][1]
    bouquet_id = kwargs["bouquet_id"]

    # Generate first_loop
    for descriptor in first_loop_descriptors:
        if bouquet_name_descriptor_func(descriptor) != None:
            bouquet_descriptor_loop.append(
                bouquet_name_descriptor_func(descriptor)
            )
        else:
            pass

    # Generate second loop
    for descriptor in second_loop_descriptors:
        transport_stream_loop.append(
            transport_stream_loop_item(
                transport_stream_id = descriptor["ts"],
                original_network_id = 41007,
                transport_descriptor_loop = [
                    service_list_descriptor_func(descriptor),
                    private_data_specifier_descriptor_func(descriptor, "second"),
                    nds_e2_descriptor_func(descriptor),
                    nds_e4_descriptor_func(descriptor)
                ]
            )
        )

    return (sec_len(bouquet_descriptor_loop, transport_stream_loop), 
            bouquet_descriptor_loop, transport_stream_loop)


def nit_loops(transports_list, *args, **kwargs):
    '''Function get 2 list args with transports,
    and return length of loops'''

    network_descriptor_loop = []
    transport_stream_loop = []

    first_loop_descriptors = kwargs["descriptors"][0]
    second_loop_descriptors = kwargs["descriptors"][1]
    network_id = kwargs["network_id"]

    # Generate first_loop
    for descriptor in first_loop_descriptors:

        if network_name_descriptor_func(descriptor) != None:
            network_descriptor_loop.append(
                network_name_descriptor_func(descriptor)
            )
        elif multilingual_network_descriptor_func(descriptor) != None:
            network_descriptor_loop.append(
                multilingual_network_descriptor_func(descriptor)
            )
        elif private_data_specifier_descriptor_func(descriptor, "first") != None:
            network_descriptor_loop.append(
                private_data_specifier_descriptor_func(descriptor, "first")
            )
        else:
            pass

    # Generate second loop
    for descriptor in second_loop_descriptors:
        transport_stream_loop.append(
            transport_stream_loop_item(
                transport_stream_id = descriptor["ts"],
                original_network_id = network_id,
                transport_descriptor_loop = [
                    service_list_descriptor_func(descriptor),
                    satellite_delivery_system_descriptor_func(descriptor)
                ]
            )
        )

    return (sec_len(network_descriptor_loop, transport_stream_loop), 
            network_descriptor_loop, 
            transport_stream_loop)


def sdt_loops(transport, *args, **kwargs):

    service_loop = []

    transport = transport[0]

    for service in transport["services"]:

        service_descriptor_loop = []
        active_descriptors = []

        for descriptor in service["descriptors"]:

            if service_descriptor_func(descriptor) != None:
                service_descriptor_loop.append(service_descriptor_func(descriptor))
            elif private_data_specifier_descriptor_func(descriptor, "first") != None:
                service_descriptor_loop.append(private_data_specifier_descriptor_func(descriptor, "first"))
            else:
                pass       

        service_loop.append(
            service_loop_item(
                service_ID = service["service_id"],
                EIT_schedule_flag = 0, 
                EIT_present_following_flag = 0, 
                running_status = 4,
                free_CA_mode = 0,       
                service_descriptor_loop = service_descriptor_loop
            )
        )

    return sec_len(service_loop), service_loop


def EIT_loops(events, descriptors, table):
    '''This function create EIT loop. Get events
    and descriptors of service as args. Return list
    with EIT sections.

    Input: 
    events = { 
        "first event": [ 
                        id, year, mon, day, hour, min, sec, dhour, dmin, 
                        dsec, EIT, loop, network, transport, service
                        ] 
        "descriptors": [{event1_descriptor}, {event1_descriptor}, ...]
        }
    descriptors = [{service1_descriptor1}, {service1_descriptor2}, ...]

    Output:
    el = [EIT_section1, EIT_section2, ...]
    '''
    
    event_descriptor_loop = []

    if "first_event" in events:
        key = "first_event"
    elif "second_event" in events:
        key = "second_event"
    else:
        pass

    # Add descriptors to loop
    for descriptor in descriptors:
        if component_descriptor_func(descriptor) != None:
            event_descriptor_loop.append(component_descriptor_func(descriptor))
        elif ca_identifier_descriptor_func(descriptor) != None:
            event_descriptor_loop.append(ca_identifier_descriptor_func(descriptor))
        elif parental_rating_descriptor_func(descriptor) != None:
            event_descriptor_loop.append(parental_rating_descriptor_func(descriptor))
        else:
            pass  

    # Add event descriptors to loop
    for event_descriptor in events["descriptors"]:
        if short_event_descriptor_func(event_descriptor) != None:
            event_descriptor_loop.append(short_event_descriptor_func(event_descriptor))   
        elif extended_event_descriptor_func(event_descriptor) != None:
            event_descriptor_loop.append(extended_event_descriptor_func(event_descriptor))
        else:
            pass

    if table == "EIT Actual PF":
        el = event_loop = [
            event_loop_item(
                event_id = events[key][0],
                start_year = events[key][1] - 1900, # since 1900
                start_month = events[key][2], 
                start_day = events[key][3],
                start_hours = events[key][4],
                start_minutes = events[key][5],
                start_seconds = events[key][6], 
                duration_hours = events[key][7], 
                duration_minutes = events[key][8],
                duration_seconds = events[key][9], 
                running_status = 4, # 4 service is running, 1 not running, 2 starts in a few seconds, 3 pausing
                free_CA_mode = 0, # 0 means service is not scrambled, 1 means at least a stream is scrambled
                event_descriptor_loop = event_descriptor_loop
            )
        ]
    elif table == "EIT Actual Schedule":
        el = event_loop = [
            event_loop_item(
                event_id = events["event"][0],
                start_year = events["event"][1] - 1900, # since 1900
                start_month = events["event"][2], 
                start_day = events["event"][3],
                start_hours = events["event"][4],
                start_minutes = events["event"][5],
                start_seconds = events["event"][6], 
                duration_hours = events["event"][7], 
                duration_minutes = events["event"][8],
                duration_seconds = events["event"][9], 
                running_status = 4, # 4 service is running, 1 not running, 2 starts in a few seconds, 3 pausing
                free_CA_mode = 0, # 0 means service is not scrambled, 1 means at least a stream is scrambled
                event_descriptor_loop = event_descriptor_loop
            )
        ]
    return el


def check_length(item_length, items_list, table, *args, **kwargs):
    '''This function check length of second loop for all
    transports of BAT or NIT. If length of loop > 1024 - 3,
    then it's divides trasnport list to multiple list, like 1/2
    using "split_to_section" function for it.
    And agian check this transport lists. Until the length 
    is not consistent with the standard.
    Finally return list with sections of table with
    standard length'''

    section_max_size = 1024 # Standard maximum length of DVB Table section, except EIT

    if table == "BAT":
        ts_section_list = bat_ts_for_sections
        descriptor_section_list = bat_descriptor_for_sections
    elif table == "NIT":
        ts_section_list = nit_ts_for_sections
        descriptor_section_list = nit_descriptor_for_sections
    elif table == "SDT Actual":
        ts_section_list = sdt_act_for_sections
    elif table == "SDT Other":
        ts_section_list = sdt_oth_for_sections
    else:
        pass

    if 0 <= (item_length + 13) <= (section_max_size - 3):
        ts_section_list.append(items_list)
        descriptor_section_list.append(kwargs["descriptors"])
        # print("\n")
        # print("*FINAL*FINAL*FINAL**FINAL**FINAL**FINAL**FINAL**FINAL*")
        # print (bat_descriptor_for_sections)
        # print("*FINAL*FINAL*FINAL**FINAL**FINAL**FINAL**FINAL**FINAL*")
        # print("\n")
    else:
        get_sections = split_to_section(items_list, kwargs["descriptors"])
        sections = get_sections[0]
        sections_descriptors = get_sections[1]

        for sec, sec_des in zip(sections, sections_descriptors):
            if table == "BAT":
                check_length(
                    bat_loops(
                        sec,
                        bouquet_id = kwargs["bouquet_id"],
                        descriptors = sec_des)[0],
                    sec, 
                    table, 
                    bouquet_id = kwargs["bouquet_id"],
                    descriptors = sec_des) # Recursion
            elif table == "NIT":
                check_length(
                    nit_loops(
                        sec,
                        network_id = kwargs["network_id"],
                        descriptors = sec_des)[0], 
                    sec, 
                    table, 
                    network_id = kwargs["network_id"],
                    descriptors = sec_des) # Recursion

            elif table == "SDT Actual":
                check_length(sdt_loops(sec)[0], sec, table)
            elif table == "SDT Other":
                check_length(sdt_loops(sec)[0], sec, table)

    return (ts_section_list, descriptor_section_list)


def check_length_sdt(item_length, items_list, transport_id, table, *args, **kwargs):
    '''This function check length of second loop for all
    transports in this loop. If length of loop > 1024 - 3,
    then it's divides trasnport list to multiple list, like 1/2
    using "split_to_section" function for it.
    And agian check this transport lists. Until the length 
    is not consistent with the standard.
    Finally return list with sections of table with
    standard length'''

    section_max_size = 1024 # Standard maximum length of DVB Table section, except EIT

    if table == "SDT Actual":
        ts_section_list = sdt_act_for_sections
    elif table == "SDT Other":
        ts_section_list = sdt_oth_for_sections
    else:
        print ("Error! Please use correct DVB Table name")

    if 0 <= (item_length + 13) <= (section_max_size - 3):
        ts_section_list.append(items_list)
    else:
        sections = split_to_section_sdt(items_list[0]["services"])

        for sec in sections:
            if table == "SDT Actual":
                check_length_sdt(
                    sdt_loops(sec)[0],
                    sec,
                    transport_id,
                    table) # Recursion
            elif table == "SDT Other":
                check_length_sdt(
                    sdt_loops(sec)[0], 
                    sec,
                    transport_id,
                    table) # Recursion

    return ts_section_list


def check_length_eit(items_list, table):
    '''This function check length of EIT dexcriptors loop. 
    If length of loop > 4096 - 3,
    then it's divides trasnport list to multiple list like 1/2
    and agian check this transport lists. Until the length 
    is not consistent with the standard.'''

    section_max_size = 4096

    if table == "EIT Actual Schedule":
        ts_section_list = eit_sched_for_sections
    elif table == "EIT_Actual_PF":
        ts_section_list = eit_act_pf_for_sections
    elif table == "EIT_Other_PF":
        ts_section_list = eit_oth_pf_for_sections
    else:
        pass

    section = event_chunks_list(items_list)

    print (section)

    for i in section:
        if table == "EIT Actual Schedule":
            ts_section_list.append(i)
        elif table == "EIT_Actual_PF":
            ts_section_list.append(i)
        elif table == "EIT_Other_PF":
            ts_section_list.append(i)
        else:
            pass

    return ts_section_list


def null_list(dvb_table):
    '''This function clear global section lists
    for next loop'''

    if dvb_table == "BAT": 
        bat_ts_for_sections.clear()
    elif dvb_table == "NIT": 
        nit_ts_for_sections.clear()
    elif dvb_table == "SDT Actual": 
        sdt_act_for_sections.clear()
    elif dvb_table == "EIT Actual Schedule": 
        eit_sched_for_sections.clear()
    else:
        pass

