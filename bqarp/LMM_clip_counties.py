__author__ = 'Lauren Makely'

import arcpy
import os
import logging


# Script arguments
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

if __name__ == "__main__":
    counties = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\20\Census\bqarp_2016_20_county_v90.shp'
    places = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\20\SWIM_FILES\KS_20160926.gdb\KS_MunicipalBoundaries'
    output = r'H:\!!!HDriveStuff\BQARP\20'
    clip_county_by_selection(counties, places, output)