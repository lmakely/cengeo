__author__ = 'Lauren Makely'

import arcpy
import os
import logging
import core


def clip_county_by_selection(census_county_file, local_file, output_folder):
    """
    Goes through a state county file and clips an input file to each county boundary. Used by BQARP to clip local
    data to census data.

    :param census_county_file:  lisrds county file
    :param local_file:          local boundary files to be split
    :param: output_folder:      base folder to put outputs. will create new folders for each split place.
    """

    arcpy.env.workspace = output_folder  # the state BQARP folder

    local_lyr = arcpy.MakeFeatureLayer_management(local_file)
    census_counties_lyr = arcpy.MakeFeatureLayer_management(census_county_file)

    logging.info('Beginning to split places by county')
    with arcpy.da.SearchCursor(census_counties_lyr, field_names=['STATEFP', 'COUNTYFP']) as cursor:
        for row in cursor:

            county_fp = '{0}{1}'.format(row[0], row[1])
            expression = """ "COUNTYFP" = '{0}' """.format(row[1])

            selection = arcpy.SelectLayerByAttribute_management(census_counties_lyr, "NEW_SELECTION", expression)
            clip_name = 'census_places_{0}.shp'.format(county_fp)
            output_path = os.path.join(output_folder, county_fp, clip_name)

            if not os.path.exists(os.path.join(output_folder, county_fp)):
                os.mkdir(os.path.join(output_folder, county_fp))

            select_by_location = arcpy.SelectLayerByLocation_management(local_lyr, "WITHIN", selection)
            num_selected_records = arcpy.Describe(select_by_location)

            if len(num_selected_records.fidSet.split(";")) > 0:
                arcpy.Clip_analysis(local_lyr, selection, output_path)
                print('Completed clipping: {}'.format(county_fp))

    logging.info('Completed splitting places')


def merge_counties(input_datasets, output_dataset):
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


if __name__ == '__main__':
    BQARP_HQ = r'P:\BAS\CARP\BQARP'
    BQARP_ME = 'H:\!!!HDriveStuff\BQARP'
    where_ever_lisrds_goes = r''

    stcou = raw_input('Enter 5 digit stcou code. If processing a statewide submission, '
                      'enter the state code followed by 3 zeros: ')
    st = stcou[0:2]
    cou = stcou[2:]
    working_gdb = os.path.join(BQARP_ME, st, cou, 'bqarp_{0}.gdb'.format(stcou))
    if not os.path.exists(working_gdb):
        arcpy.CreateFileGDB_management(os.path.join(BQARP_ME, st, cou), 'bqarp_{0}.gdb'.format(stcou), "CURRENT")

    folder_to_local_data = os.path.join(BQARP_ME, st, 'LOCAL_FILES')
    # local_counties = os.path.join(folder_to_local_data, 'counties')
    local_places = os.path.join(folder_to_local_data, 'places')

    # spatial join to check names/FIPS codes
    arcpy.SpatialJoin_analysis(smaller_shp, larger_shp, 'name_FIPS_check')
    # discrepancy tool from maddie (union/symmetrical difference)

    local_dir = os.path.join(BQARP_ME, st, 'LOCAL_FILES')

    if str(cou) == '000':
        input_data = os.path.join(BQARP_ME, st, 'local_data')
        working_folder = os.path.join(BQARP_ME, st)
        clip_county_by_selection(where_ever_lisrds_goes, input_data, working_folder)