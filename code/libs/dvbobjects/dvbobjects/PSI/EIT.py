#! /usr/bin/env python

import string
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils.MJD import *
from dvbobjects.DVB.Descriptors import *

EIT_ACTUAL_TS_PRESENT_FOLLOWING = 0x4E
EIT_ANOTHER_TS_PRESENT_FOLLOWING = 0x4F
EIT_ACTUAL_TS = 0x50 #to 0x5F
EIT_ANOTHER_TS = 0x60 #to 0x6F
EIT_ACTUAL_TS_SCHEDULE14 = 0x50
EIT_ACTUAL_TS_SCHEDULE58 = 0x51

######################################################################
class event_information_section(Section):
    
    section_max_size = 4096

    def pack_section_body(self):

        self.table_id_extension = self.service_id
        self.last_table_id = self.table_id
    
        # pack event_loop
        el_bytes = b"".join(
            map(lambda x: x.pack(),
            self.event_loop))

        fmt = "!HHBB%ds" % len(el_bytes)

        return pack(fmt,
            self.transport_stream_id,
            self.original_network_id,
            self.segment_last_section_number,
            self.last_table_id,
            el_bytes)

######################################################################
class event_loop_item(DVBobject):

    def pack(self):
    
        # pack event_descriptor_loop
        edl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.event_descriptor_loop))

        # convert to MJD
        date = MJD_convert(
            self.start_year, 
            self.start_month, 
            self.start_day)

        fmt = "!HHBBBBBBH%ds" % len(edl_bytes)

        return pack(fmt,
            self.event_id,
            date,
            self.start_hours,
            self.start_minutes,
            self.start_seconds,
            self.duration_hours,
            self.duration_minutes,
            self.duration_seconds,
            (self.running_status << 13) | 
            (self.free_CA_mode << 12) | 
            (len(edl_bytes) & 0x0FFF),
            edl_bytes)
