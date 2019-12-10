import os
from dvbobjects.utils.SectionLength import *
from dvbobjects.utils.Write import *
from dvbobjects.PSI.BAT import *
from SQL.BATSQL import *
from SQL.SQLMain import *


#############################
# Bouquet Association Table #
#############################


def bat(bouquet_id, network_id, bat_data):

    bat_file_name = "output\\bat_" + str(bouquet_id) + ".sec"
    bat_sections = []

    # Get list of ts_lists
    sections_ts = check_length(
        bat_loops(
            bat_data,
            bouquet_id,
            network_id)[0], 
        bat_data, 
        "BAT",
        bouquet_id = bouquet_id,
        network_id = network_id)

    # Generate BAT sections
    if len(sections_ts) != 0:

        for idx, i in enumerate(sections_ts):

            bat = bouquet_association_section(
                bouquet_id = bouquet_id,
                bouquet_descriptor_loop = bat_loops(
                    i,
                    bouquet_id,
                    network_id)[1], #Get first loop items
                transport_stream_loop = bat_loops(
                    i,
                    bouquet_id,
                    network_id)[2], #Get second loop items
                version_number = 1,
                section_number = idx,
                last_section_number = len(sections_ts) - 1,
            )

            bat_sections.append(bat)

        write_section(bat_file_name, bat_sections)

    else:
        pass


def regenerate_all_bat():
    '''This function regenerate all BAT'''

    all_bouquets = get_all_bouquets()

    bouquets = [
        {
            "bouquet_object_id": bouquet[0],
            "bouquet_id": bouquet[1],
            "network_id": bouquet[2]
        } for bouquet in all_bouquets
    ]

    for bouquet in bouquets:
        bouquet_data = sql_api_bat(bouquet["bouquet_object_id"], bouquet["bouquet_id"])
        if bouquet_data != None and len(bouquet_data) != 0:
            bat(bouquet["bouquet_id"], bouquet["network_id"], bouquet_data)
            null_list("BAT") # Null section list for next loop
        else:
            print ("Not found any transports in bouquet with ID: " + str(bouquet["bouquet_object_id"]))
            pass


def regenerate_changed_bat(bouquet_object_ids):
    '''This function regenerate all BAT'''

    changed_bouquets = []

    for object_id in bouquet_object_ids:
        changed_bouquets.append(get_bouquet(object_id))

    bouquets = [
        {
            "bouquet_object_id": bouquet[0],
            "bouquet_id": bouquet[1],
            "network_id": bouquet[2]
        } for bouquet in changed_bouquets
    ]

    for bouquet in bouquets:
        bouquet_data = sql_api_bat(bouquet["bouquet_object_id"], bouquet["bouquet_id"])
        if bouquet_data != None and len(bouquet_data) != 0:
            bat(bouquet["bouquet_id"], bouquet["network_id"], bouquet_data)
            null_list("BAT") # Null section list for next loop
        else:
            print ("Not found any transports in bouquet with ID: " + str(bouquet["bouquet_object_id"]))
            pass