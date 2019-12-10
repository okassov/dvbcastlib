import os
from dvbobjects.utils.SectionLength import *
from dvbobjects.utils.Write import *
from dvbobjects.PSI.BAT import *
from SQL.EITActualPFSQL import *
from SQL.EITOtherPFSQL import *
from SQL.EITActualScheduleSQL import *
from SQL.SQLMain import *


########################################################
# EIT Actual Present/Following (ETSI EN 300 468 5.2.4) #
########################################################


def eit_actual_pf(transport_id, services):

    eit_file_name = "output\\eit_act_pf_" + str(transport_id) + ".sec"
    eit_actual_pf_sections = []

    for i in services:
        
        if len(i["events"]) != 0:  

            for idx, j in enumerate(i["events"]):
                eit_actual_pf = event_information_section(
                    table_id = EIT_ACTUAL_TS_PRESENT_FOLLOWING,
                    service_id = i["service_id"],
                    transport_stream_id = transport_id,
                    original_network_id = 41007,
                    event_loop = eit_loops([j], i["descriptors"]), #Get loop items
                    segment_last_section_number = len(i["events"]) - 1,
                    version_number = 1, 
                    section_number = idx,
                    last_section_number = len(i["events"]) - 1, 
                )
                eit_actual_pf_sections.append(eit_actual_pf)

            write_section(eit_file_name, eit_actual_pf_sections)

        else:
            pass
    else:
        pass


def regenerate_all_eit_actual_pf():
    '''This function regenerate all EIT Actaul Present/Following'''

    all_transports = get_all_transports()

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in all_transports 
    ]

    for transport in transports:
        transport_data = sql_api_eit_pf(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            eit_actual_pf(transport["transport_object_id"], transport_data)
            null_list("EIT Actual PF")
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass


########################################################
# EIT Actual Present/Following (ETSI EN 300 468 5.2.4) #
########################################################


def eit_actual_schedule(transport_id, services):

    eit_file_name = "output\\eit_act_sch_" + str(transport_id) + ".sec"

    eit_actual_schedule_sections = []

    sections_ts = []
    
    for svc in services:
        chunks = event_chunks_list(svc["events"])

        for i in chunks:

            temp_chunk = []
            
            for j in i:
                temp_chunk.append(j)
            sections_ts.append(
                {
                    "id": svc["id"], 
                    "service_id": svc["service_id"], 
                    "descriptors": svc["descriptors"], 
                    "events": [i for i in temp_chunk]
                }
            )

    if len(sections_ts) != 0:

        for idx, i in enumerate(sections_ts):

            eit_actual_schedule = event_information_section(
                table_id = EIT_ACTUAL_TS_SCHEDULE14,
                service_id = i["service_id"],
                transport_stream_id = transport_id,
                original_network_id = 41007,
                event_loop = eit_loops(i["events"], i["descriptors"]), #Get loop items
                segment_last_section_number = len(sections_ts) - 1,
                version_number = 1, 
                section_number = idx,
                last_section_number = len(sections_ts) - 1, 
            )
            eit_actual_schedule_sections.append(eit_actual_schedule)

        write_section(eit_file_name, eit_actual_schedule_sections)

    else:
        pass


def regenerate_all_eit_actual_schedule():
    '''This function regenerate all EIT Actual Schedule'''

    all_transports = get_all_transports()

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in all_transports 
    ]

    for transport in transports:
        transport_data = sql_api_eit_schedule(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            eit_actual_schedule(transport["transport_object_id"], transport_data)
            null_list("EIT Actual Schedule")
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass


#######################################################
# EIT Other Present/Following (ETSI EN 300 468 5.2.4) #
#######################################################


def eit_other_pf(transports):
    
    eit_file_name = "output\\eit_oth_pf_" + str(1) + ".sec"
    eit_other_pf_sections = []

    for transport in transports:
        
        for i in transport["services"]:

            if len(i["events"]) != 0:

                for idx, j in enumerate(i["events"]):

                    eit_other_pf = event_information_section(
                        table_id = EIT_ANOTHER_TS_PRESENT_FOLLOWING,
                        service_id = i["service_id"],
                        transport_stream_id = transport["ts"],
                        original_network_id = 41007,
                        event_loop = eit_loops([j], i["descriptors"]), #Get loop items
                        segment_last_section_number = len(i["events"]) - 1,
                        version_number = 1, 
                        section_number = idx,
                        last_section_number = len(i["events"]) - 1, 
                    )

                    eit_other_pf_sections.append(eit_other_pf)

    write_section(eit_file_name, eit_other_pf_sections)


def regenerate_all_eit_other_pf():
    '''This function regenerate all EIT Other Present/Following'''

    all_transports = get_all_transports()

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in all_transports 
    ]

    all_transport_data = []
    for transport in transports:
        transport_data = sql_api_eit_other_pf(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            all_transport_data.append(transport_data)
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass
    if len(all_transport_data) != 0:
        eit_other_pf(all_transport_data)
        null_list("EIT Other PF")
    else:
        print ("Not found any transport with services")