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
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *
from dvbobjects.utils.SectionLength import *
from datetime import *
from dateutil.rrule import *
from dateutil.parser import *
from SQL.BATSQL import *
from SQL.NITSQL import *
#from SQL.EITSQLActualSchedule import *
from SQL.EITActualPFSQL import *
from SQL.EITActualScheduleSQL import *
#from SQL.SDTSQL import *
from SQL.SDTSQLtest import *
from SQL.BATSQLDescriptors import *
#from SQL.SDTSQLDescriptors import *
import time



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

# def NIT(network_id, transports, nit_id, descriptors):

#     nit_file_name = "nit_" + str(nit_id) + ".sec"

#     nit_sections = []

#     # Get list of ts_lists
#     sections_ts = check_length(
#         nit_loops(
#             transports, 
#             network_id = network_id, 
#             descriptors = descriptors)[0], 
#         transports, "NIT", 
#         network_id = network_id,
#         descriptors = descriptors)

#     # Generate NIT sections
#     if len(sections_ts) != 0:

#         for idx, i in enumerate(sections_ts):

#             nit = network_information_section(
#                 network_id = network_id,
#                 network_descriptor_loop = nit_loops(
#                     i, 
#                     network_id = network_id, 
#                     descriptors = descriptors)[1], # Get first loop items
#                 transport_stream_loop = nit_loops(
#                     i, 
#                     network_id = network_id, 
#                     descriptors = descriptors)[2], # Get second loop items
#                 version_number = 1,
#                 section_number = idx,
#                 last_section_number = len(sections_ts) - 1
#             )

#             nit_sections.append(nit)

#         # Write sections to nit.sec file
#         with open(nit_file_name, "wb") as DFILE:
#             for sec in nit_sections: 
#                 print (sec)
#                 DFILE.write(sec.pack())
#     else:
#         pass

# nits = [{"network_id": 41007, "id": 1}]#, {"network_id": 41007, "id": 2}]

# for nit in nits:
#     transports = nit_sql_main(nit["id"]) # Get transports list for BAT

#     descriptors = nit_des_sql_main(nit["id"], transports) # Get descriptors for NIT
#     #print (descriptors)

#     NIT(nit["network_id"], transports, nit["id"], descriptors) # Generate Sections
#     null_list("NIT") # Null section list for next loop


# #############################
# # Bouquet Association Table #
# #############################

# def BAT(bouquet_id, transports, descriptors):

#     bat_file_name = "bat_" + str(bouquet_id) + ".sec"

#     bat_sections = []

#     # Get list of ts_lists
#     sections_ts = check_length(
#         bat_loops(
#             transports,
#             bouquet_id = bouquet_id, 
#             descriptors = descriptors)[0], 
#         transports, "BAT",
#         bouquet_id = bouquet_id,
#         descriptors = descriptors)

#     # Generate BAT sections
#     if len(sections_ts) != 0:

#         for idx, (i,j) in enumerate(zip(sections_ts[0], sections_ts[1])):

#             bat = bouquet_association_section(
#                 bouquet_id = bouquet_id,
#                 bouquet_descriptor_loop = bat_loops(
#                     i,
#                     bouquet_id = bouquet_id,
#                     descriptors = j)[1], #Get first loop items
#                 transport_stream_loop = bat_loops(
#                     i, 
#                     bouquet_id = bouquet_id,
#                     descriptors = j)[2], #Get second loop items
#                 version_number = 1,
#                 section_number = idx,
#                 last_section_number = len(sections_ts) - 1,
#             )

#             bat_sections.append(bat)

#         # Write sections to bat.sec file
#         with open(bat_file_name, "wb") as DFILE:
#             for sec in bat_sections: 
#                 print (sec)
#                 DFILE.write(sec.pack())
#     else:
#         pass


# bats = [{"bouquet_id": 24385, "id": 1}, {"bouquet_id": 24816, "id": 2}]

# for bat in bats:
#     transports = bat_sql_main(bat["id"]) # Get transports list for BAT
#     descriptors = bat_des_sql_main(bat["id"], transports) # Get descriptors for NIT
#     print("\n")
#     print("*FIRST**FIRST**FIRST**FIRST**FIRST**FIRST**FIRST**FIRST**FIRST*")
#     print (descriptors)
#     print("*FIRST**FIRST**FIRST**FIRST**FIRST**FIRST**FIRST**FIRST**FIRST*")
#     print("\n")
#     BAT(bat["bouquet_id"], transports, descriptors) # Generate Sections
#     null_list("BAT") # Null section list for next loop


# #############################################################
# #Service Description Actual Table  (ETSI EN 300 468 5.2.3) #
# #############################################################


# def SDTActual(transport, transport_id):

#     sdt_file_name = "sdt_act_" + str(transport_id) + ".sec"

#     sdt_sections = []

#     # Get list of svc_lists
#     sections_ts = check_length_sdt(
#         sdt_loops(
#             transport)[0], 
#         transport,
#         transport_id,
#         "SDT Actual")

#     # Generate SDT sections
#     if len(sections_ts) != 0:

#         for idx, i in enumerate(sections_ts):

#             sdt = service_description_section(
#                 transport_stream_id = transport_id,
#                 original_network_id = 41007,
#                 service_loop = sdt_loops(i)[1], #Get loop items
#                 version_number = 1,
#                 section_number = idx,
#                 last_section_number = len(sections_ts) - 1,
#             )

#             sdt_sections.append(sdt)

#         # Write sections to bat.sec file
#         with open(sdt_file_name, "wb") as DFILE:
#             for sec in sdt_sections: 
#                 print (sec)
#                 DFILE.write(sec.pack())
#     else:
#         pass

# sdt_acts = [{"id": 1}]

# for sdt in sdt_acts:

#     transport = sdt_sql_main(sdt["id"])
#     if len(transport) != 0:
#         SDTActual(transport, sdt["id"])

#         null_list("SDT Actual") # Null section list for next loop
#     else:
#         pass

# #############################################################
# # Service Description Other Table  (ETSI EN 300 468 5.2.3)  #
# #############################################################

# def SDTOther(transport, transport_id):

#     sdt_file_name = "sdt_oth_" + str(transport_id) + ".sec"

#     sdt_oth_sections = []


#     # Get list of svc_lists
#     sections_ts = check_length_sdt(
#         sdt_loops(transport)[0], 
#         transport,
#         transport_id,
#         "SDT Other")

#     # Generate SDT sections
#     if len(sections_ts) != 0:

#         for idx, i in enumerate(sections_ts):

#             sdt = service_description_other_ts_section(
#                 transport_stream_id = transport_id,
#                 original_network_id = 41007,
#                 service_loop = sdt_loops(i)[1], #Get loop items
#                 version_number = 1,
#                 section_number = idx,
#                 last_section_number = len(sections_ts) - 1,
#             )

#             sdt_oth_sections.append(sdt)

#         # Write sections to bat.sec file
#         with open(sdt_file_name, "wb") as DFILE:
#             for sec in sdt_oth_sections: 
#                 print (sec)
#                 DFILE.write(sec.pack())
#     else:
#         pass

# sdt_oth = [{"id": 1}, {"id": 2}]

# for sdt in sdt_oth:

#     transport = sdt_sql_main(sdt["id"])
#     if len(transport) != 0:
#         SDTOther(transport, sdt["id"])

#         null_list("SDT Actual") # Null section list for next loop
#     else:
#         pass

###############################################
# EIT Actual Present/Following (ETSI EN 300 468 5.2.4) #
###############################################

def EITActualPF(services, transport_id):

    eit_file_name = "eit_act_pf_" + str(transport_id) + ".sec"

    eit_actual_pf_sections = []

    for i in services:
        
        if len(i["events"]) != 0:  

            for idx, j in enumerate(i["events"]):
                eit_actual_pf = event_information_section(
                    table_id = EIT_ACTUAL_TS_PRESENT_FOLLOWING,
                    service_id = i["id"],
                    transport_stream_id = transport_id,
                    original_network_id = 41007,
                    event_loop = EIT_loops(j, i["descriptors"], "EIT Actual PF"), #Get loop items
                    segment_last_section_number = len(i["events"]) - 1,
                    version_number = 1, 
                    section_number = idx,
                    last_section_number = len(i["events"]) - 1, 
                )
                eit_actual_pf_sections.append(eit_actual_pf)
            # Write sections to eit.sec file
            with open(eit_file_name, "wb") as DFILE:
                for sec in eit_actual_pf_sections: 
                    print (sec)
                    DFILE.write(sec.pack())
        else:
            pass
    else:
        pass

eit_act_pf = [{"id": 1}, {"id": 2}]

for eit in eit_act_pf:
    services = eit_sql_main(eit["id"])

    if len(services) != 0:
        EITActualPF(services, eit["id"])
        null_list("EIT Actual PF") # Null section list for next loop
    else:
        pass

# # ########################################################
# # # EIT Actual Present/Following (ETSI EN 300 468 5.2.4) #
# # ########################################################

def EITActualSchedule(services, transport_id):

    eit_file_name = "eit_act_sch_" + str(transport_id) + ".sec"

    eit_actual_schedule_sections = []

    sections_ts = []
    
    for svc in services:
        chunks = event_chunks_list(svc["events"])
        print ("###################################################")
        for i in chunks:
            
            for j in i:

                sections_ts.append(
                    {
                        "id": svc["id"], 
                        "service_id": svc["service_id"], 
                        "descriptors": svc["descriptors"], 
                        "events": j
                    }
                )
                #print ("APPEND ==========>" + str(svc["service_id"]) )

    if len(sections_ts) != 0:

        for idx, i in enumerate(sections_ts):

            eit_actual_schedule = event_information_section(
                table_id = EIT_ACTUAL_TS_SCHEDULE14,
                service_id = i["service_id"],
                transport_stream_id = transport_id,
                original_network_id = 41007,
                event_loop = EIT_loops(i["events"], i["descriptors"], "EIT Actual Schedule"), #Get loop items
                segment_last_section_number = len(sections_ts) - 1,
                version_number = 1, 
                section_number = idx,
                last_section_number = len(sections_ts) - 1, 
            )
            eit_actual_schedule_sections.append(eit_actual_schedule)
        print (len(eit_actual_schedule_sections))
        # Write sections to eit_act_pf.sec file
        with open(eit_file_name, "wb") as DFILE:
            for sec in eit_actual_schedule_sections: 
                print (sec)
                DFILE.write(sec.pack())
    else:
        pass

eit_act_sched = [{"id": 1}]

for eit in eit_act_sched:
    services = eit_sch_sql_main(eit["id"])

    if len(services) != 0:
        EITActualSchedule(services, eit["id"])
        null_list("EIT Actual PF") # Null section list for next loop
    else:
        pass

# #######################################################
# # EIT Other Present/Following (ETSI EN 300 468 5.2.4) #
# #######################################################

# eit_other_pf_sections = []

# sections_ts = check_eit_length(eit_loops(events2)[0], events2, "EIT_Other_PF")

# for idx, i in enumerate(sections_ts):

#     for jdx, j in enumerate(i):

#         eit_other_pf = event_information_section(
#             table_id = EIT_ANOTHER_TS_PRESENT_FOLLOWING,
#             service_id = i[0]["sid"],
#             transport_stream_id = 1,
#             original_network_id = 41007,
#             event_loop = eit_loops([j])[1], #Get loop items
#             segment_last_section_number = 1,
#             version_number = 1, 
#             section_number = jdx,
#             last_section_number = len(i) - 1, 
#         )

#         eit_other_pf_sections.append(eit_other_pf)

# # Write sections to eit_oth_pf.sec file
# with open("./eit_oth_pf.sec", "wb") as DFILE:
#     for sec in eit_other_pf_sections: 
#         print (sec)
#         DFILE.write(sec.pack())


# ##############################################################################################
# #################### Prepare time configuration for TOT and TOT tables #######################
# ##############################################################################################

# current_time = time.gmtime()
# current_local_time = time.localtime()

# # italian rules
# current_offset_polarity = 0x0 # positive
# if current_local_time.tm_isdst == 1:
#     start = 'DTSTART:%(year)04d%(month)02d%(day)02dT%(hour)02d%(minute)02d%(second)02d\n' % { 
#         "year": current_time[0], 
#         "month": current_time[1], 
#         "day": current_time[1], 
#         "hour" : 3, 
#         "minute": 0, 
#         "second": 0
#     }
#     start += 'RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10;COUNT=1' # last sunday of october
#     current_offset = 0x02
#     new_offset = 0x01
# else :
#     start = 'DTSTART:%(year)04d%(month)02d%(day)02dT%(hour)02d%(minute)02d%(second)02d\n' % { 
#         "year": current_time[0], 
#         "month": current_time[1], 
#         "day": current_time[1], 
#         "hour" : 2, 
#         "minute": 0, 
#         "second": 0
#     }
#     start += 'RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3;COUNT=1' # last sunday of march
#     current_offset = 0x01
#     new_offset = 0x02

# change_time = list(rrulestr(start))[0]

# ###############################################################################################
# ###############################################################################################
# ###############################################################################################


# #####################################################
# #     Time Offset Table (ETSI EN 300 468 5.2.5)     #
# #####################################################

# tot = time_offset_section(
#     descriptor_loop = [
#         local_time_offset_descriptor(
#             local_time_offset_loop = [
#                 local_time_offset_loop_item(
#                     ISO_639_language_code = b'kaz',
#                     country_region_id = 1,
#                     local_time_offset_polarity = 0,
#                     local_time_offset_hour = 6,
#                     local_time_offset_minute = 0,
#                     year_of_change = change_time.year-1900, 
#                     month_of_change = change_time.month,
#                     day_of_change = change_time.day,
#                     hour_of_change = int(str(((change_time.hour / 10) * 16) + (change_time.hour % 10)).split('.')[0]),
#                     minute_of_change = int(str(((change_time.minute / 10) * 16) + (change_time.minute % 10)).split('.')[0]),
#                     second_of_change = int(str(((change_time.second / 10) * 16) + (change_time.second % 10)).split('.')[0]),
#                     next_time_offset_hour = new_offset,
#                     next_time_offset_minute = 0x00
#                 )
#             ]
#         )
#     ],
#     year = current_time[0]-1900, # since 1900. If now 2019, then 2019 - 1900 = 119
#     month = current_time[1],
#     day = current_time[2],
#     hour = int(str(((current_time[3] / 10) * 16) + (current_time[3] % 10)).split('.')[0]),
#     minute = int(str(((current_time[4] / 10) * 16) + (current_time[4] % 10)).split('.')[0]),
#     second = int(str(((current_time[5] / 10) * 16) + (current_time[5] % 10)).split('.')[0]),
#     version_number = 1,
#     section_number = 0,
#     last_section_number = 0
#     )

# # Write sections to tot.sec file
# with open("./tot.sec", "wb") as DFILE:
#     DFILE.write(tot.pack())


# ####################################################
# #  Time Description Table (ETSI EN 300 468 5.2.5)  #
# ####################################################

# # TDT should be replaced at regeneration run time
    
# tdt = time_date_section(
#     year = current_time[0]-1900, # since 1900. If now 2019, then 2019 - 1900 = 119
#     month = current_time[1],
#     day = current_time[2],
#     hour = int(str(((current_time[3] / 10) * 16) + (current_time[3] % 10)).split('.')[0]),
#     minute = int(str(((current_time[4] / 10) * 16) + (current_time[4] % 10)).split('.')[0]),
#     second = int(str(((current_time[5] / 10) * 16) + (current_time[5] % 10)).split('.')[0]),
#     version_number = 1,
#     section_number = 0,
#     last_section_number = 0,
#     )

# # Write sections to tdt.sec file
# with open("./tdt.sec", "wb") as DFILE:
#     DFILE.write(tdt.pack())

