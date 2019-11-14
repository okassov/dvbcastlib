#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *
from dvbobjects.DVB.Descriptors import *
from dvbobjects.MPEG.Descriptors import *

######################################################################
class program_map_section(Section):

    table_id = 0x2
    
    section_max_size = 1024

    def pack_section_body(self):
    
        # pack program_info_descriptor_loop
        pidl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.program_info_descriptor_loop))

        # pack stream_loop
        pl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.stream_loop))

        self.table_id_extension = self.program_number
        self.private_indicator = 0

        fmt = "!HH%ds%ds" % (len(pidl_bytes), len(pl_bytes))

        return pack(fmt,
            0xE000 | (self.PCR_PID & 0x1FFF),
            0xF000 | (len(pidl_bytes) & 0x0FFF),
            pidl_bytes,
            pl_bytes)

######################################################################
class stream_loop_item(DVBobject):

    def pack(self):
    
        # pack elementary_stream_info_descriptor_loop
        esidl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.element_info_descriptor_loop))

        fmt = "!BHH%ds" % len(esidl_bytes)

        return pack(fmt,
            self.stream_type,
            0xE000 | (self.elementary_PID & 0x1FFF),
            0xF000 | (len(esidl_bytes) & 0x0FFF),
            esidl_bytes)
