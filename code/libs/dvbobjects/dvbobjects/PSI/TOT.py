#! /usr/bin/env python

import string
import crcmod.predefined
from dvbobjects.utils import *
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils.MJD import *
from dvbobjects.MPEG.Section import Section
from dvbobjects.utils import *
from dvbobjects.DVB.Descriptors import *

######################################################################
class time_offset_section(DVBobject):
    
    def pack(self):
    
        date = MJD_convert(self.year, self.month, self.day)

        # pack service_stream_loop
        tl_bytes = b"".join(
            map(lambda x: x.pack(),
            self.descriptor_loop))
        
        fmt = "!BHHBBBH%ds" % len(tl_bytes) 

        data = pack(fmt,
            0x73,
            0x7000 | ((len(tl_bytes) + 11) & 0xFFF),
            date,
            self.hour,
            self.minute,
            self.second,
            0xF000 | (len(tl_bytes) & 0xFFF),
            tl_bytes)

        return data + self.crc_32_new(data)
    
    def crc_32_new(self, data):
        b = bytearray(data)
        crc32_func = crcmod.predefined.mkCrcFun('crc-32-mpeg')
        print (crc32_func(memoryview(b)))
        print (hex(crc32_func(memoryview(b))))
        crc = crc32_func(memoryview(b))

        return pack("!L", crc)
