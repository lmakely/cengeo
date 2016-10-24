__author__ = 'makel004'

import os


def log_it(connection, bas_id, filename, folder, state, subtype, counties, errors, timestamp, shp_dict):
    """
    This probably should get broken down into a log function and a BAS specific format function. That way the log
    function can be used for all projects and not just BAS. Could even break it down into multiple checks that get
    called in a BAS specific log so those can be used for other projects? Or instead of saving all these args in other
    functions, have the log file open then and append those errors to it? - LMM

    Creates a log file for processor to review.
    File is saved as a .txt within the working directory.

    :param connection:  SQL table to log changes in?
    :param bas_id:      5 digit code that corresponds to entity
    :param filename:    name of file being processed
    :param folder:      dir that the filename is within
    :param state:       state (code?) that entity lies in
    :param subtype:     (no idea - LMM)
    :param counties:    list of affected counties for this set of changes
    :param errors:      list of errors encountered
    :param timestamp:   pull from system
    :param shp_dict:    pulled from bas.dicts to check values
    """
    # creates and opens text file for logging errors
    f = open(os.path.join(folder, 'log.txt'), 'w')
    # inserts BAS ID at the top of the txt file
    f.write(bas_id + '\n')

    # prints list of errors if there are any to text file
    if errors:
        f.write('errors: \n')
        for x in errors:  # loops through the list of errors and inserts them on a new line
            f.write('    {0}\n'.format(x))

    # writes the submission type to the text file
    f.write('Submission Type:\n    {sub}\n'.format(subtype))

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

            f.write('Shapefile:\n    {shp}\n'.format(shp))  # prints path of file that was processed (print just the name?)
            f.write('Change Type:\n    {chng}\n'.format(values['changetype']))  # type of geography changed
            if values['fldErrors']:  # checks FOR required fields in shapefile
                f.write('Expected field(s) missing:\n')
                for v in values['fldErrors']:
                    f.write('    {fields}\n'.format(v))
            if values['valueErrors']:  # checks for missing/inconsistent data IN required fields
                f.write('values missing from key fields:\n')
                if values['changetype'] in ['ln', 'hydroa', 'plndk', 'alndk']:
                    f.write('* FEAT_ID is a stand-in for TLID, AREAID, POINTID, or HYDROID depending on layer\n')
                    f.write('    FID | FULLNAME | CHNG_TYPE | RELATE | MTFCC | FEAT_ID* | PROBLEM \n')
                else:
                    f.write('    FID | NAME | CHNG_TYPE | EFF_DATE | DOCU | AREA | RELATE | PROBLEM \n')

                # address this section
                for v in values['valueErrors']:
                    if type(v) == type(('',)):
                        f.write('    ' + ' | '.join(list(str(x) for x in v)) + '\n')
                    else:
                        f.write('    {val)\n'.format(v))

            if values['prj'] is False:  # checks that shp has a projection
                f.write('!Missing .PRJ file!\n')

            if values['GDBFC']:
                f.write('layer name in GDB:\n    {gdb}\n'.format(values['GDBFC']))

            f.write('=================================================\n')
    connection.commit()
    f.close()