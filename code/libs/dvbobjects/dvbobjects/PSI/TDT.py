#! /usr/bin/env python

import string
from dvbobjects.utils import *
from dvbobjects.utils.DVBobject import *
from dvbobjects.utils.MJD import *

######################################################################
class time_date_section(DVBobject):

    def pack(self):
    
        date = MJD_convert(self.year, self.month, self.day)

        fmt = "!BHHBBB"

        return pack(fmt,
            0x70,
            0x7005,
            date,
            self.hour,
            self.minute,
            self.second)
