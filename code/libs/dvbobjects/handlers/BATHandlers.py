from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *
from .DefaultHandlers import *
import itertools # Need for iterate nds_e4_descriptor, because it's have 3 list


#########################################################
# Handlers for NIT First Loop (Network Descriptor Loop) #
#########################################################

def bouquet_name_descriptor_func(descriptor):
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

    if get_dict_key(descriptor) == "bouquet_name_descriptor":

        if len(descriptor["bouquet_name_descriptor"]) != 0:

            body = descriptor["bouquet_name_descriptor"]
            result = bouquet_name_descriptor(
                bouquet_name = bytes(body["bouquet_name"], encoding="utf-8")
                )
        else:
            result = None

        return result
    else:
        return None

############################################################
# Handlers for NIT Second Loop (Transport Descriptor Loop) #
############################################################

# def service_list_descriptor_func(descriptor):
#     '''This function get dict as arg.
#     Input dict format ===>
#     {
#         "ts": id,
#         "descriptors:
#             [ 
#                 {
#                     "descriptor1_name": 
#                         {
#                         "descirptor1_value1": descriptor_data1,
#                         "descirptor1_value2": descriptor_data2,
#                         "descirptor1_value3": descriptor_data3,
#                         ...
#                         },
#                 },
#                 {
#                     "descriptor2_name": 
#                         {
#                         "descirptor2_value1": descriptor_data1,
#                         "descirptor2_value2": descriptor_data2,
#                         "descirptor2_value3": descriptor_data3,
#                         ...
#                         },
#                 },
#                 ...  
#             ]
#     }
#     Return out of service_list_descriptor
#     '''

#     dvb_service_descriptor_loop = []

#     for item in descriptor["descriptors"]:
#         if get_dict_key(item) == "service_list_descriptor":

#             body = item["service_list_descriptor"]

#             service_ids = body["service_id"] # Get list of Service IDs
#             service_types = body["service_type"] # Get list of Service Types

#             for (sid, stype) in zip(service_ids, service_types):
#                 dvb_service_descriptor_loop.append(
#                     service_descriptor_loop_item(
#                         service_ID = sid,
#                         service_type = stype
#                     )
#                 )
#         else:
#             pass
#     result = service_list_descriptor(dvb_service_descriptor_loop = dvb_service_descriptor_loop)

#     return result


def nds_e2_descriptor_func(descriptor):
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

    nds_e2_descriptor_loop = []

    if get_dict_key(descriptor) == "nds_e2_descriptor":

        if len(descriptor["nds_e2_descriptor"]) != 0:
            body = descriptor["nds_e2_descriptor"]

            for service in body:
                nds_e2_descriptor_loop.append(
                    nds_e2_descriptor_loop_item(
                        service_ID = service["service_id"],
                        logical_channel_number = service["logical_channel_number"]
                    )
                )
            result = nds_e2_descriptor(nds_e2_descriptor_loop = nds_e2_descriptor_loop)
        else:
            result = None

        return result
    else:
        return None




def nds_e4_descriptor_func(descriptor):
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
    nds_e4_descriptor_loop = []

    if get_dict_key(descriptor) == "nds_e4_descriptor":

        if len(descriptor) != 0:

            body = descriptor["nds_e4_descriptor"]

            for service in body:
                nds_e4_descriptor_loop.append(
                    nds_e4_descriptor_loop_item(
                        service_ID = service["service_id"],
                        general_order = service["general_order"],
                        order_by_type = service["order_by_type"]
                    )
                )
            result = nds_e4_descriptor(nds_e4_descriptor_loop = nds_e4_descriptor_loop)
        else:
            result = None
        return result
    else:
        return None

