__author__ = 'Lauren Makely'

import arcpy
import logging
import os


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


def format_qa_mxd(current_mxd_path, new_gdb, new_mxd_path):
    print('stuff')

if __name__ == "__main__":
    template = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\preprocess_template.mxd'
    st_folder = arcpy.GetParameterAsText(0)
    format_processing_mxd(template, st_folder)