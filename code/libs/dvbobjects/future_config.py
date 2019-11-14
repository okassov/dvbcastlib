#! /usr/bin/env python

import os
from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.PSI.BAT import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *


test_transport_stream_id = 1
test_original_transport_stream_id = 1
test1_service_id = 1


services = {10: 1, 20: 1, 30: 1, 40: 1, 50: 1, 60: 1, 70: 1, 80: 1, 90: 1,
            11: 1, 21: 1, 31: 1, 41: 1, 51: 1, 61: 1, 71: 1, 81: 1, 91: 1,
            12: 1, 22: 1, 32: 1, 42: 1, 52: 1, 62: 1, 72: 1, 82: 1, 92: 1,
            13: 1, 23: 1, 33: 1, 43: 1, 53: 1, 63: 1, 73: 1, 83: 1, 93: 1,
            14: 1, 24: 1, 34: 1, 44: 1, 54: 1, 64: 1, 74: 1, 84: 1, 94: 1,
            15: 1, 25: 1, 35: 1, 45: 1, 55: 1, 65: 1, 75: 1, 85: 1, 95: 1,
            16: 1, 26: 1, 36: 1, 46: 1, 56: 1, 66: 1, 76: 1, 86: 1, 96: 1,
            17: 1, 27: 1, 37: 1, 47: 1, 57: 1, 67: 1, 77: 1, 87: 1, 97: 1,
            18: 1, 28: 1, 38: 1, 48: 1, 58: 1, 68: 1, 78: 1, 88: 1, 98: 1,
            19: 1, 29: 1, 39: 1, 
}


#############################
# Network Information Table #
#############################


nit = network_information_section(
    network_id = 41007,
    network_descriptor_loop = [
        network_descriptor(network_name = b"Marat Network",),
        multilingual_network_descriptor(
            multilingual_network_descriptor_loop = [
                multilingual_network_descriptor_loop_item(
                    ISO_639_language_code = b"rus",
                    network_name = b"Kazteleradio"
                )
            ]
        ),
        private_data_specifier_descriptor(private_data_specifier = 24577),
    ],
    transport_stream_loop = [
        transport_stream_loop_item(
            transport_stream_id = test_transport_stream_id,
            original_network_id = test_original_transport_stream_id,
            transport_descriptor_loop = [
                service_list_descriptor(
                    dvb_service_descriptor_loop = [
                        service_descriptor_loop_item(
                             service_ID = key, 
                             service_type = value,
                        ) for key, value in services.items()
                        # service_descriptor_loop_item(
                        #     service_ID = test1_service_id, 
                        #     service_type = 1, # digital tv service type
                        # ),
                    ],
                ),
                transport_stream_sat_descriptor(
                    frequency = 1211141313,
                    orbital_position = 5850,
                    west_east_flag = 1,
                    polarization = 3,
                    roll_off = 0,
                    modulation_system = 1,
                    modulation_type = 1,
                    symbol_rate = 30,
                    FEC_inner = 3)
            ],        
        ),
    ],
    version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
    section_number = 0,
    last_section_number = 0,
)




bat = bouquet_association_section(
    bouquet_id = 24385,
    bouquet_descriptor_loop = [
        bouquet_name_descriptor(bouquet_name = b"Subscriber BAT [0x5F41]")
    ],
    transport_stream_loop = [
        transport_stream_loop_item(
            transport_stream_id = test_transport_stream_id,
            original_network_id = test_original_transport_stream_id,
            transport_descriptor_loop = [
                service_list_descriptor(
                    dvb_service_descriptor_loop = [
                        service_descriptor_loop_item(
                            service_ID = test1_service_id, 
                            service_type = 1, # digital tv service type
                        ),
                    ],
                )
            ]
        )
    ],
    version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
    section_number = 0,
    last_section_number = 0,
)











out = open("./nit.sec", "wb")
out.write(nit.pack())
out.close
out = open("./nit.sec", "wb") # python  flush bug
out.close
os.system('/usr/local/bin/sec2ts 16 < ./nit.sec > ./firstnit.ts')

out = open("./bat.sec", "wb")
out.write(bat.pack())
out.close
out = open("./bat.sec", "wb") # python  flush bug
out.close
os.system('/usr/local/bin/sec2ts 17 < ./bat.sec > ./firstbat.ts')

