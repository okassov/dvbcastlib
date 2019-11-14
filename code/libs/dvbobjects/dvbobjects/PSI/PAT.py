#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import *
from dvbobjects.utils import *

######################################################################
class program_association_section(Section):

    table_id = 0x00
    
    section_max_size = 1024

    def pack_section_body(self):
    
        # pack program_loop_item
        pl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.program_loop))

        self.table_id_extension = self.transport_stream_id # ???
        self.private_indicator = 0

        fmt = "!%ds" % (len(pl_bytes))

        return pack(fmt, pl_bytes)

######################################################################
class program_loop_item(DVBobject):

    def pack(self):
    
        # pack program_loop_item
        fmt = "!HH"

        return pack(fmt,
            self.program_number,
            0xE000 | (self.PID & 0x1FFF))
