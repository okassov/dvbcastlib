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

def network_name_descriptor_func(descriptor):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "descriptor_name: 
            {
            "descirptor_value1": descriptor_data1,
            "descirptor_value2": descriptor_data2,
            "descirptor_value3": descriptor_data3,
            ...
            }
    }
    Return out of network_name_descriptor
    '''

    if get_dict_key(descriptor) == "network_name_descriptor":

        if len(descriptor["network_name_descriptor"]):

            body = descriptor["network_name_descriptor"]
            result = network_name_descriptor(
                network_name = bytes(body["network_name"], encoding="utf-8")
                )
        else:
            result = None

        return result
    else:
        return None

def multilingual_network_descriptor_func(descriptor):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "descriptor_name: 
            {
            "descirptor_value1": descriptor_data1,
            "descirptor_value2": descriptor_data2,
            "descirptor_value3": descriptor_data3,
            ...
            }
    }
    Return out of multilingual_network_descriptor
    '''

    multilingual_network_descriptor_loop = []

    if get_dict_key(descriptor) == "multilingual_network_descriptor":

        if len(descriptor["multilingual_network_descriptor"]) != 0:
            body = descriptor["multilingual_network_descriptor"]
            for name in body:
                multilingual_network_descriptor_loop.append(
                    multilingual_network_descriptor_loop_item(
                        ISO_639_language_code = bytes(name["ISO_639_language_code"], encoding="utf-8"),
                        network_name = bytes(name["network_name"], encoding="utf-8")
                    )
                )
            result = multilingual_network_descriptor(
                multilingual_network_descriptor_loop = multilingual_network_descriptor_loop)
        else:
            result = None

        return result
    else:
        return None


############################################################
# Handlers for NIT Second Loop (Transport Descriptor Loop) #
############################################################

def service_list_descriptor_func(descriptor):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "ts": id,
        "descriptors:
            [ 
                {
                    "descriptor1_name": 
                        {
                        "descirptor1_value1": descriptor_data1,
                        "descirptor1_value2": descriptor_data2,
                        "descirptor1_value3": descriptor_data3,
                        ...
                        },
                },
                {
                    "descriptor2_name": 
                        {
                        "descirptor2_value1": descriptor_data1,
                        "descirptor2_value2": descriptor_data2,
                        "descirptor2_value3": descriptor_data3,
                        ...
                        },
                },
                ...  
            ]
    }
    Return out of service_list_descriptor
    '''

    dvb_service_descriptor_loop = []

    if get_dict_key(descriptor) == "service_list_descriptor":
        if len(descriptor["service_list_descriptor"]) != 0:

            body = descriptor["service_list_descriptor"]
            for service in body:
                dvb_service_descriptor_loop.append(
                    service_descriptor_loop_item(
                        service_ID = service["service_id"],
                        service_type = service["service_type"]
                    )
                )
            result = service_list_descriptor(dvb_service_descriptor_loop = dvb_service_descriptor_loop)
        else:
            result = None

        return result
    else:
        return None


def satellite_delivery_system_descriptor_func(descriptor):
    '''This function get dict as arg.
    Input dict format ===>
    {
        "ts": id,
        "descriptors:
            [ 
                {
                    "descriptor1_name": 
                        {
                        "descirptor1_value1": descriptor_data1,
                        "descirptor1_value2": descriptor_data2,
                        "descirptor1_value3": descriptor_data3,
                        ...
                        },
                },
                {
                    "descriptor2_name": 
                        {
                        "descirptor2_value1": descriptor_data1,
                        "descirptor2_value2": descriptor_data2,
                        "descirptor2_value3": descriptor_data3,
                        ...
                        },
                },
                ...  
            ]
    }
    Return out of service_list_descriptor
    '''

    if get_dict_key(descriptor) == "satellite_delivery_system_descriptor":
        if len(descriptor["satellite_delivery_system_descriptor"]) != 0:
            body = descriptor["satellite_delivery_system_descriptor"]
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
        else:
            result = None

        return result
    else:
        return None