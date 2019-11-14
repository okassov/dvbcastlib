#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *
from dvbobjects.DVB.Descriptors import *

######################################################################
class update_notification_section(Section):

    table_id = 0x4B
    
    section_max_size = 4096

    def pack_section_body(self):
    
        self.table_id_extension = self.action_type << 8 | 
            ((self.OUI >> 16) ^ 
            ((self.OUI >> 8) & 0xFF) ^ 
            (self.OUI & 0xFF))
        
        # pack common_descriptor_loop
        common_bytes = b"".join(
            map(lambda x: x.pack(),
            self.common_descriptor_loop))

        # pack compatibility_descriptor_loop
        compatibility_bytes = b"".join(
            map(lambda x: x.pack(),
            self.compatibility_descriptor_loop))

        fmt = "!HBBH%ds%ds" % (len(common_bytes), len(compatibility_bytes))

        return pack(fmt,
            self.OUI >> 8,
            self.OUI & 0xFF,
            self.processing_order,
            0xF000 | len(common_bytes),
            common_bytes,
            compatibility_bytes)

######################################################################
class unt_compatibility_descriptor_loop_item(DVBobject):

    def pack(self):
    
        # pack target_descriptor_loop
        tdl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.target_descriptor_loop))
            
        # pack operational descriptor_loop
        odl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.operational_descriptor_loop))
        
        fmt = "!%dsHH%dsH%ds" % (
            len(self.compatibility_descriptor), 
            len(tdl_bytes), 
            len(odl_bytes))

        return pack(fmt,
            self.compatibility_descriptor,
            len(tdl_bytes) + len(odl_bytes),
            0xF000 | len(tdl_bytes),
            tdl_bytes,
            0xF000 | len(odl_bytes),
            odl_bytes)
