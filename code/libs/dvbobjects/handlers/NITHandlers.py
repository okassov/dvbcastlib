from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *


####################
# Default Handlers #                                     
####################

def get_dict_key(dictionary):
    '''This function get dict as arg
    and return it's key in string format'''

    for i in dictionary.keys():
        return i


#########################################################
# Handlers for NIT First Loop (Network Descriptor Loop) #
#########################################################

def network_name_descriptor_func(items):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "descriptor_name: 
            {"descirptor_value1": descriptor_data1 }
            {"descirptor_value2": descriptor_data2 }
            {"descirptor_value3": descriptor_data3 }
    }
    Return out of network_name_descriptor
    '''

    if get_dict_key(items) == "network_name_descriptor":

        body = items["network_name_descriptor"]
        result = network_name_descriptor(
            network_name = bytes(body["network_name"], encoding="utf-8")
            )

        return result
    else:
        pass

def multilingual_network_descriptor_func(items):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "descriptor_name: 
            {"descirptor_value1": descriptor_data1 }
            {"descirptor_value2": descriptor_data2 }
            {"descirptor_value3": descriptor_data3 }
    }
    Return out of multilingual_network_descriptor
    '''

    multilingual_network_descriptor_loop = []

    if get_dict_key(items) == "multilingual_network_descriptor":

        body = items["multilingual_network_descriptor"]

        language_codes = body["ISO_639_language_code"]
        network_names = body["network_name"]

        for (code, name) in zip(language_codes, network_names):
            multilingual_network_descriptor_loop.append(
                multilingual_network_descriptor_loop_item(
                    ISO_639_language_code = bytes(code, encoding="utf-8"),
                    network_name = bytes(name, encoding="utf-8")
                )
            )

        result = multilingual_network_descriptor(
            multilingual_network_descriptor_loop = multilingual_network_descriptor_loop)

        print (len(multilingual_network_descriptor_loop))

        return result
    else:
        pass

def private_data_specifier_descriptor_func(items):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "descriptor_name: 
            {"descirptor_value1": descriptor_data1 }
            {"descirptor_value2": descriptor_data2 }
            {"descirptor_value3": descriptor_data3 }
    }
    Return out of private_data_specifier_descriptor
    '''

    if get_dict_key(items) == "private_data_specifier_descriptor":

        body = items["private_data_specifier_descriptor"]

        result = private_data_specifier_descriptor(
            private_data_specifier = body["private_data_specifier"]
            )

        return result
    else:
        pass


############################################################
# Handlers for NIT Second Loop (Transport Descriptor Loop) #
############################################################

def service_list_descriptor_func(items):

    dvb_service_descriptor_loop = []

    for item in items["descriptors"]:
        if get_dict_key(item) == "service_list_descriptor":

            body = item["service_list_descriptor"]

            service_ids = body["service_id"] # Get list of Service IDs
            service_types = body["service_type"] # Get list of Service Types

            for (sid, stype) in zip(service_ids, service_types):
                dvb_service_descriptor_loop.append(
                    service_descriptor_loop_item(
                        service_ID = sid,
                        service_type = stype
                    )
                )
        else:
            pass

    result = service_list_descriptor(dvb_service_descriptor_loop = dvb_service_descriptor_loop)

    return result


def satellite_delivery_system_descriptor_func(items):

    for item in items["descriptors"]:

        if get_dict_key(item) == "satellite_delivery_system_descriptor":

            body = item["satellite_delivery_system_descriptor"]

            result = satellite_delivery_system_descriptor(
                        frequency = body["frequency"],
                        orbital_position = body["orbital_position"],
                        west_east_flag = body["west_east_flag"],
                        polarization = body["polarization"],
                        roll_off = body["roll_off"],
                        modulation_system = body["modulation_system"],
                        modulation_type = body["modulation_type"],
                        symbol_rate = body["symbol_rate"],
                        FEC_inner = body["FEC_inner"]
                    )

            return result
        else:
            pass