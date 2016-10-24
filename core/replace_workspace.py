__author__ = 'Lauren Makely'

import arcpy


def replace_workspace_and_save_copy(current_mxd_path, current_gdb, new_gdb, new_mxd_path):
    """
    This function will take in an mxd with broken links or different links and attempt to replace the data sources. If
    the sources were broken in the mxd and there are any data sets that are not successfully pathed to the new gdb, it
    will print a list of the data sets that are still broken. For a function that will print all data sources see
    core/list_data_sources.py

    :param current_mxd_path:    Path to the mxd with broken links
    :param current_gdb:         Path to the GDB that was used to create the mxd
    :param new_gdb:             GDB where the data resides now
    :param new_mxd_path:        Path where you want to save your new mxd. It will be saved as a copy so the name can
                                be different than the original mxd.
    :return:
    """

    mxd = arcpy.mapping.MapDocument(current_mxd_path)
    arcpy.env.overwriteOutput = True

    for lyr in arcpy.mapping.ListLayers(mxd):
        print(lyr)
        mxd.findAndReplaceWorkspacePaths(current_gdb, new_gdb, lyr)

    print('\nBroken links:')
    broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
    for broken_lyr in broken_list:
        print(broken_lyr)

    mxd.saveACopy(new_mxd_path)

    del mxd

if __name__ == "__main__":
    w = r'H:\!!!HDriveStuff\Test.mxd'
    x = r'H:\!!!HDriveStuff\BQARP\testdata.gdb'
    y = r'H:\!!!HDriveStuff\BQARP\testdata2.gdb'
    z = r'H:\!!!HDriveStuff\BQARP\Test_30001.mxd'
    replace_workspace_and_save_copy(w, x, y, z)