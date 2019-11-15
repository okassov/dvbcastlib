#! /usr/bin/env python

import string
import os
from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.PSI.BAT import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *

bat_ts_for_sections = []
nit_ts_for_sections = []

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


def sec_len(first_loop, second_loop):
    '''This function calculate bat section length.
    Get first_loop descriptors and second_loop 
    descriptors as args. Return section length'''

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
                        ) for i in services
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


def check_length(transports_length, transports, ts_section):
    '''This function check length of second loop for all
    transports in this loop. If length of loop > 1024 - 3,
    then it's divides trasnport list to multiple list like 1/2
    and agian check this transport lists. Until the length 
    is not consistent with the standard.'''

    section_max_size = 1024

    if ts_section == "BAT":
        ts_section_list = bat_ts_for_sections
    elif ts_section == "NIT":
        ts_section_list = nit_ts_for_sections
    else:
        pass

    if 0 <= (transports_length + 13) <= (section_max_size - 3):
        ts_section_list.append(transports)
    else:
        section = split_list(transports)
        for i in section:
            check_length(bat_loops(i, services)[0], i, ts_section)
    print (ts_section_list)
    return ts_section_list

