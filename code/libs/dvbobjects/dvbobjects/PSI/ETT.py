#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.ATSC.Loops import *
from dvbobjects.utils.MJD import *

######################################################################
class extended_text_table_section(Section):

    table_id = 0xCC

    section_max_size = 4093

    def pack_section_body(self):
        
        self.table_id_extension = self.ETT_table_id_extension
        self.protocol_version = 0
        
        extended_text_message_bytes = self.extended_text_message.pack()
        
        fmt = "!BL%ds" % len(extended_text_message_bytes)

        return pack(fmt,
            self.protocol_version,
            self.ETM_id,
            extended_text_message_bytes)

