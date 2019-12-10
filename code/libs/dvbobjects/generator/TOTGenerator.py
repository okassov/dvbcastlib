import os
from dvbobjects.utils.Write import *
from dvbobjects.utils.datetime import *
from dvbobjects.PSI.TOT import *


#############################################
# Time Offset Table (ETSI EN 300 468 5.2.5) #
#############################################

def tot():

    file_name = os.path.join("output", "tot", "tot.sec")
    directory = os.path.dirname(file_name)

    current_time = get_datetime()[0]
    change_time = get_datetime()[1]
    new_offset = get_datetime()[2]

    tot = time_offset_section(
        descriptor_loop = [
            local_time_offset_descriptor(
                local_time_offset_loop = [
                    local_time_offset_loop_item(
                        ISO_639_language_code = b'kaz',
                        country_region_id = 1,
                        local_time_offset_polarity = 0,
                        local_time_offset_hour = 6,
                        local_time_offset_minute = 0,
                        year_of_change = change_time.year-1900, 
                        month_of_change = change_time.month,
                        day_of_change = change_time.day,
                        hour_of_change = int(str(((change_time.hour / 10) * 16) + (change_time.hour % 10)).split('.')[0]),
                        minute_of_change = int(str(((change_time.minute / 10) * 16) + (change_time.minute % 10)).split('.')[0]),
                        second_of_change = int(str(((change_time.second / 10) * 16) + (change_time.second % 10)).split('.')[0]),
                        next_time_offset_hour = new_offset,
                        next_time_offset_minute = 0x00
                    )
                ]
            )
        ],
        year = current_time[0]-1900, # since 1900. If now 2019, then 2019 - 1900 = 119
        month = current_time[1],
        day = current_time[2],
        hour = int(str(((current_time[3] / 10) * 16) + (current_time[3] % 10)).split('.')[0]),
        minute = int(str(((current_time[4] / 10) * 16) + (current_time[4] % 10)).split('.')[0]),
        second = int(str(((current_time[5] / 10) * 16) + (current_time[5] % 10)).split('.')[0]),
        version_number = 1,
        section_number = 0,
        last_section_number = 0
        )

    if not os.path.exists(directory):
        os.makedirs(file_name)

        # Write sections to tot.sec file
        with open(file_name, "wb") as DFILE:
            DFILE.write(tot.pack())
            DFILE.flush()

    else:

        # Write sections to tdt.sec file
        with open(file_name, "wb") as DFILE:
            DFILE.write(tot.pack())
            DFILE.flush()