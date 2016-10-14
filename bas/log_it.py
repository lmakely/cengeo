__author__ = 'makel004'

import os


def log_it(connection, bas_id, filename, folder, state, subtype, counties, errors, timestamp, shp_dict):
    """
    # Creates a log file for processor to review.
    File is saved as a .txt within the working directory.

    Inputs:
        connection: SQL table to log changes in?
        bas_id:     5 digit code that corresponds to entity
        filename:   name of file being processed
        folder:     dir that the filename is within
        state:      state (code?) that entity lies in
        subtype:    (no idea - LMM)
        counties:   list of affected counties for this set of changes
        errors:     list of errors encountered
        timestamp:  pull from system
        shp_dict:
    """
    # creates and opens text file for logging errors
    f = open(os.path.join(folder, 'log.txt'), 'w')
    # inserts BAS ID at the top of the txt file
    f.write(bas_id + '\n')

    # prints list of errors if there are any to text file
    if errors:
        f.write('errors: \n')
        for x in errors:  # loops through the list of errors and inserts them on a new line
            f.write('    ' + str(x) + '\n')

    # writes the submission type to the text file
    f.write('Submission Type:\n    ' + str(subtype) + '\n')

    # any intersecting counties are written to file here and if there aren't any, puts none
    if counties:
        f.write('Affected counties:\n\n')
        f.write(','.join(counties))
        f.write('\n\n')
    else:
        f.write('Affected counties:\n    None\n')

    try:  # fix this up later?
        connection.execute("insert into ENTITIES values(?,?,?,?,?,?,?,?);", (bas_id,
                                                                             filename,
                                                                             folder,
                                                                             state,
                                                                             subtype,
                                                                             str(counties),
                                                                             str(errors),
                                                                             timestamp))
    except:  # fix this up later?
        pass

    # checks attributes based on type of file and outputs lists of missing values
    if shp_dict:
        f.write('==Shapefile Summary==============================\n')
        for shp, values in shp_dict.iteritems():
            connection.execute("insert into SHAPEFILES values(?,?,?,?,?,?,?,?);", (bas_id,
                                                                                   filename,
                                                                                   shp,
                                                                                   str(values['changetype']),
                                                                                   str(values['GDBFC']),
                                                                                   str(values['fldErrors']),
                                                                                   str(values['valueErrors']),
                                                                                   str(values['prj'])))
            f.write('Shapefile:\n    {0}\n'.format(shp))  # prints path of file that was processed (print just the name?)
            f.write('Change Type:\n    ' + str(values['changetype']) + '\n')  # type of geography changed
            if values['fldErrors']:  # checks FOR required fields in shapefile
                f.write('Expected field(s) missing:\n')
                for v in values['fldErrors']:
                    f.write('    ' + str(v) + '\n')
            if values['valueErrors']:  # checks for missing/inconsistent data IN required fields
                f.write('values missing from key fields:\n')
                if values['changetype'] in ['ln', 'hydroa', 'plndk', 'alndk']:
                    f.write('* FEAT_ID is a stand-in for TLID, AREAID, POINTID, or HYDROID depending on layer\n')
                    f.write('    FID | FULLNAME | CHNG_TYPE | RELATE | MTFCC | FEAT_ID* | PROBLEM \n')
                else:
                    f.write('    FID | NAME | CHNG_TYPE | EFF_DATE | DOCU | AREA | RELATE | PROBLEM \n')
                for v in values['valueErrors']:
                    if type(v) == type(('',)):
                        f.write('    ' + ' | '.join(list(str(x) for x in v)) + '\n')
                    else:
                        f.write('    ' + str(v) + '\n')

            if values['prj'] is False:  # checks that shp has a projection
                f.write('!Missing .PRJ file!\n')

            if values['GDBFC']:
                f.write('layer name in GDB:\n    '+values['GDBFC']+'\n')

            f.write('=================================================\n')
    connection.commit()
    f.close()