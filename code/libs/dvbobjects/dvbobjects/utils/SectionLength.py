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
from handlers.DefaultHandlers import *

# For BAT sections
bat_ts_for_sections = []
bat_descriptor_for_sections = []

# For NIT sections
nit_ts_for_sections = []
nit_descriptor_for_sections = []

sdt_act_for_sections = []
sdt_act_descriptor_for_sections = []

sdt_oth_for_sections = []
sdt_oth_descriptor_for_sections = []

eit_sched_for_sections = []
eit_act_pf_for_sections = []
eit_oth_pf_for_sections = []

services = [[100, 1], [200, 1], [300, 1], [400, 1], [500, 1], [600, 1], [700, 1], [800, 1], [900, 1],
            [110, 1], [210, 1], [310, 1], [410, 1], [510, 1], [610, 1], [710, 1], [810, 1], [910, 1],
            [120, 1], [220, 1], [320, 1], [420, 1], [520, 1], [620, 1], [720, 1], [820, 1], [920, 1],
            [130, 1], [230, 1], [330, 1], [430, 1], [530, 1], [630, 1], [730, 1], [830, 1], [930, 1],
            [140, 1], [240, 1], [340, 1], [440, 1], [540, 1], [640, 1], [740, 1], [840, 1], [940, 1],
            [150, 1], [250, 1], [350, 1], [450, 1], [550, 1], [650, 1], [750, 1], [850, 1], [950, 1],
            [160, 1], [260, 1], [360, 1], [460, 1], [560, 1], [660, 1], [760, 1], [860, 1], [960, 1],
            [170, 1], [270, 1], [370, 1], [470, 1], [570, 1], [670, 1], [770, 1], [870, 1], [970, 1],
            [180, 1], [280, 1], [380, 1], [480, 1], [580, 1], [680, 1], [780, 1], [880, 1], [980, 1],
            [190, 1], [290, 1], [390, 1], [490, 1]]


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

# def split_to_section_sdt(items_list, descriptors, parts=2):
#     '''This function divide item list into 
#     2 parts, divide this item descriptors and
#     return.
#     For example:

#     Input item_list: 
#         [ ts1, ts2, ts3 ]
#     Input descriptors: 
#         [ 
#             [first_loop], 
#             [second_loop-ts1, second_loop-ts2, second_loop-ts3] 
#         ]
    
#     After divide it will be:

#     Output split_items:
#         [ [ ts1 ], [ ts2, ts3 ] ]
#     Output split_descriptors: 
#         [ 
#             [ [first_loop], [second_loop-ts1] ], 
#             [ [first_loop], [second_loop-ts2, second_loop-ts3] ]
#         ]
#     {'ts': 1, 'services': [{'id': 1, 'service_id': 300}, {'id': 2, 'service_id': 301}, {'id': 3, 'service_id': 302}, {'id': 4, 'service_id': 303}, {'id': 5, 'service_id': 304}, {'id': 6, 'service_id': 305}, {'id': 7, 'service_id': 306}, {'id': 8, 'service_id': 307}, {'id': 9, 'service_id': 308}, {'id': 10, 'service_id': 309}, {'id': 11, 'service_id': 310}, {'id': 12, 'service_id': 311}, {'id': 13, 'service_id': 312}, {'id': 14, 'service_id': 313}, {'id': 15, 'service_id': 314}, {'id': 16, 'service_id': 315}, {'id': 17, 'service_id': 316}, {'id': 18, 'service_id': 317}, {'id': 19, 'service_id': 318}, {'id': 20, 'service_id': 319}, {'id': 21, 'service_id': 320}, {'id': 22, 'service_id': 321}, {'id': 23, 'service_id': 322}, {'id': 24, 'service_id': 323}, {'id': 25, 'service_id': 324}, {'id': 26, 'service_id': 325}, {'id': 27, 'service_id': 326}, {'id': 28, 'service_id': 327}, {'id': 29, 'service_id': 328}, {'id': 30, 'service_id': 329}]}
#     '''
#     #print (descriptors)
#     split_descriptors = []
#     #print (descriptors)

#     sdt_loop_descriptors = descriptors[0]

#     #print (items_list)

#     length = len(items_list)

#     split_items = [ items_list[i*length // parts: (i+1)*length // parts] for i in range(parts) ]
#     #print (split_items)
#     # Create empty lists in split_descritors list = count of sections 
#     for i in range(len(split_items)):
#         split_descriptors.append([])

#     for index, chunk in enumerate(split_items):
#         for item in chunk:
#             #print (item)
#             for descriptor in sdt_loop_descriptors["descriptors"]:
#                 descriptor_name = get_dict_key(descriptor[0])
#                 if descriptor[0][descriptor_name]["service"] == item["id"]:
#                     split_descriptors[index].append(descriptor)
#                 else:
#                     pass
#     new_split_items = []
#     new_split_descriptors = []
#     # for i in range(len(split_items)):
#     #     new_split_items.append({"ts": 1, "services": []})

#     for index, i in enumerate(split_items):
#         new_split_items.insert(index, [{"ts": 1, "services": []}])
#         for j in i:
#             new_split_items[index][0]["services"].append(j)

#     for index, i in enumerate(split_descriptors):
#         new_split_descriptors.insert(index, [{"ts": 1, "descriptors": []}])
#         for j in i:
#             new_split_descriptors[index][0]["descriptors"].append(j)


#     # print (new_split_items)

#     return (new_split_items, new_split_descriptors)


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
    print (len(items_list))
    length = len(items_list)
    result = []
    split_items = [ items_list[i*length // parts: (i+1)*length // parts] for i in range(parts) ]
    #print (split_items)
    # Create empty lists in split_descritors list = count of sections 
    # for i in range(len(split_items)):
    #     split_descriptors.append([])

    # for index, chunk in enumerate(split_items):
    #     for item in chunk:
    #         #print (item)
    #         for descriptor in sdt_loop_descriptors["descriptors"]:
    #             descriptor_name = get_dict_key(descriptor[0])
    #             if descriptor[0][descriptor_name]["service"] == item["id"]:
    #                 split_descriptors[index].append(descriptor)
    #             else:
    #                 pass
    # new_split_items = []
    # new_split_descriptors = []
    # for i in range(len(split_items)):
    #     new_split_items.append({"ts": 1, "services": []})

    for index, i in enumerate(split_items):
        result.insert(index, [{"ts": 1, "services": []}])
        for j in i:
            result[index][0]["services"].append(j)

    # for index, i in enumerate(split_descriptors):
    #     new_split_descriptors.insert(index, [{"ts": 1, "descriptors": []}])
    #     for j in i:
    #         new_split_descriptors[index][0]["descriptors"].append(j)


    # # print (new_split_items)
    #   print (result)
    return result


def event_chunks_list(alist, parts=2):
    '''This function divide EIT event list into 
    chunks lists with len == 2'''

    length = len(alist)

    return [ alist[i:i+parts] for i in range(0, len(alist), parts)]


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


# def sdt_loops(transport, *args, **kwargs):

#     sdt_descriptor_loop = []

#     sdt_loop_descriptors = kwargs["descriptors"]

#     service_descriptor_loop = []

#     service_loop = []

#     transport = transport[0]
#     descriptors = sdt_loop_descriptors[0]

#     for service in transport["services"]:

#         service_descriptor_loop = []
#         active_descriptors = []

#         for descriptor in descriptors["descriptors"]:

#             for des in descriptor:

#                 if service_descriptor_func(des) != None:
#                     if des["service_descriptor"]["service"] == service["id"]:
#                         service_descriptor_loop.append(service_descriptor_func(des))
#                         active_descriptors.append("service_descriptor")
#                     else:
#                         pass
#                 elif private_data_specifier_descriptor_func(des, "first") != None:
#                     if des["private_data_specifier_descriptor"]["service"] == service["id"]:
#                         service_descriptor_loop.append(private_data_specifier_descriptor_func(des, "first"))
#                         active_descriptors.append("private_data_specifier_descriptor")
#                     else:
#                         pass
#                 else:
#                     pass       

#         service_loop.append(
#             service_loop_item(
#                 service_ID = service["service_id"],
#                 EIT_schedule_flag = 0, 
#                 EIT_present_following_flag = 0, 
#                 running_status = 4,
#                 free_CA_mode = 0,       
#                 service_descriptor_loop = service_descriptor_loop
#             )
#         )

#     return sec_len(service_loop), service_loop

def sdt_loops(transport, *args, **kwargs):

    sdt_descriptor_loop = []

    service_descriptor_loop = []

    service_loop = []

    # print ("\n")
    # print ("############################################################")
    # print (transport)

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

def eit_loops(events_list):

    el = event_loop = [
        event_loop_item(
            event_id = i["event_id"], 
            start_year = 108, # since 1900
            start_month = 6, 
            start_day = 10,
            start_hours = 0x23,
            start_minutes = 0x30,
            start_seconds = 0x00, 
            duration_hours = 0x12, 
            duration_minutes = 0x00,
            duration_seconds = 0x00, 
            running_status = 4, # 4 service is running, 1 not running, 2 starts in a few seconds, 3 pausing
            free_CA_mode = 0, # 0 means service is not scrambled, 1 means at least a stream is scrambled
            event_descriptor_loop = [
                component_descriptor (
                    stream_content = 1,
                    component_type = 1,
                    component_tag = 0,
                    ISO_639_language_code = b"rus",
                    text_char = b"Description of component"
                ),
                ca_identifier_descriptor (
                    ca_identifier_descriptor_loop = [
                        ca_identifier_descriptor_loop_item (
                            ca_system_id = 2514
                        )
                    ]
                ),
                parental_rating_descriptor (
                    country_code = b"KAZ",
                    rating = 1
                ),
                extended_event_descriptor (
                    descriptor_number = 0,
                    last_descriptor_number = 0,
                    ISO639_language_code = b"KAZ",
                    extended_event_loop = [
                        extended_event_loop_item(
                            item = b"",
                            item_description = b""
                        )
                    ],
                    text = b"asdasd"
                ),
                short_event_descriptor (
                    ISO639_language_code = b"KAZ", 
                    event_name = i["event_name"],
                    text = i["text"], 
                )    
            ],
        ) for i in events_list
    ]
    return sec_len(el), el


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


# def check_length_sdt(item_length, items_list, transport_id, table, *args, **kwargs):
#     '''This function check length of second loop for all
#     transports in this loop. If length of loop > 1024 - 3,
#     then it's divides trasnport list to multiple list, like 1/2
#     using "split_to_section" function for it.
#     And agian check this transport lists. Until the length 
#     is not consistent with the standard.
#     Finally return list with sections of table with
#     standard length'''
#     #print (kwargs["descriptors"])
#     section_max_size = 1024 # Standard maximum length of DVB Table section, except EIT

#     if table == "SDT Actual":
#         ts_section_list = sdt_act_for_sections
#         descriptor_section_list = sdt_act_descriptor_for_sections
#     elif table == "SDT Other":
#         ts_section_list = sdt_oth_for_sections
#         descriptor_section_list = sdt_oth_descriptor_for_sections
#     else:
#         pass

#     if 0 <= (item_length + 13) <= (section_max_size - 3):
#         ts_section_list.append(items_list)
#         descriptor_section_list.append(kwargs["descriptors"])
#         # print("\n")
#         # print("*FINAL*FINAL*FINAL**FINAL**FINAL**FINAL**FINAL**FINAL*")
#         # print (bat_descriptor_for_sections)
#         # print("*FINAL*FINAL*FINAL**FINAL**FINAL**FINAL**FINAL**FINAL*")
#         # print("\n")
#     else:
#         get_sections = split_to_section_sdt(items_list[0]["services"], kwargs["descriptors"])
#         sections = get_sections[0]
#         sections_descriptors = get_sections[1]

#         for sec, sec_des in zip(sections, sections_descriptors):
#             #print (sec)
#             if table == "SDT Actual":
#                 check_length_sdt(
#                     sdt_loops(
#                         sec,
#                         descriptors = sec_des)[0],
#                     sec,
#                     transport_id,
#                     table, 
#                     descriptors = sec_des) # Recursion
#             elif table == "SDT Other":
#                 check_length_sdt(
#                     sdt_loops(
#                         sec,
#                         descriptors = sec_des)[0], 
#                     sec, 
#                     table,
#                     descriptors = sec_des) # Recursion
#     return (ts_section_list, descriptor_section_list)


def check_length_sdt(item_length, items_list, transport_id, table, *args, **kwargs):
    '''This function check length of second loop for all
    transports in this loop. If length of loop > 1024 - 3,
    then it's divides trasnport list to multiple list, like 1/2
    using "split_to_section" function for it.
    And agian check this transport lists. Until the length 
    is not consistent with the standard.
    Finally return list with sections of table with
    standard length'''
    #print (kwargs["descriptors"])
    section_max_size = 1024 # Standard maximum length of DVB Table section, except EIT

    if table == "SDT Actual":
        ts_section_list = sdt_act_for_sections
    elif table == "SDT Other":
        ts_section_list = sdt_oth_for_sections
    else:
        pass

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
                    table) # Recursion
    return ts_section_list


def check_eit_length(item_length, items_list, table):
    '''This function check length of EIT dexcriptors loop. 
    If length of loop > 4096 - 3,
    then it's divides trasnport list to multiple list like 1/2
    and agian check this transport lists. Until the length 
    is not consistent with the standard.'''

    section_max_size = 4096

    if table == "EIT_Schedule":
        ts_section_list = eit_sched_for_sections
    elif table == "EIT_Actual_PF":
        ts_section_list = eit_act_pf_for_sections
    elif table == "EIT_Other_PF":
        ts_section_list = eit_oth_pf_for_sections
    else:
        pass

    section = event_chunks_list(items_list)

    for i in section:
        if table == "EIT_Schedule":
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
    else:
        pass

