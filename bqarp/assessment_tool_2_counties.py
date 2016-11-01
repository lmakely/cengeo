__author__ = 'Lauren Makely'

import arcpy
import os

"""
THIS IS A TOOL FOR ARCMAP AND WILL NOT WORK ON ITS OWN IN PYTHON


This tool takes in a list of features to be merged together and lets the user define the field
used by the submitter to store county and/or place names. It then performs a spatial join and
selection to figure out where mismatches are.
"""

merge_these_features = arcpy.GetParameterAsText(0)  # list of counties to merge together
put_them_here = arcpy.GetParameterAsText(1)  # this should be your local data folder and will default to there
local_join_field = arcpy.GetParameterAsText(2)  # the field in the local data to perform the matching on
local_fips_field = arcpy.GetParameterAsText(3)  # the field in the local data to perform the matching on
st = arcpy.GetParameterAsText(4)  # the state code, cause its easier to just ask for it here

merged_counties_folder = os.path.join(put_them_here, 'counties')
if not os.path.exists(merged_counties_folder):
    os.mkdir(merged_counties_folder)

merged_counties = os.path.join(merged_counties_folder, 'local_counties_{0}.shp'.format(st))
arcpy.Merge_management(merge_these_features, merged_counties)
