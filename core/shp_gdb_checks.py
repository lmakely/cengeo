__author__ = 'Lauren Ely'

import os
import arcpy


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


def desc_shp(shp):
    """
    prints list of filed names and their types.
    :param shp: esri shapefile
    :return:    list of attribute fields

    example output:
    NAME       TYPE
    ====================
    FID        OID
    Shape      Geometry
    OBJECTID_1 Integer
    OBJECTID   Integer
    STATEFP    String
    COUNTYFP   String
    ====================
    """

    print('{:10s} {}'.format('NAME', 'TYPE'))
    print('====================')
    for f in arcpy.ListFields(shp):
        print('{:10s} {}'.format(f.name, f.type))
    print('====================')


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


def merge_files(input_datasets, output_dataset):
    """
    Merges together a set of polygons into one polygon dataset. Input should consist of filepaths to each
    polygon.

    :param input_datasets:  list of feature classes or shapefiles to be merged into one output. must all be
                            of similar geometries
    :param output_dataset:  file path and name of output dataset
    :return:
    """
    output_folder, name = os.path.split(output_dataset)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    arcpy.Merge_management(input_datasets, output_dataset, "")


def get_and_project(working_dir, file_to_project, input_file):
    """
    !!!!HAS NOT BEEN TESTED SINCE FORMATTING!!!
    this is not done but already figured out. wanted to preserve the info and clean up later into a real function.

    :param working_dir:     folder files will be put in
    :param file_to_project: path to file to project? or just the name?
    :param input_file:      file to get projection information from
    :return:
    """
    # project data
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    path, old_name = os.path.split(file_to_project)
    new_name = "{}_projected.shp".format(old_name[:-4])
    final_out_name = os.path.join(working_dir, new_name)

    targetDescribe = arcpy.Describe(input_file)
    targetSR = targetDescribe.SpatialReference
    arcpy.Project_management(file_to_project, final_out_name, targetSR)



