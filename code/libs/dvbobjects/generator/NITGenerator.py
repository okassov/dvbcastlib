import os
from dvbobjects.utils.SectionLength import *
from dvbobjects.utils.Write import *
from dvbobjects.PSI.NIT import *
from SQL.NITSQL import *
from SQL.SQLMain import *


#############################
# Network Information Table #
#############################


def nit(network_object_id, network_id, network_data):

    nit_file_name = "output\\nit_" + str(network_object_id) + ".sec"
    nit_sections = []

    # Get list of ts_lists
    sections_ts = check_length(
        nit_loops(
            network_data, 
            network_id)[0], 
        network_data, 
        "NIT", 
        network_id = network_id)

    # Generate NIT sections
    if len(sections_ts) != 0:

        for idx, i in enumerate(sections_ts):

            nit = network_information_section(
                network_id = network_id,
                network_descriptor_loop = nit_loops(
                    i, 
                    network_id = network_id)[1], # Get first loop items
                transport_stream_loop = nit_loops(
                    i, 
                    network_id = network_id)[2], # Get second loop items
                version_number = 1,
                section_number = idx,
                last_section_number = len(sections_ts) - 1
            )
            nit_sections.append(nit)

        write_section(nit_file_name, nit_sections)

    else:
        pass


def regenerate_all_nit():
    '''This function regenerate all NIT'''

    all_networks = get_all_networks()

    networks = [ 
        {
            "network_object_id": network[0], 
            "network_id": network[1]
        } for network in all_networks 
    ]

    for network in networks:
        network_data = sql_api_nit(network["network_object_id"], network["network_id"]) # Get network information with transports 
        if network_data != None and len(network_data["transports"]) != 0:
            nit(network["network_object_id"], network["network_id"], network_data) # Generate Sections
            null_list("NIT") # Null section list for next loop
        else:
            print ("Not found any transports in network with ID: " + str(network["network_object_id"]))


def regenerate_changed_nit(network_object_ids):
    '''This function regenerate changed NIT'''

    changed_networks = []

    for object_id in network_object_ids:
        changed_networks.append(get_network(object_id))

    if len(changed_networks) != 0:

        networks = [ 
            {
                "network_object_id": network[0], 
                "network_id": network[1]
            } for network in changed_networks 
        ]

        for network in networks:
            network_data = sql_api_nit(network["network_object_id"], network["network_id"]) # Get network information with transports 
            if network_data != None and len(network_data["transports"]) != 0:
                nit(network["network_object_id"], network["network_id"], network_data) # Generate Sections
                null_list("NIT") # Null section list for next loop
            else:
                print ("Not found any transports in network with ID: " + str(network["network_object_id"]))
                pass
    else:
        print ("Error! Not found any networks.")
        pass