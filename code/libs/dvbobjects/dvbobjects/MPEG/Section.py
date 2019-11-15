#! /usr/bin/env python

from dvbobjects.utils import *
import crcmod.predefined

######################################################################
class Section(DVBobject):
    """The base class of many PSI/SI Sections.

    It implements the general layout of all(?) PSI/SI
    sections with 'syntax_indicator' == 1.

    Constant Attributes:

      - 'section_syntax_indicator' = 1,

      - 'current_next_indicator' = 1.

    Attributes to be provided by subclasses:

      - 'table_id'

      - 'table_id_extension'

    Attributes to be provided by other means (e.g. using 'set()'):

      - 'version_number'

      - 'section_number'

      - 'last_section_number'

    Computed Attributes:

      - 'section_length'

      - 'crc_32'
    
    Subclasses must implement a 'pack_section_body()' method.
    """
    section_max_size = 4096
    section_syntax_indicator = 1
    private_indicator = 0
    current_next_indicator = 1

    def __sanity_check(self):

        print ("Section Length =====> " + str(self.section_length))

        assert self.section_syntax_indicator == 1
        assert self.current_next_indicator in (0, 1)
        assert 0 <= self.table_id <= 0xff
        assert 0 <= self.table_id_extension <= 0xffff
        assert 0 <= self.section_length <= self.section_max_size - 3
        assert 0 <= self.section_number <= 0xFF
        assert 0 <= self.last_section_number <= 0xFF

    def pack(self):
    
        body = self.pack_section_body()
        
        self.section_length = (
            5                           # section header rest
            + len(body)                 # section body
            + 4                         # CRC32
            )
        length_info_16 = (
            0xB000
            | (self.section_syntax_indicator<<15)
            | (self.private_indicator << 14)
            | (self.section_length)
            )
        version_info_8 = (
            0xC0
            | ((self.version_number & 0x01f) << 1)
            | (self.current_next_indicator)
            )

        self.__sanity_check()

        data = pack("!BHHBBB",
            self.table_id,
            length_info_16,
            self.table_id_extension,
            version_info_8,
            self.section_number,
            self.last_section_number) + body

        return data + self.crc_32_new(data)

    def crc_32(self, data):

        crc = crc32.CRC_32(data)
        
        return pack("!L", crc)

    def crc_32_new(self, data):
        b = bytearray(data)
        crc32_func = crcmod.predefined.mkCrcFun('crc-32-mpeg')
        print (crc32_func(memoryview(b)))
        print (hex(crc32_func(memoryview(b))))
        crc = crc32_func(memoryview(b))

        return pack("!L", crc)
