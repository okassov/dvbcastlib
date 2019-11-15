#! /usr/bin/env python

import os
from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.PSI.BAT import *
from dvbobjects.utils.LengthCalculate import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *


test_transport_stream_id = 1
test_transport_stream_id_2 = 2
test_transport_stream_id_3 = 3
test_transport_stream_id_4 = 4
test_transport_stream_id_5 = 5
test_transport_stream_id_6 = 6
test_original_transport_stream_id = 1
test1_service_id = 1


services = [[100, 1], [200, 1], [300, 1], [400, 1], [500, 1], [600, 1], [700, 1], [800, 1], [900, 1],
            [110, 1], [210, 1], [310, 1], [410, 1], [510, 1], [610, 1], [710, 1], [810, 1], [910, 1],
            [120, 1], [220, 1], [320, 1], [420, 1], [520, 1], [620, 1], [720, 1], [820, 1], [920, 1],
            [130, 1], [230, 1], [330, 1], [430, 1], [530, 1], [630, 1], [730, 1], [830, 1], [930, 1],
            [140, 1], [240, 1], [340, 1], [440, 1], [540, 1], [640, 1], [740, 1], [840, 1], [940, 1],
            [150, 1], [250, 1], [350, 1], [450, 1], [550, 1], [650, 1], [750, 1], [850, 1], [950, 1],
            [160, 1], [260, 1], [360, 1], [460, 1], [560, 1], [660, 1], [760, 1], [860, 1], [960, 1],
            [170, 1], [270, 1], [370, 1], [470, 1], [570, 1], [670, 1], [770, 1], [870, 1], [970, 1],
            [180, 1], [280, 1], [380, 1], [480, 1], [580, 1], [680, 1], [780, 1], [880, 1], [980, 1],
            [190, 1], [290, 1], [390, 1], [490, 1]]

transports = [1,2,3,4,5,6,7,8,9,10,11]


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
                             service_ID = i[0], 
                             service_type = i[1],
                        ) for i in services
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

############################################################################

check_length(bat_loops_length(transports, services), transports)


# if check_length(bat_loops_length(transports, services)):
#     print ("Section OK")
# else:
#     if len(transports) == 1:
#         print ("Need decrease transport_descriptor_loop length")
#     else:
#         print (split_list(transports))
#         for i in split_list(transports):
#             if check_length(bat_loops_length(i, services)):
#                 print("LENGTH OK")
#             else:
#                 print ("LENGTH FALSE")
############################################################################



# bat = bouquet_association_section(
#     bouquet_id = 24385,
#     bouquet_descriptor_loop = bdl,
#     transport_stream_loop = tdl,
#     version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
#     section_number = 0,
#     last_section_number = 0,
# )











# out = open("./nit.sec", "wb")
# out.write(nit.pack())
# out.close
# out = open("./nit.sec", "wb") # python  flush bug
# out.close
# os.system('/usr/local/bin/sec2ts 16 < ./nit.sec > ./firstnit.ts')

# out = open("./bat.sec", "wb")
# out.write(bat.pack())
# out.close
# out = open("./bat.sec", "wb") # python  flush bug
# out.close
# os.system('/usr/local/bin/sec2ts 17 < ./bat.sec > ./firstbat.ts')

