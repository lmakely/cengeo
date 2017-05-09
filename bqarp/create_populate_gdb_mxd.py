__author__ = 'Lauren Makely'
# Import arcpy module

import logging
import os
import arcpy

arcpy.env.overwriteOutput = True


# function that searches through the directory to generate results
def find_files(search_folder, *search_string):
    """
    Generates a list of files that matches the search criteria.

    :param search_folder:   folder to search within
    :param search_string:   filetype to look for
    :return:                path for the files  that contain the search string
    """
    for f in os.listdir(search_folder):
        # if the extension for a file is '.zip' it gets produced
        for ext in search_string:
            if f.endswith(ext):
                yield f


def make_header(my_string, char='*'):
    """
    formats a header that will use any character and fit to any length string

    :param my_string:   string to be printed as the header
    :param char:        the character that will frame the header
    :return:

    example:
        from cengeo import core
        bas_id = "32613169140"
        print cengeo.core.make_header("BAS ID: {ID}".format(bas_id), "+")

    output example (from above):
        +++++++++++++++++++++++
        + BAS ID: 32613169140 +
        +++++++++++++++++++++++

    """
    my_string = "{c} {s} {c}".format(c=char, s=my_string)
    output = "{b}\n{s}\n{b}".format(b=char * len(my_string), s=my_string)
    return output


def format_processing_mxd(current_mxd_path, new_gdb, stcou):
    """
    This function replaces the workspace for an mxd with a new gdb. Then it saves the mxd as a new map document.

    :param current_mxd_path:    Path to the GDB that was used to create the mxd
    :param new_gdb:             GDB where the data resides now
    :return:
    """

    mxd = arcpy.mapping.MapDocument(current_mxd_path)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = new_gdb

    head, tail = os.path.split(new_gdb)
    logging.basicConfig(filename=os.path.join(head, 'create_template_log.txt'), level=logging.DEBUG, format='%(message)s')
    logging.info(make_header('Creating processing mxd for {0}'.format(stcou)))

    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.isFeatureLayer:
            fc = lyr.datasetName
            arcpy.AddMessage("Replacing workspace: {0}".format(fc))
            new_path = os.path.join(new_gdb, fc)
            if arcpy.Exists(new_path):
                lyr.replaceDataSource(new_gdb, "FILEGDB_WORKSPACE", fc)

                if lyr.name.endswith('county'):
                    df.extent = lyr.getExtent()

                if lyr.name.endswith('census_places'):
                    if lyr.symbologyType == 'UNIQUE_VALUES':
                        lyr.symbology.valueField = 'NAME'
                        lyr.symbology.addAllValues()

    print('\nBroken links in new mxd:')
    broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
    for broken_lyr in broken_list:
        logging.warning("\t{0}".format(broken_lyr))

    gdb_path, gdb = os.path.split(new_gdb)
    new_mxd_path = os.path.join(gdb_path, '{0}_{1}.mxd'.format(tail[:-4], stcou))
    mxd.saveACopy(new_mxd_path)

    del mxd


def move_originals(input_shapefiles, output_location):
    arcpy.env.overwriteOutput = True

    input_shps = input_shapefiles

    for item in input_shps:
        folder, out_name = os.path.split(item)
        out = os.path.join(output_location, out_name)
        arcpy.Copy_management(item, out)
        arcpy.Delete_management(item)


if __name__ == "__main__":
    state_folder = arcpy.GetParameterAsText(0)  # state being processed
    # DO NOT USE A STCOU ON THIS INPUT!!! Use a generic string and the stcou will be appended to it
    output_name = arcpy.GetParameterAsText(1)  # string that should be used to name the gdbs and mxds
    overwrite_val = arcpy.GetParameterAsText(2)

    arcpy.env.overwriteOutput = overwrite_val

    directory, st = os.path.split(state_folder)

    for filename in os.listdir(state_folder):
        if filename.isdigit() and len(filename) == 5:
            arcpy.AddMessage('Beginning {0}'.format(filename))
            stcou_dir = os.path.join(state_folder, filename)
            shapes = find_files(os.path.join(state_folder, filename), '.shp')

            name_format = "{0}_{1}.gdb".format(output_name, filename)
            gdb_filepath = os.path.join(stcou_dir, name_format)
            arcpy.CreateFolder_management(stcou_dir, "original_shapefiles")

            arcpy.AddMessage('...creating gdb')
            # Process: Create File GDB
            arcpy.CreateFileGDB_management(stcou_dir, name_format, "CURRENT")

            arcpy.AddMessage('...importing shapefiles')
            arcpy.AddMessage('...moving originals')
            # Process: Feature Class to Geodatabase (multiple)
            for shp in shapes:
                shapefile = os.path.join(stcou_dir, shp)
                arcpy.FeatureClassToGeodatabase_conversion(shapefile, gdb_filepath)
                move_originals([shapefile], os.path.join(stcou_dir, "original_shapefiles"))

            arcpy.AddMessage('...formatting mxd')
            template = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\preprocess_template.mxd'
            format_processing_mxd(template, gdb_filepath, filename)

            print('...completed {0}'.format(filename))