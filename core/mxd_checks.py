__author__ = 'Lauren Ely'


import arcpy
import core
import os
import logging


def create_and_setup_mxd(template_mxd, where_to_save_mxd, directory_of_features):
    """

    :param where_to_save_mxd:   file path to project folder
    :param folder_to_walk:      file path to data folder. all data inside (even in a geodatabase) will be added to mxd
    :return:
    """

    logger = logging.getLogger()

    # setup mxd and map document
    arcpy.env.overwriteOutput = True
    mxd = arcpy.mapping.MapDocument(template_mxd)
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

    add_these_shps = core.find_files(directory_of_features, '.shp')
    add_these_fcs = core.find_files(directory_of_features, '.gdb')

    for gdb in add_these_fcs:
        arcpy.env.workspace = os.path.join(directory_of_features, gdb)
        fcs = arcpy.ListFeatureClasses()
        for fc in fcs:
            try:
                add_layer = arcpy.mapping.Layer(fc)
                logger.info(fc)
                arcpy.mapping.AddLayer(df, add_layer, "AUTO_ARRANGE")
            except:
                logger.info('Failed to add {} to mxd'.format(fc))
                continue

    mxd_layers = arcpy.mapping.ListLayers(mxd)

    for shp in add_these_shps:
        if shp in mxd_layers:
            pass
        else:
            try:
                add_layer = arcpy.mapping.Layer(os.path.join(directory_of_features, shp))
                logger.info(shp)
                arcpy.mapping.AddLayer(df, add_layer, "AUTO_ARRANGE")
            except:
                logger.info('Failed to add {} to mxd'.format(shp))
                continue

    output_mxd = os.path.join(where_to_save_mxd, 'BQARP_Assessment.mxd')
    logger.info('Saving mxd to {}'.format(output_mxd))
    mxd.saveACopy(output_mxd)


def list_data_sources(path_to_mxd):
    """
    Use this function to see if the file paths used in an mxd are:
        1) from the correct source
        2) broken or not

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
