#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *
from dvbobjects.DVB.Descriptors import *

######################################################################
class service_description_section(Section):

    table_id = 0x42
    
    section_max_size = 1024

    def pack_section_body(self):

        self.table_id_extension = self.transport_stream_id
        self.private_indicator = 1
    
        # pack service_stream_loop
        sl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.service_loop))

        fmt = "!HB%ds" % len(sl_bytes)

        return pack(fmt,
            self.original_network_id,
            0xFF,
            sl_bytes)

######################################################################
class service_description_other_ts_section(Section):

    table_id = 0x46
    
    section_max_size = 1024

    def pack_section_body(self):

        self.table_id_extension = self.transport_stream_id
        self.private_indicator = 1
    
        # pack service_stream_loop
        sl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.service_loop))

        fmt = "!HB%ds" % len(sl_bytes)

        return pack(fmt,
            self.original_network_id,
            0xFF,
            sl_bytes)

######################################################################
class service_loop_item(DVBobject):

    def pack(self):
    
        # pack service_descriptor_loop
        sdl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.service_descriptor_loop))

        fmt = "!HBH%ds" % len(sdl_bytes)

        return pack(fmt,
            self.service_ID,
            0xFC | (self.EIT_schedule_flag << 1) | 
            (self.EIT_present_following_flag),
            (self.running_status << 13) | 
            (self.free_CA_mode << 12) | 
            (len(sdl_bytes) & 0x0FFF),
            sdl_bytes)
