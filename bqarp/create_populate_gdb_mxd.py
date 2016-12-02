__author__ = 'Lauren Makely'
# Import arcpy module
import sys
sys.path.insert(0, r'H:\GitHub\cengeo\core')

import stcou_codes
import os
import arcpy


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


def format_processing_mxd(current_mxd_path, new_gdb):
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
    proj, stcou = tail[:-4].split('_')
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

    # change this before giving it to maddie
    bqarp = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP'
    st = stcou[0:2]
    new_mxd_path = os.path.join(bqarp, st, stcou, '{0}_processing.mxd'.format(tail[:-4]))
    mxd.saveACopy(new_mxd_path)

    del mxd


def move_originals(input_shapefiles, output_location):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = input_shapefiles

    input_shps = arcpy.env.workspace
    output_folder = output_location

    for item in input_shps.split(';'):
        arcpy.AddMessage('Moving originals...')
        folder, out_name = os.path.split(item)
        out = os.path.join(output_folder, out_name)
        arcpy.Copy_management(item, out)
        arcpy.Delete_management(item)


if __name__ == "__main__":
    Output_File_GDB_Location = arcpy.GetParameterAsText(0)  # folder the gdb, originals folder, and mxd should be placed
    Output_GDB_and_MXD_Name = arcpy.GetParameterAsText(1)  # string that should be used to name the gdb and mxd
    Input_Features = arcpy.GetParameterAsText(2)  # list of shps to add to the gdb and move

    state_folder = arcpy.GetParameterAsText(0)  # state being processed
    directory, st = os.path.split(state_folder)
    stcou = '{0}001'.format(st)

    if os.path.join(state_folder, stcou, 'original_shapefiles'):
        overwrite_value = raw_input('Overwrite existing data? y/n?')
        if overwrite_value == 'Y' or overwrite_value == 'y':
            arcpy.env.overwriteOutput = True
        else:
            arcpy.env.overwriteOutput = False

    for stcou in stcou.st:
        # Local variables:
        Original_Shapefiles = Output_File_GDB_Location
        Derived_Geodatabase = Output_File_GDB_Location

        # Process: Create File GDB
        arcpy.CreateFileGDB_management(Output_File_GDB_Location, Output_GDB_and_MXD_Name, "CURRENT")

        # Process: Feature Class to Geodatabase (multiple)
        arcpy.FeatureClassToGeodatabase_conversion(Input_Features, Output_File_GDB_Location)

        # Process: Create Folder
        tempEnvironment0 = arcpy.env.workspace
        arcpy.env.workspace = Derived_Geodatabase
        arcpy.CreateFolder_management(Output_File_GDB_Location, "original_shapefiles")
        arcpy.env.workspace = tempEnvironment0

        move_originals(Input_Features, Original_Shapefiles)

        template = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\preprocess_template.mxd'
        format_processing_mxd(template, Derived_Geodatabase)