__author__ = 'Lauren Makely'

import arcpy
from arcpy import da
import os
import logging

"""
THIS IS A TOOL FOR ARCMAP AND WILL NOT WORK ON ITS OWN IN PYTHON WITHOUT MODIFICATION


This tool takes in a list of features to be merged together and lets the user define the field
used by the submitter to store feature names. It then performs a union and selection to
figure out where discrepancies are.

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

geography = arcpy.GetParameterAsText(0)
input_features = arcpy.GetParameterAsText(1)  # list of features to merge together
put_them_here = arcpy.GetParameterAsText(2)  # this should be your local data folder or other similar raw data folder
local_name_field = arcpy.GetParameterAsText(3)  # the name field in the local data to perform the matching on
local_fips_field = arcpy.GetParameterAsText(4)  # the FIPs code field in the local data to perform the matching on
st = arcpy.GetParameterAsText(5)  # the state code, cause its easier to just ask for it here
census_geography_shp = arcpy.GetParameterAsText(6)  # LISRDS file for corresponding census geography

# Setting up the output log file
logging.basicConfig(filename=os.path.join(put_them_here, 'assessment_log.txt'),
                    level=logging.DEBUG,
                    format='%(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.info(make_header('  Processing files for {}  '.format(st)))

# Where the files will end up (divides them into the different geography types, e.g. places, counties, school districts)
merged_geo_folder = os.path.join(put_them_here, geography)

# Checks that the output folder exists and if not, makes it
if not os.path.exists(merged_geo_folder):
    arcpy.AddMessage('Making output folder....')
    os.mkdir(merged_geo_folder)

# Defining the output shp name for the merged local features
merged_geos = os.path.join(merged_geo_folder, 'local_{0}_merge_{1}.shp'.format(geography, st))
# Output path for union
local_census_join_shp = os.path.join(merged_geo_folder, '{0}_union_{1}.shp'.format(geography, st))
# Temporary files used later on to format the discrepancy polygon
discrepancy_file_multipart = "in_memory\\places_select_MultipartToSin"
discrepancy_file_select = "in_memory\\places_select_area"
# Creates a list of the input shapefiles from above (arc stores them differently that python will interpret them)
these_features = [feature for feature in input_features.split(';')]

# Adds message to arc window
arcpy.AddMessage('Merging features into one file....')
# Adds message to the log file that describes all the files being merged
logging.info('Merging the flowing:')
for shp in these_features:
    logging.info(shp)
# Merging the files together
arcpy.Merge_management(these_features, merged_geos)

# Many local files store their place names in a field called NAME just like we do. This bit here makes sure the later
# comparisons are performed on the correct census NAME field. If manipulating names to remove or add extra information,
# please modify a copy of their data. This script does not care about casing so modifications to that are unnecessary.
census_name = 'NAME'
fields = arcpy.ListFields(merged_geos)
i = 1
for field in fields:
    if field.name == 'NAME':
        census_name = 'NAME_1'
    elif field.name == 'NAME_{0}'.format(i):
        i += 1
        census_name = 'NAME_{0}'.format(i)
    else:
        continue

# Status update to arc window
arcpy.AddMessage('Beginning comparison of census data and local data....')

# Process: Union
arcpy.Union_analysis([merged_geos,
                     census_geography_shp],
                     local_census_join_shp,
                     "ALL",
                     "",
                     "GAPS")

fips_fields = ['{0}'.format(local_fips_field), 'COUNTYFP', 'FIPS_MATCH']
name_fields = ['{0}'.format(local_name_field), '{0}'.format(census_name), 'NAME_MATCH']

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(local_census_join_shp, 'local_census_lyr')

if local_fips_field != "":
    # Process: Add Field
    arcpy.AddField_management(local_census_join_shp, 'FIPS_MATCH', 'TEXT')
    # Status update to arc window
    arcpy.AddMessage('FIPS_MATCH field added....')

    fips_mismatch = 0
    with arcpy.da.UpdateCursor('local_census_lyr', fips_fields) as cursor:
        for row in cursor:
            fips_length = len(str(row[0]))
            if fips_length == 3:
                if str(row[0]) == str(row[1]):
                    row[2] = 'Y'
                else:
                    row[2] = 'N'
                    fips_mismatch += 1
                cursor.updateRow(row)
            elif fips_length == 5:
                if str(row[0][2:]) == str(row[1]):
                    row[2] = 'Y'
                else:
                    row[2] = 'N'
                    fips_mismatch += 1
                cursor.updateRow(row)
            else:
                row[2] = 'N'
                fips_mismatch += 1
    logging.warning('{0} FIPS records did not match'.format(fips_mismatch))

if local_name_field != "":
    # Process: Add Field (2)
    arcpy.AddField_management(local_census_join_shp, 'NAME_MATCH', 'TEXT')
    # Status update to arc window
    arcpy.AddMessage('NAME_MATCH field added....')
    name_mismatch = 0
    with arcpy.da.UpdateCursor('local_census_lyr', name_fields) as cursor:
        for row in cursor:
            if str(row[0]).upper() == str(row[1]).upper():
                row[2] = 'Y'
            else:
                row[2] = 'N'
                name_mismatch += 1
            cursor.updateRow(row)
    logger.warning('{0} Name records did not match'.format(name_mismatch))

discrepancy_file = os.path.join(merged_geo_folder, 'bqarp_{0}_discrepancies.shp'.format(geography))

name_fields_expression = """UPPER({0}) <> UPPER({1})""".format(census_name.upper(), local_name_field.upper())
arcpy.Select_analysis(local_census_join_shp, discrepancy_file_select, name_fields_expression)
arcpy.MultipartToSinglepart_management(discrepancy_file_select, discrepancy_file_multipart)

temporary_output_file = os.path.join(merged_geo_folder, 'temp_file.shp')
arcpy.Project_management(discrepancy_file_multipart,
                         temporary_output_file,
                         "PROJCS['North_America_Albers_Equal_Area_Conic',"
                         "GEOGCS['GCS_North_American_1983',"
                         "DATUM['D_North_American_1983',"
                         "SPHEROID['GRS_1980',6378137.0,298.257222101]],"
                         "PRIMEM['Greenwich',0.0],"
                         "UNIT['Degree',0.0174532925199433]],"
                         "PROJECTION['Albers'],"
                         "PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],"
                         "PARAMETER['Central_Meridian',-96.0],"
                         "PARAMETER['Standard_Parallel_1',20.0],"
                         "PARAMETER['Standard_Parallel_2',60.0],"
                         "PARAMETER['Latitude_Of_Origin',40.0],"
                         "UNIT['Meter',1.0]]",
                         "",
                         "",
                         "NO_PRESERVE_SHAPE",
                         "")

# Process: Calculate Areas
arcpy.CalculateAreas_stats(temporary_output_file, discrepancy_file)
arcpy.Delete_management(temporary_output_file)

arcpy.AddMessage('Adding processing attribute fields...')
# creating QC fields
arcpy.AddField_management(discrepancy_file, "FEEDBACK", "TEXT", "", "", "3", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "COMMENTS", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "RELATE", "TEXT", "", "", "5", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "PROCESS", "TEXT", "", "", "1", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "P_COMMENTS", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "VERIFY", "TEXT", "", "", "1", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "V_COMMENTS", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "DIGITIZE", "TEXT", "", "", "1", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "D_COMMENTS", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "DIG_QA", "TEXT", "", "", "1", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(discrepancy_file, "Q_COMMENTS", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
logging.info('Discrepancy output file located at {0}'.format(discrepancy_file))

logging.info('Union output file located at {0}'.format(local_census_join_shp))
arcpy.AddMessage('Assessment complete!')