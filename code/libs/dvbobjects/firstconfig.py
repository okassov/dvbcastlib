#! /usr/bin/env python

import os

from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *


test_transport_stream_id = 1
test_original_transport_stream_id = 1
test1_service_id = 1
test1_pmt_pid = 1031


#############################
# Network Information Table #
#############################

nit = network_information_section(
    network_id = 1,
    network_descriptor_loop = [
        network_descriptor(network_name = b"Marat Network",), 
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
                ),
            ],        
        ),
    ],
    version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
    section_number = 0,
    last_section_number = 0,
)


#######################################################
# Program Association Table (ISO/IEC 13818-1 2.4.4.3) #
#######################################################

pat = program_association_section(
    transport_stream_id = test_transport_stream_id,
    program_loop = [
        program_loop_item(
            program_number = test1_service_id,
            PID = test1_pmt_pid,
        ),  
        program_loop_item(
            program_number = 0, # special program for the NIT
            PID = 16,
        ), 
    ],
    version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
    section_number = 0,
    last_section_number = 0,
)


#####################################################
# Service Description Table (ETSI EN 300 468 5.2.3) #
#####################################################

sdt = service_description_section(
    transport_stream_id = test_transport_stream_id,
    original_network_id = test_original_transport_stream_id,
    service_loop = [
        service_loop_item(
            service_ID = test1_service_id,
            EIT_schedule_flag = 0, # 0 no current even information is broadcasted, 1 broadcasted
            EIT_present_following_flag = 0, # 0 no next event information is broadcasted, 1 is broadcasted
            running_status = 4, # 4 service is running, 1 not running, 2 starts in a few seconds, 3 pausing
            free_CA_mode = 0, # 0 means service is not scrambled, 1 means at least a stream is scrambled
            service_descriptor_loop = [
                service_descriptor(
                    service_type = 1, # digital television service
                    service_provider_name = b"Marat Provider",
                    service_name = b"Marat Service 1",
                ),    
            ],
        ),    
    ],
    version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
    section_number = 0,
    last_section_number = 0,
)



###############################################
# Program Map Table (ISO/IEC 13818-1 2.4.4.8) #
###############################################

pmt = program_map_section(
    program_number = test1_service_id,
    PCR_PID = 2064,
    program_info_descriptor_loop = [],
    stream_loop = [
        stream_loop_item(
            stream_type = 2, # mpeg2 video stream type
            elementary_PID = 2064,
            element_info_descriptor_loop = []
        ),
        stream_loop_item(
            stream_type = 4, # mpeg2 audio stream type
            elementary_PID = 2068,
            element_info_descriptor_loop = []
        ),
    ],
    version_number = 1, # you need to change the table number every time you edit, so the decoder will compare its version with the new one and update the table
    section_number = 0,
    last_section_number = 0,
)    

#
# PSI marshalling and encapsulation
#

out = open("./nit.sec", "wb")
out.write(nit.pack())
out.close
out = open("./nit.sec", "wb") # python  flush bug
out.close
os.system('/usr/local/bin/sec2ts 16 < ./nit.sec > ./firstnit.ts')

out = open("./pat.sec", "wb")
out.write(pat.pack())
out.close
out = open("./pat.sec", "wb") # python   flush bug
out.close
os.system('/usr/local/bin/sec2ts 0 < ./pat.sec > ./firstpat.ts')

out = open("./sdt.sec", "wb")
out.write(sdt.pack())
out.close
out = open("./sdt.sec", "wb") # python   flush bug
out.close
os.system('/usr/local/bin/sec2ts 17 < ./sdt.sec > ./firstsdt.ts')

out = open("./pmt.sec", "wb")
out.write(pmt.pack())
out.close
out = open("./pmt.sec", "wb") # python   flush bug
out.close
os.system('/usr/local/bin/sec2ts ' + str(test1_pmt_pid) + ' < ./pmt.sec > ./firstpmt.ts')

