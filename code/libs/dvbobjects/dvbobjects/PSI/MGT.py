#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *

######################################################################
class master_guide_section(Section):

    table_id = 0xC7
    
    section_max_size = 4096

    def pack_section_body(self):
    
        # pack tables_loop
        tl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.tables_loop))

        # pack descriptors_loop
        dl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.descriptors_loop))

        self.table_id_extension = 0
        self.private_indicator = 1

        fmt = "!BH%dsH%ds" % (len(tl_bytes), len(dl_bytes))

        return pack(fmt,
            self.ATSC_protocol_version,
            len(self.tables_loop),
            tl_bytes,
            0xF000 | (len(dl_bytes) & 0x0FFF),
            dl_bytes)

######################################################################
class table_loop_item(DVBobject):

    def pack(self):
    
        # pack transport_descriptor_loop
        dl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.descriptors_loop))

        fmt = "!HHBLH%ds" % len(dl_bytes)
        
        return pack(fmt,
            self.table_type,
            0xE000 | (self.table_type_pid & 0x1FFF),
            0xE0 | (self.table_type_version_number & 0x1F),
            self.number_bytes,
            0xF000 | (len(dl_bytes) & 0x0FFF),
            dl_bytes)
