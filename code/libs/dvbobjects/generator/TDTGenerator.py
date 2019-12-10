import os
from dvbobjects.utils.Write import *
from dvbobjects.utils.datetime import *
from dvbobjects.PSI.TDT import *


##################################################
# Time Description Table (ETSI EN 300 468 5.2.5) #
##################################################

# TDT should be replaced at regeneration run time

def tdt():

    file_name = os.path.join("output", "tdt", "tdt.sec")
    directory_name = os.path.join("output", "tdt")
    directory = os.path.dirname(file_name)

    current_time = get_datetime()[0]
    change_time = get_datetime()[1]
    
    tdt = time_date_section(
        year = current_time[0]-1900, # since 1900. If now 2019, then 2019 - 1900 = 119
        month = current_time[1],
        day = current_time[2],
        hour = int(str(((current_time[3] / 10) * 16) + (current_time[3] % 10)).split('.')[0]),
        minute = int(str(((current_time[4] / 10) * 16) + (current_time[4] % 10)).split('.')[0]),
        second = int(str(((current_time[5] / 10) * 16) + (current_time[5] % 10)).split('.')[0]),
        version_number = 1,
        section_number = 0,
        last_section_number = 0,
        )

    if not os.path.exists(directory):
        os.makedirs(file_name)

        # Write sections to tdt.sec file
        with open(file_name, "wb") as DFILE:
            DFILE.write(tdt.pack())
            DFILE.flush()

    else:

        # Write sections to tdt.sec file
        with open(file_name, "wb") as DFILE:
            DFILE.write(tdt.pack())
            DFILE.flush()