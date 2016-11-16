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


def format_processing_mxd(current_mxd_path, new_gdb):
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
    arcpy.env.workspace = new_gdb

    head, tail = os.path.split(new_gdb)
    proj, stcou = tail[:-4].split('_')
    logging.info(make_header('Creating processing mxd for {0}'.format(stcou)))

    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.isFeatureLayer:
            print(lyr.name)
            if lyr.name.endswith('msp'):
                data_set = 'npc_bqarp_2016_{0}_msp_addr_t13'.format(stcou)
                if arcpy.Exists(os.path.join(arcpy.env.workspace, data_set)):
                    print(os.path.join(arcpy.env.workspace, data_set))
                    lyr.replaceDataSource(new_gdb,
                                          "FILEGDB_WORKSPACE",
                                          data_set)

            elif lyr.name.endswith('edges'):
                data_set = 'npc_bqarp_2016_{0}_edge_vw'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          "FILEGDB_WORKSPACE",
                                          data_set)

            elif lyr.name.endswith('offset'):
                data_set = 'npc_bqarp_2016_{0}_offset'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('parcels'):
                data_set = 'npc_bqarp_2016_{0}_parcel_data'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('cousub'):
                data_set = 'npc_bqarp_2016_{0}_cousub_v90'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('county'):
                data_set = 'npc_bqarp_2016_{0}_county_v90'.format(stcou)
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('areawater'):
                data_set = 'npc_bqarp_2016_{0}_areawater'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('places_union'):
                data_set = 'npc_bqarp_2016_{0}_places_union'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('counties_union'):
                data_set = 'npc_bqarp_2016_{0}_counties_union'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('census_places'):
                data_set = 'npc_bqarp_2016_{0}_census_places'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('local_places'):
                data_set = 'npc_bqarp_2016_{0}_local_places'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

            elif lyr.name.endswith('discrepancies_places'):
                data_set = 'npc_bqarp_2016_{0}_places_discrepancies'.format(stcou)
                print(os.path.join(arcpy.env.workspace, data_set))
                if arcpy.Exists(data_set):
                    lyr.replaceDataSource(arcpy.env.workspace,
                                          'FILEGDB_WORKSPACE',
                                          data_set)

    print('\nBroken links in new mxd:')
    broken_list = arcpy.mapping.ListBrokenDataSources(mxd)
    for broken_lyr in broken_list:
        logging.warning("\t{0}".format(broken_lyr))

    # change this before giving it to maddie
    bqarp = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP'
    st = stcou[0:2]
    new_mxd_path = os.path.join(bqarp, st, stcou, '{0}_processing.mxd'.format(stcou))
    mxd.saveACopy(new_mxd_path)

    del mxd

def format_qa_mxd(current_mxd_path, new_gdb, new_mxd_path):
    print('stuff')

if __name__ == "__main__":
    template = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\preprocess_template.mxd'
    stcou_gdb = arcpy.GetParameterAsText(0)  # r'H:\!!!HDriveStuff\BQARP\20\20005\bqarp_20005.gdb'
    format_processing_mxd(template, stcou_gdb)