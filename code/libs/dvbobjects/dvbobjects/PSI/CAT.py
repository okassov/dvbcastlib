#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *

######################################################################
class conditional_access_section(Section):

    table_id = 0x01
    
    section_max_size = 1024

    def pack_section_body(self):
    
        # pack ca_descriptor_loop
        pl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.ca_descriptor_loop))

        self.table_id_extension = 0xFFFF

        fmt = "!%ds" % (len(pl_bytes))
        
        return pack(fmt, pl_bytes)

