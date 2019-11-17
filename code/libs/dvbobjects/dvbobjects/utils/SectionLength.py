#! /usr/bin/env python

import string
import os
from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.PSI.BAT import *
from dvbobjects.PSI.EIT import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *

bat_ts_for_sections = []
nit_ts_for_sections = []
sdt_svc_for_sections = []
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


def split_list(alist, parts=2):
    '''This function divide list into 2 parts'''

    length = len(alist)

    return [ alist[i*length // parts: (i+1)*length // parts] 
             for i in range(parts) ]

def event_chunks_list(alist, parts=2):
    '''This function divide EIT event list into 
    chunks lists with len == 2'''

    length = len(alist)

    result = [ alist[i:i+parts] for i in range(0, len(alist), parts)]

    print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print (result)

    return [ alist[i:i+parts] for i in range(0, len(alist), parts)]


def sec_len(first_loop, second_loop = []):
    '''This function calculate bat section length.
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
        print (len(fl_bytes))
        return len(fl_bytes)


def bat_loops(transports_list, services_list):
    '''Function get 2 list args with transports and services,
    and return length of loops.
    Args:
    transports_list = [ts_id1, ts_id2, ...]
    services_list = [[[ts_id1_sid1, ts_id1_sid1_type], [ts_id1_sid1, ts_id1_sid1_type], ...]]
    Return:
    (sec_len, bdl, tdl)'''

    bdl = bouquet_descriptor_loop = [
            bouquet_name_descriptor(bouquet_name = b"Subscriber BAT [0x5F41]")
        ]

    tdl = transport_stream_loop = [
            transport_stream_loop_item(
                transport_stream_id = i,
                original_network_id = 41007,
                transport_descriptor_loop = [
                    service_list_descriptor(
                        dvb_service_descriptor_loop = [
                            service_descriptor_loop_item(
                                 service_ID = i[0], 
                                 service_type = i[1],
                            ) for i in services_list
                        ],
                    )
                ]
            ) for i in transports_list
        ]

    return sec_len(bdl, tdl), bdl, tdl


def nit_loops(transports_list, services_list):
    '''Function get 2 list args with transports and services,
    and return length of loops'''

    ndl = network_descriptor_loop = [
        network_descriptor(network_name = b"Marat Network",),
        multilingual_network_descriptor(
            multilingual_network_descriptor_loop = [
                multilingual_network_descriptor_loop_item(
                    ISO_639_language_code = b"rus",
                    network_name = b"Kazteleradio"
                )
            ]
        ),
        private_data_specifier_descriptor(private_data_specifier = 24577),
        ]

    tdl = transport_stream_loop = [
        transport_stream_loop_item(
            transport_stream_id = i,
            original_network_id = 41007,
            transport_descriptor_loop = [
                service_list_descriptor(
                    dvb_service_descriptor_loop = [
                        service_descriptor_loop_item(
                             service_ID = i[0], 
                             service_type = i[1],
                        ) for i in services_list
                    ]
                ),
                transport_stream_sat_descriptor(
                    frequency = 1211141313,
                    orbital_position = 5850,
                    west_east_flag = 1,
                    polarization = 3,
                    roll_off = 0,
                    modulation_system = 1,
                    modulation_type = 1,
                    symbol_rate = 30,
                    FEC_inner = 3
                )
            ]        
        ) for i in transports_list
    ]

    return sec_len(ndl, tdl), ndl, tdl


def sdt_loops(services):

    sl = service_loop = [ 
        service_loop_item(
            service_ID = i[0],
            EIT_schedule_flag = 0, # 0 no current even information is broadcasted, 1 broadcasted
            EIT_present_following_flag = 0, # 0 no next event information is broadcasted, 1 is broadcasted
            running_status = 4, # 4 service is running, 1 not running, 2 starts in a few seconds, 3 pausing
            free_CA_mode = 0, # 0 means service is not scrambled, 1 means at least a stream is scrambled
            service_descriptor_loop = [
                service_descriptor(
                    service_type = 1, # digital television service
                    service_provider_name = b"Marat Provider",
                    service_name = b"Marat Service",
                ),
                private_data_specifier_descriptor(private_data_specifier = 24577),
                epg_information_descriptor(
                    epg_information_loop = [
                        epg_information_descriptor_loop_item(
                            parental_rating = 60,
                            inverse_CGMS_A_value = 1
                        )
                    ]
                )
            ]
        ) for i in services   
    ]

    return sec_len(sl), sl

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


def check_length(item_length, items_list, table):
    '''This function check length of second loop for all
    transports in this loop. If length of loop > 1024 - 3,
    then it's divides trasnport list to multiple list like 1/2
    and agian check this transport lists. Until the length 
    is not consistent with the standard.'''

    section_max_size = 1024

    if table == "BAT":
        ts_section_list = bat_ts_for_sections
    elif table == "NIT":
        ts_section_list = nit_ts_for_sections
    elif table == "SDT":
        ts_section_list = sdt_svc_for_sections
    elif table == "EIT":
        ts_section_list = eit_for_sections
    else:
        pass

    if 0 <= (item_length + 13) <= (section_max_size - 3):
        ts_section_list.append(items_list)
    else:
        section = split_list(items_list)
        for i in section:
            if table == "BAT":
                check_length(bat_loops(i, services)[0], i, table)
            elif table == "NIT":
                check_length(nit_loops(i, services)[0], i, table)
            elif table == "SDT":
                check_length(sdt_loops(i)[0], i, table)
            elif table == "EIT":
                check_length(eit_loops(i)[0], i, table)
    print (ts_section_list)
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
    if table == "EIT_Actual_PF":
        ts_section_list = eit_act_pf_for_sections
    if table == "EIT_Other_PF":
        ts_section_list = eit_oth_pf_for_sections
    else:
        pass

    section = event_chunks_list(items_list)
    for i in section:
        if table == "EIT_Schedule":
            ts_section_list.append(i)
        if table == "EIT_Actual_PF":
            ts_section_list.append(i)
        if table == "EIT_Other_PF":
            ts_section_list.append(i)
        else:
            pass

    return ts_section_list

