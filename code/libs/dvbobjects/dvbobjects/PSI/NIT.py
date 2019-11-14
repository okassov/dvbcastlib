#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *
from dvbobjects.DVB.Descriptors import *

######################################################################
class network_information_section(Section):

    table_id = 0x40
    
    section_max_size = 1024

    def pack_section_body(self):
    
        # pack network_descriptor_loop
        ndl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.network_descriptor_loop))

        # pack transport_stream_loop
        tsl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.transport_stream_loop))

        self.table_id_extension = self.network_id
        self.private_indicator = 1

        fmt = "!H%dsH%ds" % (len(ndl_bytes), len(tsl_bytes))

        return pack(fmt,
            0xF000 | (len(ndl_bytes) & 0x0FFF),
            ndl_bytes,
            0xF000 | (len(tsl_bytes) & 0x0FFF),
            tsl_bytes)

######################################################################
class transport_stream_loop_item(DVBobject):

    def pack(self):
    
        # pack transport_descriptor_loop
        tdl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.transport_descriptor_loop))

        fmt = "!HHH%ds" % len(tdl_bytes)

        return pack(fmt,
            self.transport_stream_id,
            self.original_network_id,
            0xF000 | (len(tdl_bytes) & 0x0FFF),
            tdl_bytes)
