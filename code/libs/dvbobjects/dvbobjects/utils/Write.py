

def write_section(section_filename, sections):
    '''This function write sections to file
    with .sec format as byte'''

    # Write sections to .sec file
    with open(section_filename, "wb") as DFILE:
        for sec in sections: 
            print (sec)
            DFILE.write(sec.pack())
            DFILE.flush()