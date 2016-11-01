__author__ = 'Lauren Makely'

import arcpy
from arcpy import da
import os

"""
THIS IS A TOOL FOR ARCMAP AND WILL NOT WORK ON ITS OWN IN PYTHON WITHOUT MODIFICATION


This tool takes in a list of features to be merged together and lets the user define the field
used by the submitter to store county and/or place names. It then performs a spatial join and
selection to figure out where mismatches are.
"""

merge_these_features = arcpy.GetParameterAsText(0)  # list of places to merge together
put_them_here = arcpy.GetParameterAsText(1)  # this should be your local data folder
local_name_field = arcpy.GetParameterAsText(2)  # the name field in the local data to perform the matching on
local_fips_field = arcpy.GetParameterAsText(3)  # the FIPs code field in the local data to perform the matching on
st = arcpy.GetParameterAsText(4)  # the state code, cause its easier to just ask for it here
census_places_shp = arcpy.GetParameterAsText(5)  # LISRDS file for corresponding census places


merged_places_folder = os.path.join(put_them_here, 'places')
if not os.path.exists(merged_places_folder):
    os.mkdir(merged_places_folder)

merged_places = os.path.join(merged_places_folder, 'local_places_merge_{0}.shp'.format(st))
arcpy.Merge_management(merge_these_features, merged_places)

local_census_join_shp = os.path.join(merged_places_folder, 'local_places_join_{0}.shp'.format(st))

# Process: Spatial Join
arcpy.SpatialJoin_analysis(merged_places,
                           census_places_shp,
                           local_census_join_shp,
                           'JOIN_ONE_TO_MANY',
                           'KEEP_ALL',
                           "",
                           'INTERSECT')

# Process: Add Field
arcpy.AddField_management(local_census_join_shp,
                          'FIPS_MATCH',
                          'TEXT')

# Process: Add Field (2)
arcpy.AddField_management(local_census_join_shp,
                          'NAME_MATCH',
                          'TEXT')

fips_fields = ['{0}'.format(local_fips_field), 'PLACEFP', 'FIPS_MATCH']
name_fields = ['{0}'.format(local_name_field), 'NAME', 'NAME_MATCH']

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(local_census_join_shp, 'local_census_lyr')

with arcpy.da.UpdateCursor('local_census_lyr', fips_fields) as cursor:
    for row in cursor:
        if str(row[0]) == str(row[1]):
            row[2] = 'Y'
        else:
            row[2] = 'N'
        cursor.updateRow(row)

with arcpy.da.UpdateCursor('local_census_lyr', name_fields) as cursor:
    for row in cursor:
        if str(row[0]) == str(row[1]):
            row[2] = 'Y'
        else:
            row[2] = 'N'
        cursor.updateRow(row)