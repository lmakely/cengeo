__author__ = 'Lauren Makely'

import arcpy


def replace_workspace_and_save_copy(current_mxd_path, current_gdb, new_gdb, new_mxd_path):
    """
    This function will take in an mxd with broken links or different links and attempt to replace the data sources. If
    the name of a layer is different in the new data source, it will not fix the path to it. If the sources were
    broken in the mxd and there are any data sets that are not successfully pathed to the new gdb, it will print a list
    of the data sets that are still broken. For a function that will print all data sources see core/list_data_sources.

    :param current_mxd_path:    Path to the mxd with broken links
    :param current_gdb:         Path to the GDB that was used to create the mxd
    :param new_gdb:             GDB where the data resides now
    :param new_mxd_path:        Path where you want to save your new mxd. It will be saved as a copy so the name can
                                be different than the original mxd.
    :return:
    """

    mxd = arcpy.mapping.MapDocument(current_mxd_path)
    arcpy.env.overwriteOutput = True

    print("Layers in mxd:")
    for lyr in arcpy.mapping.ListLayers(mxd):
        print("\t{0}".format(lyr))
        mxd.findAndReplaceWorkspacePaths(current_gdb, new_gdb, lyr)

    print('\nBroken links in new mxd:')
    broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
    for broken_lyr in broken_list:
        print("\t{0}".format(broken_lyr))

    mxd.saveACopy(new_mxd_path)

    del mxd

if __name__ == "__main__":
    w = r'C:\Test.mxd'
    x = r'C:\testdata.gdb'
    y = r'C:\subdir\testdata2.gdb'
    z = r'C:\subdir\Test2.mxd'
    replace_workspace_and_save_copy(w, x, y, z)