from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *
from .DefaultHandlers import *

############################################################
# Handlers for NIT Second Loop (Transport Descriptor Loop) #
############################################################


def service_descriptor_func(items):
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

    if get_dict_key(items) == "service_descriptor":

        body = items["service_descriptor"]

        stype = body["service_type"]
        spname = bytes(body["service_provider_name"], encoding="utf-8")
        sname = bytes(body["service_name"], encoding="utf-8")

        result = service_descriptor(
                service_type = stype,
                service_provider_name = spname ,
                service_name = sname
            )

        return result
    else:
        pass


