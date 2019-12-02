from Generator import *
from SQL.DVBActiveTables import *
from SQL.SQLMain import *
from SQL.BATSQL import *
from SQL.NITSQL import *
from SQL.EITActualPFSQL import *
from SQL.EITOtherPFSQL import *
from SQL.EITActualScheduleSQL import *
from SQL.SDTActualSQL import *
from SQL.SDTOtherSQL import *



def regenerate_all_tables():
    '''This function regenerate all 
    DVB tables. Then user activate
    button Regenerate ALL'''

    active_dvb_tables = get_active_dvb_tables()
    print (active_dvb_tables)
    

    for table in active_dvb_tables:

        table_name = table[0]

        # NIT DVB Table
        if table_name == "NIT":
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
                    pass
        

        # BAT DVB Table
        if table_name == "BAT":
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


        # SDT Actual Table
        if table_name == "SDT Actual":
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
    

        # SDT Other Table
        if table_name == "SDT Other":
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


        # EIT Actual Present Following Table
        if table_name == "EIT Actual Present Following":
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


        # EIT Actual Schedule Table
        if table_name == "EIT Actual Schedule":
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


        # EIT Other Present Following Table
        if table_name == "EIT Other Present Following":
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


def main(action):

	if action == "All":
		regenerate_all_tables()
	elif action == "Changed":
		regenerate_changed_tables()
	else:
		pass


main("All")
