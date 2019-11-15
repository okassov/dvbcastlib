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

ts_for_sections = []

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


def bat_sec_len(first_loop, second_loop):
    '''This function calculate bat section length.
    Get first_loop descriptors and second_loop 
    descriptors as args. Return section length'''

    # pack bouquet_descriptor_loop
    bdl_bytes = b"".join(
        map(lambda x: x.pack(),
        first_loop))

    # pack transport_stream_loop
    tsl_bytes = b"".join(
        map(lambda x: x.pack(),
        second_loop))

    print ("Calculated length ===> " + str(len(bdl_bytes) + len(tsl_bytes)))

    return len(bdl_bytes) + len(tsl_bytes)


def bat_loops(transports_list, services_list):
    '''Function get 2 list args with transports and services,
    and return length of loops'''

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

    return bat_sec_len(bdl, tdl), bdl, tdl


def split_list(alist, wanted_parts=2):
    '''This function divide list into 2 parts'''

    length = len(alist)

    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]


def check_length(transports_length, transports):
    '''This function check length of second loop for all
    transports in this loop. If length of loop > 1024 - 3,
    then it's divides trasnport list to multiple list like 1/2
    and agian check this transport lists. Until the length 
    is not consistent with the standard.'''

    section_max_size = 1024


    if 0 <= (transports_length + 13) <= (section_max_size - 3):
        ts_for_sections.append(transports)
        #print (ts_for_sections)
    else:
        section = split_list(transports)
        #print (section)
        for i in section:
            check_length(bat_loops(i, services)[0], i)


    return (ts_for_sections)


