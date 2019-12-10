import os
from dvbobjects.utils.SectionLength import *
from dvbobjects.utils.Write import *
from dvbobjects.PSI.SDT import *
from SQL.SDTActualSQL import *
from SQL.SDTOtherSQL import *
from SQL.SQLMain import *



#############################################################
# Service Description Actual Table  (ETSI EN 300 468 5.2.3) #
#############################################################


def sdt_actual(transport_id, services):

    sdt_file_name = "output\\sdt_act_" + str(transport_id) + ".sec"

    sdt_sections = []

    # Get list of svc_lists
    sections_ts = check_length_sdt(
        sdt_loops(
            services)[0], 
        services,
        transport_id,
        "SDT Actual")

    # Generate SDT sections
    if len(sections_ts) != 0:

        for idx, i in enumerate(sections_ts):

            sdt = service_description_section(
                transport_stream_id = transport_id,
                original_network_id = 41007,
                service_loop = sdt_loops(i)[1], #Get loop items
                version_number = 1,
                section_number = idx,
                last_section_number = len(sections_ts) - 1,
            )

            sdt_sections.append(sdt)

        write_section(sdt_file_name, sdt_sections)

    else:
        pass


def regenerate_all_sdt_actual():
    '''This function regenerate all SDT Actual'''

    all_transports = get_all_transports()

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in all_transports 
    ]

    for transport in transports:
        transport_data = sql_api_sdt_actual(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            sdt_actual(transport["transport_object_id"], transport_data)
            null_list("SDT Actual")
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass


def regenerate_changed_sdt_actual(transport_object_ids):
    '''This function regenerate all SDT Actual'''

    changed_transports = []

    for object_id in transport_object_ids:
        changed_transports.append(get_transport(object_id))

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in changed_transports 
    ]

    for transport in transports:
        transport_data = sql_api_sdt_actual(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            sdt_actual(transport["transport_object_id"], transport_data)
            null_list("SDT Actual")
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass



############################################################
# Service Description Other Table  (ETSI EN 300 468 5.2.3) #
############################################################


def sdt_other(transports):

    sdt_file_name = "output\\sdt_oth_" + str(1) + ".sec"
    sdt_oth_sections = []

    for transport in transports:

        # Get list of svc_lists
        sections_ts = check_length_sdt(
                    sdt_loops(transport["services"])[0], 
                    transport["services"],
                    transport["ts"],
                    "SDT Other")

        # Generate SDT sections
        if len(sections_ts) != 0:

            for idx, i in enumerate(sections_ts):

                sdt = service_description_other_ts_section(
                    transport_stream_id = transport["ts"],
                    original_network_id = 41007,
                    service_loop = sdt_loops(i)[1], #Get loop items
                    version_number = 1,
                    section_number = idx,
                    last_section_number = len(sections_ts) - 1,
                )
                sdt_oth_sections.append(sdt)

        else:
            pass

    write_section(sdt_file_name, sdt_oth_sections)


def regenerate_all_sdt_other():
    '''This function regenerate all SDT Other'''

    all_transports = get_all_transports()

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in all_transports 
    ]

    all_transport_data = []
    for transport in transports:
        transport_data = sql_api_sdt_other(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            all_transport_data.append(transport_data)
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass
    if len(all_transport_data) != 0:
        sdt_other(all_transport_data)
        null_list("SDT Other")
    else:
        print ("Not found any transport with services")    


def regenerate_changed_sdt_other(transport_object_ids):
    '''This function regenerate all SDT Other'''

    changed_transports = []

    for object_id in transport_object_ids:
        changed_transports.append(object_id)

    transports = [ 
        {
            "transport_object_id": transport[0], 
        } for transport in all_transports 
    ]

    all_transport_data = []
    for transport in transports:
        transport_data = sql_api_sdt_other(transport["transport_object_id"])
        if transport_data != None and len(transport_data) != 0:
            all_transport_data.append(transport_data)
        else:
            print ("Not found any services in transport with ID: " + str(transport["transport_object_id"]))
            pass
    if len(all_transport_data) != 0:
        sdt_other(all_transport_data)
        null_list("SDT Other")
    else:
        print ("Not found any transport with services") 