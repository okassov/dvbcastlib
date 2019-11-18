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

services2 = [100,200,300,400,500,600,700,800,900,901,902,903,904,905,906,
            101,201,303,401,501,601,701,801,907,908,909,910,911,912,913]

services3 = [
    {"ts": 1, 
    "services": 
        [
            {"sid": 100, "type": 1, "lcn": 10}, 
            {"sid": 101, "type": 1, "lcn": 20}, 
            {"sid": 103, "type": 1, "lcn": 30},
            {"sid": 104, "type": 1, "lcn": 40}, 
            {"sid": 105, "type": 1, "lcn": 50}, 
            {"sid": 106, "type": 1, "lcn": 60},
            {"sid": 107, "type": 1, "lcn": 70}, 
            {"sid": 108, "type": 1, "lcn": 80}, 
            {"sid": 109, "type": 1, "lcn": 90},
            {"sid": 110, "type": 1, "lcn": 100}, 
            {"sid": 111, "type": 1, "lcn": 101}, 
            {"sid": 112, "type": 1, "lcn": 102},
            {"sid": 113, "type": 1, "lcn": 103}, 
            {"sid": 114, "type": 1, "lcn": 104}, 
            {"sid": 115, "type": 1, "lcn": 105},
            {"sid": 116, "type": 1, "lcn": 106}, 
            {"sid": 117, "type": 1, "lcn": 107}, 
            {"sid": 118, "type": 1, "lcn": 108},
            {"sid": 119, "type": 1, "lcn": 109}, 
            {"sid": 120, "type": 1, "lcn": 110}, 
            {"sid": 121, "type": 1, "lcn": 111},
            {"sid": 122, "type": 1, "lcn": 112}, 
            {"sid": 123, "type": 1, "lcn": 113}, 
            {"sid": 124, "type": 1, "lcn": 114},
            {"sid": 125, "type": 1, "lcn": 115}, 
            {"sid": 126, "type": 1, "lcn": 116}, 
            {"sid": 127, "type": 1, "lcn": 117},
            {"sid": 128, "type": 1, "lcn": 118}, 
            {"sid": 129, "type": 1, "lcn": 119}, 
            {"sid": 130, "type": 1, "lcn": 120},
            {"sid": 131, "type": 1, "lcn": 121}, 
            {"sid": 132, "type": 1, "lcn": 122}, 
            {"sid": 133, "type": 1, "lcn": 123},
            {"sid": 134, "type": 1, "lcn": 124}, 
            {"sid": 135, "type": 1, "lcn": 125}, 
            {"sid": 136, "type": 1, "lcn": 126},
            {"sid": 137, "type": 1, "lcn": 127}, 
            {"sid": 138, "type": 1, "lcn": 128}, 
            {"sid": 139, "type": 1, "lcn": 129},
            {"sid": 140, "type": 1, "lcn": 130}, 
            {"sid": 141, "type": 1, "lcn": 131}, 
            {"sid": 142, "type": 1, "lcn": 132},

        ]
    },
    {"ts": 2, 
    "services": 
        [
            {"sid": 200, "type": 1, "lcn": 11}, 
            {"sid": 201, "type": 1, "lcn": 21}, 
            {"sid": 203, "type": 1, "lcn": 31},
            {"sid": 204, "type": 1, "lcn": 41}, 
            {"sid": 205, "type": 1, "lcn": 51}, 
            {"sid": 206, "type": 1, "lcn": 61},
            {"sid": 207, "type": 1, "lcn": 71}, 
            {"sid": 208, "type": 1, "lcn": 81}, 
            {"sid": 209, "type": 1, "lcn": 91},
        ]
    },
    {"ts": 3, 
    "services": 
        [
            {"sid": 300, "type": 1, "lcn": 12}, 
            {"sid": 301, "type": 1, "lcn": 22}, 
            {"sid": 303, "type": 1, "lcn": 32},
            {"sid": 304, "type": 1, "lcn": 42}, 
            {"sid": 305, "type": 1, "lcn": 52}, 
            {"sid": 306, "type": 1, "lcn": 62},
            {"sid": 307, "type": 1, "lcn": 72}, 
            {"sid": 308, "type": 1, "lcn": 82}, 
            {"sid": 309, "type": 1, "lcn": 92},
        ]
    },
    {"ts": 4, 
    "services": 
        [
            {"sid": 400, "type": 1, "lcn": 13}, 
            {"sid": 401, "type": 1, "lcn": 23}, 
            {"sid": 403, "type": 1, "lcn": 33},
            {"sid": 404, "type": 1, "lcn": 43}, 
            {"sid": 405, "type": 1, "lcn": 53}, 
            {"sid": 406, "type": 1, "lcn": 63},
            {"sid": 407, "type": 1, "lcn": 73}, 
            {"sid": 408, "type": 1, "lcn": 83}, 
            {"sid": 409, "type": 1, "lcn": 93},
        ]
    },
    {"ts": 5, 
    "services": 
        [
            {"sid": 500, "type": 1, "lcn": 14}, 
            {"sid": 501, "type": 1, "lcn": 24}, 
            {"sid": 503, "type": 1, "lcn": 34},
            {"sid": 504, "type": 1, "lcn": 44}, 
            {"sid": 505, "type": 1, "lcn": 54}, 
            {"sid": 506, "type": 1, "lcn": 64},
            {"sid": 507, "type": 1, "lcn": 74}, 
            {"sid": 508, "type": 1, "lcn": 84}, 
            {"sid": 509, "type": 1, "lcn": 94},
        ]
    },
    {"ts": 6, 
    "services": 
        [
            {"sid": 600, "type": 1, "lcn": 15}, 
            {"sid": 601, "type": 1, "lcn": 25}, 
            {"sid": 603, "type": 1, "lcn": 35},
            {"sid": 604, "type": 1, "lcn": 45}, 
            {"sid": 605, "type": 1, "lcn": 55}, 
            {"sid": 606, "type": 1, "lcn": 65},
            {"sid": 607, "type": 1, "lcn": 75}, 
            {"sid": 608, "type": 1, "lcn": 85}, 
            {"sid": 609, "type": 1, "lcn": 95},
        ]
    },
    {"ts": 7, 
    "services": 
        [
            {"sid": 700, "type": 1, "lcn": 16}, 
            {"sid": 701, "type": 1, "lcn": 26}, 
            {"sid": 703, "type": 1, "lcn": 36},
            {"sid": 704, "type": 1, "lcn": 46}, 
            {"sid": 705, "type": 1, "lcn": 56}, 
            {"sid": 706, "type": 1, "lcn": 66},
            {"sid": 707, "type": 1, "lcn": 76}, 
            {"sid": 708, "type": 1, "lcn": 86}, 
            {"sid": 709, "type": 1, "lcn": 96},
        ]
    },
    {"ts": 8, 
    "services": 
        [
            {"sid": 800, "type": 1, "lcn": 17}, 
            {"sid": 801, "type": 1, "lcn": 27}, 
            {"sid": 803, "type": 1, "lcn": 37},
            {"sid": 804, "type": 1, "lcn": 47}, 
            {"sid": 805, "type": 1, "lcn": 57}, 
            {"sid": 806, "type": 1, "lcn": 67},
            {"sid": 807, "type": 1, "lcn": 77}, 
            {"sid": 808, "type": 1, "lcn": 87}, 
            {"sid": 809, "type": 1, "lcn": 97},
        ]
    },
    {"ts": 9, 
    "services": 
        [
            {"sid": 900, "type": 1, "lcn": 18}, 
            {"sid": 901, "type": 1, "lcn": 28}, 
            {"sid": 903, "type": 1, "lcn": 38},
            {"sid": 904, "type": 1, "lcn": 48}, 
            {"sid": 905, "type": 1, "lcn": 58}, 
            {"sid": 906, "type": 1, "lcn": 68},
            {"sid": 907, "type": 1, "lcn": 78}, 
            {"sid": 908, "type": 1, "lcn": 88}, 
            {"sid": 909, "type": 1, "lcn": 98},
        ]
    },
]






transports = [1,2,3,4,5,6,7,8,9,10]

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


#############################
# Network Information Table #
#############################

nit_sections = []

# Get list of ts_lists
sections_ts = check_length(nit_loops(services3, services)[0], services3, "NIT")

# Generate NIT sections
if len(sections_ts) != 0:

    for idx, i in enumerate(sections_ts):

        nit = network_information_section(
            network_id = 41007,
            network_descriptor_loop = nit_loops(i, services)[1], #Get first loop items
            transport_stream_loop = nit_loops(i, services)[2], #Get second loop items
            version_number = 1,
            section_number = idx,
            last_section_number = len(sections_ts) - 1
        )

        nit_sections.append(nit)

    # Write sections to nit.sec file
    with open("./nit.sec", "wb") as DFILE:
        for sec in nit_sections: 
            print (sec)
            DFILE.write(sec.pack())
else:
    pass


#############################
# Bouquet Association Table #
#############################
def BAT(bouquet_id, transports):
    bat_sections = []

    # Get list of ts_lists
    sections_ts = check_length(bat_loops(transports, services)[0], transports, "BAT")

    print (sections_ts)
    
    # Generate BAT sections
    if len(sections_ts) != 0:

        for idx, i in enumerate(sections_ts):

            bat = bouquet_association_section(
                bouquet_id = bouquet_id,
                bouquet_descriptor_loop = bat_loops(i, services)[1], #Get first loop items
                transport_stream_loop = bat_loops(i, services)[2], #Get second loop items
                version_number = 1,
                section_number = idx,
                last_section_number = len(sections_ts) - 1,
            )

            bat_sections.append(bat)

        # Write sections to bat.sec file
        with open("./bat.sec", "wb") as DFILE:
            for sec in bat_sections: 
                print (sec)
                DFILE.write(sec.pack())
    else:
        pass

bats = [{"bouquet_id": 24385, "id": 1}]

for bat in bats:
    services4 = bat_sql_main(bat["id"])
    BAT(bat["bouquet_id"], services4)
# services4 = bat_sql_main(1)
# BAT(24385, services4)

#############################################################
# Service Description Actual Table  (ETSI EN 300 468 5.2.3) #
#############################################################

sdt_sections = []

# Get list of svc_lists
sections_ts = check_length(sdt_loops(services)[0], services, "SDT Actual")

# Generate SDT sections
if len(sections_ts) != 0:

    for idx, i in enumerate(sections_ts):

        sdt = service_description_section(
            transport_stream_id = 1,
            original_network_id = 41007,
            service_loop = sdt_loops(i)[1], #Get loop items
            version_number = 1,
            section_number = idx,
            last_section_number = len(sections_ts) - 1,
        )

        sdt_sections.append(sdt)

    # Write sections to bat.sec file
    with open("./sdt_act.sec", "wb") as DFILE:
        for sec in sdt_sections: 
            print (sec)
            DFILE.write(sec.pack())
else:
    pass


#############################################################
# Service Description Other Table  (ETSI EN 300 468 5.2.3) #
#############################################################

sdt_oth_sections = []

# Get list of svc_lists
sections_ts = check_length(sdt_loops(services)[0], services, "SDT Other")

# Generate SDT sections
if len(sections_ts) != 0:

    for idx, i in enumerate(sections_ts):

        sdt = service_description_other_ts_section(
            transport_stream_id = 1,
            original_network_id = 41007,
            service_loop = sdt_loops(i)[1], #Get loop items
            version_number = 1,
            section_number = idx,
            last_section_number = len(sections_ts) - 1,
        )

        sdt_oth_sections.append(sdt)

    # Write sections to bat.sec file
    with open("./sdt_oth.sec", "wb") as DFILE:
        for sec in sdt_oth_sections: 
            print (sec)
            DFILE.write(sec.pack())
else:
    pass


###############################################
# EIT Actual Schedule (ETSI EN 300 468 5.2.4) #
###############################################

eit_schedule_sections = []

sections_ts = check_eit_length(eit_loops(events)[0], events, "EIT_Schedule")

if len(services2) != 0:

    for i in services2:

        if len(sections_ts) != 0:   

            for idx, j in enumerate(sections_ts):

                eit_schedule = event_information_section(
                    table_id = EIT_ACTUAL_TS_SCHEDULE14,
                    service_id = i,
                    transport_stream_id = 1,
                    original_network_id = 41007,
                    event_loop = eit_loops(j)[1], #Get loop items
                    segment_last_section_number = 1,
                    version_number = 1, 
                    section_number = idx,
                    last_section_number = len(sections_ts) - 1, 
                )

                eit_schedule_sections.append(eit_schedule)

            # Write sections to bat.sec file
            with open("./eit_sch.sec", "wb") as DFILE:
                for sec in eit_schedule_sections: 
                    print (sec)
                    DFILE.write(sec.pack())
        else:
            pass
else:
    pass


# ########################################################
# # EIT Actual Present/Following (ETSI EN 300 468 5.2.4) #
# ########################################################

eit_actual_pf_sections = []

sections_ts = check_eit_length(eit_loops(events2)[0], events2, "EIT_Actual_PF")

if len(sections_ts) != 0:

    for idx, i in enumerate(sections_ts):

        for jdx, j in enumerate(i):

            eit_actual_pf = event_information_section(
                table_id = EIT_ACTUAL_TS_PRESENT_FOLLOWING,
                service_id = i[0]["sid"],
                transport_stream_id = 1,
                original_network_id = 41007,
                event_loop = eit_loops([j])[1], #Get loop items
                segment_last_section_number = 1,
                version_number = 1, 
                section_number = jdx,
                last_section_number = len(i) - 1, 
            )

            eit_actual_pf_sections.append(eit_actual_pf)

    # Write sections to eit_act_pf.sec file
    with open("./eit_act_pf.sec", "wb") as DFILE:
        for sec in eit_actual_pf_sections: 
            print (sec)
            DFILE.write(sec.pack())
else:
    pass


#######################################################
# EIT Other Present/Following (ETSI EN 300 468 5.2.4) #
#######################################################

eit_other_pf_sections = []

sections_ts = check_eit_length(eit_loops(events2)[0], events2, "EIT_Other_PF")

for idx, i in enumerate(sections_ts):

    for jdx, j in enumerate(i):

        eit_other_pf = event_information_section(
            table_id = EIT_ANOTHER_TS_PRESENT_FOLLOWING,
            service_id = i[0]["sid"],
            transport_stream_id = 1,
            original_network_id = 41007,
            event_loop = eit_loops([j])[1], #Get loop items
            segment_last_section_number = 1,
            version_number = 1, 
            section_number = jdx,
            last_section_number = len(i) - 1, 
        )

        eit_other_pf_sections.append(eit_other_pf)

# Write sections to eit_oth_pf.sec file
with open("./eit_oth_pf.sec", "wb") as DFILE:
    for sec in eit_other_pf_sections: 
        print (sec)
        DFILE.write(sec.pack())


##############################################################################################
#################### Prepare time configuration for TOT and TOT tables #######################
##############################################################################################

current_time = time.gmtime()
current_local_time = time.localtime()

# italian rules
current_offset_polarity = 0x0 # positive
if current_local_time.tm_isdst == 1:
    start = 'DTSTART:%(year)04d%(month)02d%(day)02dT%(hour)02d%(minute)02d%(second)02d\n' % { 
        "year": current_time[0], 
        "month": current_time[1], 
        "day": current_time[1], 
        "hour" : 3, 
        "minute": 0, 
        "second": 0
    }
    start += 'RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10;COUNT=1' # last sunday of october
    current_offset = 0x02
    new_offset = 0x01
else :
    start = 'DTSTART:%(year)04d%(month)02d%(day)02dT%(hour)02d%(minute)02d%(second)02d\n' % { 
        "year": current_time[0], 
        "month": current_time[1], 
        "day": current_time[1], 
        "hour" : 2, 
        "minute": 0, 
        "second": 0
    }
    start += 'RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3;COUNT=1' # last sunday of march
    current_offset = 0x01
    new_offset = 0x02

change_time = list(rrulestr(start))[0]

###############################################################################################
###############################################################################################
###############################################################################################


#####################################################
#     Time Offset Table (ETSI EN 300 468 5.2.5)     #
#####################################################

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
                    year_of_change = change_time.year-1900, 
                    month_of_change = change_time.month,
                    day_of_change = change_time.day,
                    hour_of_change = int(str(((change_time.hour / 10) * 16) + (change_time.hour % 10)).split('.')[0]),
                    minute_of_change = int(str(((change_time.minute / 10) * 16) + (change_time.minute % 10)).split('.')[0]),
                    second_of_change = int(str(((change_time.second / 10) * 16) + (change_time.second % 10)).split('.')[0]),
                    next_time_offset_hour = new_offset,
                    next_time_offset_minute = 0x00
                )
            ]
        )
    ],
    year = current_time[0]-1900, # since 1900. If now 2019, then 2019 - 1900 = 119
    month = current_time[1],
    day = current_time[2],
    hour = int(str(((current_time[3] / 10) * 16) + (current_time[3] % 10)).split('.')[0]),
    minute = int(str(((current_time[4] / 10) * 16) + (current_time[4] % 10)).split('.')[0]),
    second = int(str(((current_time[5] / 10) * 16) + (current_time[5] % 10)).split('.')[0]),
    version_number = 1,
    section_number = 0,
    last_section_number = 0
    )

# Write sections to tot.sec file
with open("./tot.sec", "wb") as DFILE:
    DFILE.write(tot.pack())


####################################################
#  Time Description Table (ETSI EN 300 468 5.2.5)  #
####################################################

# TDT should be replaced at regeneration run time
    
tdt = time_date_section(
    year = current_time[0]-1900, # since 1900. If now 2019, then 2019 - 1900 = 119
    month = current_time[1],
    day = current_time[2],
    hour = int(str(((current_time[3] / 10) * 16) + (current_time[3] % 10)).split('.')[0]),
    minute = int(str(((current_time[4] / 10) * 16) + (current_time[4] % 10)).split('.')[0]),
    second = int(str(((current_time[5] / 10) * 16) + (current_time[5] % 10)).split('.')[0]),
    version_number = 1,
    section_number = 0,
    last_section_number = 0,
    )

# Write sections to tdt.sec file
with open("./tdt.sec", "wb") as DFILE:
    DFILE.write(tdt.pack())

