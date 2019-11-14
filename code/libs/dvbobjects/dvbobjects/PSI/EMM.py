#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *

######################################################################
class entitlement_management_message_section(Section):

    table_id = 0x8F
    
    section_max_size = 1024

    def pack_section_body(self):
    
        # pack program_loop_item
        pl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.emm_loop))

        self.table_id_extension = 0xFFFF

        fmt = "!%ds" % (len(pl_bytes))

        return pack(fmt, pl_bytes)

######################################################################
class emm_loop_item(DVBobject):

    def pack(self):
    
        # pack program_loop_item
        fmt = "!H"

        return pack(fmt,
            self.test)
