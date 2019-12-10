from generator.NITGenerator import *
from generator.BATGenerator import *
from generator.SDTGenerator import *
from generator.EITGenerator import *
from generator.TDTGenerator import *
from generator.TOTGenerator import *
from SQL.SQLMain import *


def regenerate_all_tables():
    '''This function regenerate all 
    DVB tables. Then user activate
    button Regenerate ALL'''

    active_dvb_tables = get_active_dvb_tables()

    for table in active_dvb_tables:

        table_name = table[0]

        # if table_name == "NIT":
        #     regenerate_all_nit()
        
        # elif table_name == "BAT":
        #     regenerate_all_bat()

        # elif table_name == "SDT Actual":
        #     regenerate_all_sdt_actual()
    
        # elif table_name == "SDT Other":
        #     regenerate_all_sdt_other()

        # elif table_name == "EIT Actual Present Following":
        #     regenerate_all_eit_actual_pf()

        # elif table_name == "EIT Actual Schedule":
        #     regenerate_all_eit_actual_schedule()

        # elif table_name == "EIT Other Present Following":
        #     regenerate_all_eit_other_pf()

        if table_name == "TDT":
            tdt()

        elif table_name == "TOT":
            tot()

        else:
            print ("Error! Unknown DVB Table")
            pass


def regenerate_changed_tables():

    changed_dvb_tables = []

    # for table in changed_dvb_tables:


def main(action):

    if action == "All":
        regenerate_all_tables()
    elif action == "Changed":
        regenerate_changed_tables()
    else:
        pass


main("All")
