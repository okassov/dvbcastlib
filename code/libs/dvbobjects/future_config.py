#! /usr/bin/env python

import os
from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.PSI.BAT import *
from dvbobjects.PSI.EIT import *
from dvbobjects.PSI.TDT import *
from dvbobjects.PSI.TOT import *
from dvbobjects.utils.SectionLength import *
from dvbobjects.utils.DateTime import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *



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

services2 = [100,200,300,400,500,600,700,800,900,901,902,903,904,905,906,
            101,201,303,401,501,601,701,801,907,908,909,910,911,912,913]
transports = [1,2,3,4]

events = [
            {"event_id": 1, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"event_id": 2, "event_name": b"Second Event", "text": b"Second Event Text"}, 
            {"event_id": 3, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 4, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 5, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"event_id": 6, "event_name": b"Second Event", "text": b"Second Event Text"}, 
            {"event_id": 7, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 8, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 9, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"event_id": 10, "event_name": b"Second Event", "text": b"Second Event Text"}, 
            {"event_id": 11, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 12, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 13, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"event_id": 14, "event_name": b"Second Event", "text": b"Second Event Text"}, 
            {"event_id": 15, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 16, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 17, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 18, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 19, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"event_id": 20, "event_name": b"Second Event", "text": b"Second Event Text"}, 
            {"event_id": 21, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 22, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 23, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 24, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
            {"event_id": 25, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"event_id": 26, "event_name": b"Second Event", "text": b"Second Event Text"}, 
            {"event_id": 27, "event_name": b"Third Event", "text": b"Third Event Text"}, 
            {"event_id": 28, "event_name": b"Fourth Event", "text": b"Fourth Event Text"},
        ]

events2 = [
            {"sid": 100, "event_id": 1, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"sid": 100, "event_id": 2, "event_name": b"Second Event", "text": b"Second Event Text"},
            {"sid": 200, "event_id": 1, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"sid": 200, "event_id": 2, "event_name": b"Second Event", "text": b"Second Event Text"},
            {"sid": 300, "event_id": 1, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"sid": 300, "event_id": 2, "event_name": b"Second Event", "text": b"Second Event Text"},
            {"sid": 400, "event_id": 1, "event_name": b"First Event", "text": b"First Event Text"}, 
            {"sid": 400, "event_id": 2, "event_name": b"Second Event", "text": b"Second Event Text"},
        ]


# #############################
# # Network Information Table #
# #############################

# nit_sec_res = []

# # Get list of ts_lists
# sections_ts = check_length(nit_loops(transports, services)[0], transports, "NIT")

# # Generate sections
# for idx, val in enumerate(sections_ts):

#     nit = network_information_section(
#         network_id = 41007,
#         network_descriptor_loop = nit_loops(val, services)[1],
#         transport_stream_loop = nit_loops(val, services)[2],
#         version_number = 1,
#         section_number = idx,
#         last_section_number = len(sections_ts) - 1
#     )
#     nit_sec_res.append(nit)

# # Write sections to nit.sec file
# with open("./nit.sec", "wb") as DFILE:
#     for sec in nit_sec_res: 
#         print (sec)
#         DFILE.write(sec.pack())


# ############################################################################

# #############################
# # Bouquet Association Table #
# #############################


# bat_sec_res = []

# # Get list of ts_lists
# sections_ts = check_length(bat_loops(transports, services)[0], transports, "BAT")

# # Generate sections
# for idx, val in enumerate(sections_ts):

#     bat = bouquet_association_section(
#         bouquet_id = 24385,
#         bouquet_descriptor_loop = bat_loops(val, services)[1],
#         transport_stream_loop = bat_loops(val, services)[2],
#         version_number = 1,
#         section_number = idx,
#         last_section_number = len(sections_ts) - 1,
#     )

#     bat_sec_res.append(bat)

# # Write sections to bat.sec file
# with open("./bat.sec", "wb") as DFILE:
#     for sec in bat_sec_res: 
#         print (sec)
#         DFILE.write(sec.pack())

# #############################################################################################


# #####################################################
# # Service Description Table (ETSI EN 300 468 5.2.3) #
# #####################################################

# sdt_sec_res = []

# # Get list of svc_lists
# sections_ts = check_length(sdt_loops(services)[0], services, "SDT")

# print (sections_ts)

# # Generate sections
# for idx, val in enumerate(sections_ts):

#     print (len(sections_ts))

#     sdt = service_description_section(
#         transport_stream_id = 1,
#         original_network_id = 41007,
#         service_loop = sdt_loops(val)[1],
#         version_number = 1,
#         section_number = idx,
#         last_section_number = len(sections_ts) - 1,
#     )

#     sdt_sec_res.append(sdt)

# # Write sections to bat.sec file
# with open("./sdt.sec", "wb") as DFILE:
#     for sec in sdt_sec_res: 
#         print (sec)
#         DFILE.write(sec.pack())



#####################################################
#  Event Information Table (ETSI EN 300 468 5.2.4)  #
#####################################################

#######################
# EIT Actual Schedule #
#######################

# eit_sch_sec_res = []

# sections_ts = check_eit_length(eit_loops(events)[0], events, "EIT_Schedule")

# for i in services2:
#     for idx, val in enumerate(sections_ts):

#         print (len(sections_ts))

#         eit_schedule = event_information_section(
#             table_id = EIT_ACTUAL_TS_SCHEDULE14,
#             service_id = i,
#             transport_stream_id = 1,
#             original_network_id = 41007,
#             event_loop = eit_loops(val)[1],
#             segment_last_section_number = 1,
#             version_number = 1, 
#             section_number = idx, # this is the second section
#             last_section_number = len(sections_ts) - 1, 
#         )

#         eit_sch_sec_res.append(eit_schedule)

#     # Write sections to bat.sec file
#     with open("./eit_sch.sec", "wb") as DFILE:
#         for sec in eit_sch_sec_res: 
#             print (sec)
#             DFILE.write(sec.pack())

################################
# EIT Actual Present/Following #
################################

eit_act_pf_sec_res = []

sections_ts = check_eit_length(eit_loops(events2)[0], events2, "EIT_Actual_PF")

for idx, val in enumerate(sections_ts):

    print (len(sections_ts))
    print (len(val))


    for iidx, i in enumerate(val):

        eit_actual_pf = event_information_section(
            table_id = EIT_ACTUAL_TS_PRESENT_FOLLOWING,
            service_id = val[0]["sid"],
            transport_stream_id = 1,
            original_network_id = 41007,
            event_loop = eit_loops([i])[1],
            segment_last_section_number = 1,
            version_number = 1, 
            section_number = iidx, # this is the second section
            last_section_number = len(val) - 1, 
        )

        eit_act_pf_sec_res.append(eit_actual_pf)

# Write sections to bat.sec file
with open("./eit_act_pf.sec", "wb") as DFILE:
    for sec in eit_act_pf_sec_res: 
        print (sec)
        DFILE.write(sec.pack())


################################
# EIT Other Present/Following  #
################################

eit_oth_pf_sec_res = []

sections_ts = check_eit_length(eit_loops(events2)[0], events2, "EIT_Other_PF")

for idx, val in enumerate(sections_ts):

    print (len(sections_ts))
    print (len(val))
    

    for iidx, i in enumerate(val):

        eit_other_pf = event_information_section(
            table_id = EIT_ANOTHER_TS_PRESENT_FOLLOWING,
            service_id = val[0]["sid"],
            transport_stream_id = 1,
            original_network_id = 41007,
            event_loop = eit_loops([i])[1],
            segment_last_section_number = 1,
            version_number = 1, 
            section_number = iidx, # this is the second section
            last_section_number = len(val) - 1, 
        )

        eit_oth_pf_sec_res.append(eit_other_pf)

# Write sections to bat.sec file
with open("./eit_oth_pf.sec", "wb") as DFILE:
    for sec in eit_oth_pf_sec_res: 
        print (sec)
        DFILE.write(sec.pack())


#########################################################

tot = time_offset_section(
    descriptor_loop = [
        local_time_offset_descriptor(
            local_time_offset_loop = [
                local_time_offset_loop_item(
                    ISO_639_language_code = b'kaz',
                    country_region_id = 1,
                    local_time_offset_polarity = 0,
                    local_time_offset_hour = 6,
                    local_time_offset_minute = 0,
                    year_of_change = get_date()[0], 
                    month_of_change = get_date()[1],
                    day_of_change = get_date()[2],
                    hour_of_change = 0,
                    minute_of_change = 0,
                    second_of_change = 0,
                    next_time_offset_hour = 6,
                    next_time_offset_minute = 0
                )
            ]
        )
    ],
    year = get_date()[0], # since 1900. If now 2019, then 2019 - 1900 = 119
    month = get_date()[1],
    day = get_date()[2],
    hour = get_date()[3], # use hex like decimals
    minute = get_date()[4],
    second = get_date()[5],
    version_number = 1,
    section_number = 0,
    last_section_number = 0
    )

with open("./tot.sec", "wb") as DFILE:
    DFILE.write(tot.pack())

#####################################################
#  Time Description Table (ETSI EN 300 468 5.2.5)   #
#####################################################

# TDT should be replaced at regeneration run time

tdt = time_date_section(
    year = get_date()[0], # since 1900. If now 2019, then 2019 - 1900 = 119
    month = get_date()[1],
    day = get_date()[2],
    hour = get_date()[3], # use hex like decimals
    minute = get_date()[4],
    second = get_date()[5],
    version_number = 1,
    section_number = 0,
    last_section_number = 0,
    )

with open("./tdt.sec", "wb") as DFILE:
    DFILE.write(tdt.pack())