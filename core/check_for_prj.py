__author__ = 'Lauren Makely'

import os


# check for .prj file for each changes shp. do before importing to GDB.
def check_for_prj(full_path_to_shp):
    """
    Takes in full path to a shapefile and makes sure it has an associated projection file. If there is no .prj included
    in the submission, the submitter needs to be notified or the projection assigned.

    :param full_path_to_shp:    path to a shapefile
    :return                     True (file exists)
                                False (file does not exist)
    """

    return os.path.exists(full_path_to_shp[:-3]+'prj')