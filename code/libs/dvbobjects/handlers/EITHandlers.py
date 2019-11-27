from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *
from .DefaultHandlers import *
import itertools # Need for iterate nds_e4_descriptor, because it's have 3 list


#########################################################
# Handlers for NIT First Loop (Network Descriptor Loop) #
#########################################################

def component_descriptor_func(items):
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

    if get_dict_key(items) == "component_descriptor":

        if len(items["component_descriptor"]) != 0:

            body = items["component_descriptor"]
            result = component_descriptor(
                stream_content = body["stream_content"],
                component_type = body["component_type"],
                component_tag = body["component_tag"],
                ISO_639_language_code = bytes(body["ISO_639_language_code"], encoding="utf-8"),
                text_char = bytes(body["text_char"], encoding="utf-8")
                )
        else:
            result = None

        return result
    else:
        pass


def ca_identifier_descriptor_func(items):
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

    if get_dict_key(items) == "ca_identifier_descriptor":

        if len(items["ca_identifier_descriptor"]) != 0:

            body = items["ca_identifier_descriptor"]
            result = ca_identifier_descriptor(
                ca_identifier_descriptor_loop = [
                    ca_identifier_descriptor_loop_item(
                        ca_system_id = body["ca_system_id"]
                    ) 
                ]
            )
        else:
            result = None

        return result
    else:
        pass


def parental_rating_descriptor_func(items):
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

    if get_dict_key(items) == "parental_rating_descriptor":

        if len(items["parental_rating_descriptor"]) != 0:

            body = items["parental_rating_descriptor"]
            result = parental_rating_descriptor(
                country_code = bytes(body["country_code"], encoding="utf-8"),
                rating = body["rating"]
                )
        else:
            result = None

        return result
    else:
        pass

def short_event_descriptor_func(items):
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

    if get_dict_key(items) == "short_event_descriptor":

        if len(items["short_event_descriptor"]) != 0:

            body = items["short_event_descriptor"]
            result = short_event_descriptor(
                ISO_639_language_code = bytes(body["ISO_639_language_code"], encoding="utf-8"),
                event_name = bytes(body["event_name"], encoding="utf-8"),
                text = bytes(body["text"], encoding="utf-8")
                )
        else:
            result = None

        return result
    else:
        pass


def extended_event_descriptor_func(items):
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

    if get_dict_key(items) == "extended_event_descriptor":

        if len(items["extended_event_descriptor"]) != 0:

            body = items["extended_event_descriptor"]
            result = extended_event_descriptor(
                descriptor_number = body["descriptor_number"],
                last_descriptor_number = body["last_descriptor_number"],
                ISO_639_language_code = bytes(body["ISO_639_language_code"], encoding="utf-8"),
                extended_event_loop = [
                    extended_event_loop_item(
                        item = b"",
                        item_description = b""
                    )
                ],
                text = bytes(body["text"], encoding="utf-8")
                )
        else:
            result = None

        return result
    else:
        pass