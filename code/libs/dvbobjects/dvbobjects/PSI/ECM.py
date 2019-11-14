#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *

######################################################################
class entitlement_control_message_section(Section):

    table_id = 0x80
    
    section_max_size = 1024

    def pack_section_body(self):
    
        # pack program_loop_item
        pl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.ecm_loop))

        self.table_id_extension = 0xFFFF

        fmt = "!%ds" % (len(pl_bytes))

        return pack(fmt, pl_bytes)

######################################################################
class ecm_loop_item(DVBobject):

    def pack(self):
    
        # pack program_loop_item
        fmt = "!HHHHHHHH"
        
        return pack(fmt,
            self.cw1_1,
            self.cw1_2,
            self.cw1_3,
            self.cw1_4,
            self.cw2_1,
            self.cw2_2,
            self.cw2_3,
            self.cw2_4)
