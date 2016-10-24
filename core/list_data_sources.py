__author__ = 'Lauren Makely'

import arcpy


def list_data_sources(path_to_mxd):
    """

    :param path_to_mxd: path to an mxd that you want to inspect
    :return:
    """
    mxd = arcpy.mapping.MapDocument(path_to_mxd)

    lyr_list = arcpy.mapping.ListLayers(mxd)

    for lyr in lyr_list:
        if lyr.isBroken:
            link_broken = 'Yes'
        else:
            link_broken = 'No'
        print('Layer: {0}\n\tPath: {1}\n\tBroken: {2}'.format(lyr.name, lyr.dataSource, link_broken))

if __name__ == "__main__":
    w = r'C:\Test.mxd'
    list_data_sources(w)