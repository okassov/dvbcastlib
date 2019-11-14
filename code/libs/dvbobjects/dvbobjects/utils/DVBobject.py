#! /usr/bin/env python

import string
import pprint

######################################################################
def CDR(s, alignment = 4, gap_byte = 0xFF):
    """If necessary, append to 's' a trailing NUL byte
    and fill with 'gap_byte' until properly aligned.
    """

    if len(s) % alignment == 0 and s[-1] in ("\x00", "\xFF"):
        return s
    s = s + "\x00"

    while len(s) % alignment:
        s = s + chr(gap_byte)
    return s					    
					    
######################################################################
class DVBobject:
    """The base class for many protocol data units.

    Basically it provides functionality similar to a C-struct.
    Members are set via keyword arguments either in the constructor
    or via the set() method. Other (rather static) attributes
    can be defined as (sub-)class attributes.

    Subclasses must implement a 'pack()' method which returns
    the properly packed byte string.

    Attributes may come from the following sources:

    1. (Static) class attributes;

    2. Keyword arguments given in the constructor;

    3. Keyword arguments given in the 'set()' method;

    4. Direct assignment to instance attributes (NOT recommended).
    """

    #
    # Default attribute value.
    # Subclasses can do that, too!
    #
    
    ISO_639_language_code = "deu"

    def __init__(self, **kwargs):
        """Initialize instance attributes from keyword arguments.
        """
        self.set(**kwargs)

    def set(self, **kwargs):
        """Add (more) instance attributes from keyword arguments.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

