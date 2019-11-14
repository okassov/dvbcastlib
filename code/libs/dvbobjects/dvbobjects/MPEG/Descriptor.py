#! /usr/bin/env python

from dvbobjects.utils import *

######################################################################
class Descriptor(DVBobject):
    """The base class for all Descriptors.
    Subclasses must implement a bytes() method,
    that returns the descriptor body bytes.
    """

    def pack(self):

        bytes = self.bytes()

        return pack("!BB%ds" % len(bytes),
            self.descriptor_tag,
            len(bytes),
            bytes)

