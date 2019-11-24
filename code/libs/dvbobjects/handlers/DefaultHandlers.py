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

def private_data_specifier_descriptor_func(items, loop):
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
    Return out of private_data_specifier_descriptor
    '''
    if loop == "first":
        #print (items)
        if get_dict_key(items) == "private_data_specifier_descriptor":
            body = items["private_data_specifier_descriptor"]

            result = private_data_specifier_descriptor(
                private_data_specifier = body["private_data_specifier"]
                )
            return result
        else:
            pass

    elif loop == "second":
        for item in items["descriptors"]:
            if get_dict_key(item) == "private_data_specifier_descriptor":
                body = item["private_data_specifier_descriptor"]
                result = private_data_specifier_descriptor(
                    private_data_specifier = body["private_data_specifier"]
                )
                return result
            else:
                pass