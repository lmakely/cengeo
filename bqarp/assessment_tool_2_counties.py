__author__ = 'Lauren Makely'

import arcpy
from arcpy import da
import os
import logging

"""
THIS IS A TOOL FOR ARCMAP AND WILL NOT WORK ON ITS OWN IN PYTHON WITHOUT MODIFICATION


This tool takes in a list of features to be merged together and lets the user define the field
used by the submitter to store county and/or county names. It then performs a spatial join and
selection to figure out where mismatches are.
"""


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

arcpy.env.overwriteOutput = True

input_features = arcpy.GetParameterAsText(0)  # list of counties to merge together
put_them_here = arcpy.GetParameterAsText(1)  # this should be your local data folder or other similar raw data folder
local_name_field = arcpy.GetParameterAsText(2)  # the name field in the local data to perform the matching on
local_fips_field = arcpy.GetParameterAsText(3)  # the FIPs code field in the local data to perform the matching on
st = arcpy.GetParameterAsText(4)  # the state code, cause its easier to just ask for it here
census_counties_shp = arcpy.GetParameterAsText(5)  # LISRDS file for corresponding census counties


logging.basicConfig(filename=os.path.join(put_them_here, 'assessment_log.txt'), level=logging.DEBUG, format='%(message)s', filemode='w')
logger = logging.getLogger()
logger.info(make_header('  Processing files for {}  '.format(st)))

these_features = [feature for feature in input_features.split(';')]

merged_counties_folder = os.path.join(put_them_here, 'counties')
if not os.path.exists(merged_counties_folder):
    arcpy.AddMessage('Making output folder....')
    os.mkdir(merged_counties_folder)

projected_counties = os.path.join(merged_counties_folder, 'projected_local')
if not os.path.exists(projected_counties):
    os.mkdir(projected_counties)

merged_counties = os.path.join(merged_counties_folder, 'local_counties_merge_{0}.shp'.format(st))

projection = '{0}.prj'.format(census_counties_shp[:-4])
arcpy.AddMessage('Projecting features....')
for shp in these_features:
    head, tail = os.path.split(shp)
    output_name = os.path.join(projected_counties, '{0}_projected.shp'.format(tail[:-4]))
    arcpy.Project_management(shp, output_name, projection)

merge_these_features = []
arcpy.AddMessage('Merging features into one file....')
projected_features = list(find_files(projected_counties, '.shp'))
for f in projected_features:
    merge_these_features.append(os.path.join(projected_counties, f))
arcpy.Merge_management(merge_these_features, merged_counties)

local_census_join_shp = os.path.join(merged_counties_folder, 'counties_join_{0}.shp'.format(st))

# Process: Spatial Join
arcpy.AddMessage('Beginning comparison of census data and local data....')
arcpy.SpatialJoin_analysis(merged_counties,
                           census_counties_shp,
                           local_census_join_shp,
                           'JOIN_ONE_TO_MANY',
                           'KEEP_ALL',
                           "",
                           'INTERSECT')

# Process: Add Field
arcpy.AddField_management(local_census_join_shp,
                          'FIPS_MATCH',
                          'TEXT')
arcpy.AddMessage('FIPS_MATCH field added....')

# Process: Add Field (2)
arcpy.AddField_management(local_census_join_shp,
                          'NAME_MATCH',
                          'TEXT')
arcpy.AddMessage('NAME_MATCH field added....')

fips_fields = ['{0}'.format(local_fips_field), 'COUNTYFP', 'FIPS_MATCH']
name_fields = ['{0}'.format(local_name_field), 'NAME', 'NAME_MATCH']

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(local_census_join_shp, 'local_census_lyr')

fips_mismatch = 0
name_mismatch = 0

with arcpy.da.UpdateCursor('local_census_lyr', fips_fields) as cursor:
    for row in cursor:
        if str(row[0]) == str(row[1]):
            row[2] = 'Y'
        else:
            row[2] = 'N'
            fips_mismatch += 1
        cursor.updateRow(row)

with arcpy.da.UpdateCursor('local_census_lyr', name_fields) as cursor:
    for row in cursor:
        if str(row[0]) == str(row[1]):
            row[2] = 'Y'
        else:
            row[2] = 'N'
            name_mismatch += 1
        cursor.updateRow(row)

arcpy.AddMessage('Deleting intermediate files....')
os.rmdir(projected_counties)
os.remove(merged_counties)

logger.warning('{0} FIPS records did not match'.format(fips_mismatch))
logger.warning('{0} Name records did not match'.format(name_mismatch))
logging.info('Output file located at {0}'.format(local_census_join_shp))
arcpy.AddMessage('Assessment complete! counties can now be split by county.')