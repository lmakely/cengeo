__author__ = 'Lauren Makely'

import arcpy
import os
import logging

"""
THIS IS A TOOL FOR ARCMAP AND WILL NOT WORK ON ITS OWN IN PYTHON WITHOUT MODIFICATION

This tool will use census data to clip local data to each county in a state. It can be used on feature classes or
shapefiles. While its primary use is to divide up data for BQARP, it can be altered to fit tasks for other programs.
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
    output_string = "{b}\n{s}\n{b}".format(b=char * len(my_string), s=my_string)
    return output_string


def find_files(search_folder, *search_string):
    """
    Generates a list of files that matches the search criteria.

    :param search_folder:   folder to search within
    :param search_string:   filetype to look for
    :return:                path for the files  that contain the search string
    """
    for f in os.listdir(search_folder):
        # if the extension for a file matches the search string it gets produced
        if search_string:
            for ext in search_string:
                if f.endswith(ext):
                    yield f
        else:
            yield f


def clip_county_by_selection(joined_county_file, local_file, output_folder, type_submission):
    """
    Goes through a state county file and clips an input file to each county boundary. Used by BQARP to clip local
    data to census data.

    :param joined_county_file:  lisrds county file
    :param local_file:          local boundary files to be split
    :param output_folder:       base folder to put outputs. will create new folders for each split place.
    :param type_submission:     this is used to format the name of the output shapefile. In the arctool it will be
                                a drop down list to make things standardized.
    """

    arcpy.env.workspace = output_folder  # the state BQARP folder

    arcpy.MakeFeatureLayer_management(joined_county_file, 'joined_counties_lyr')
    arcpy.MakeFeatureLayer_management(local_file, 'local_places_lyr')

    logging.info('Beginning to split places by county')
    field_names = ['STATEFP', 'COUNTYFP']
    logging.info('Number of records selected for each county')
    with arcpy.da.SearchCursor('joined_counties_lyr', field_names) as cursor:
        for row in cursor:
            # create the full county code and sql statement
            county_fp = '{0}{1}'.format(row[0], row[1])
            expression = """"COUNTYFP" = '{0}'""".format(row[1])
            # select each county from the joined counties and set outputs folder
            arcpy.SelectLayerByAttribute_management('joined_counties_lyr',
                                                    "NEW_SELECTION",
                                                    expression)

            # select the places inside the selection
            arcpy.SelectLayerByLocation_management('local_places_lyr',
                                                   "WITHIN",
                                                   'joined_counties_lyr',
                                                   "",
                                                   "NEW_SELECTION",
                                                   "NOT_INVERT")

            select_length = int(arcpy.GetCount_management('local_places_lyr').getOutput(0))
            logging.info('{0}: {1}'.format(county_fp, select_length))

            if select_length > 0:
                clip_name = 'npc_bqarp_2016_{0}_{1}.shp'.format(county_fp, type_submission)
                output_path = os.path.join(output_folder, county_fp)

                # make the output folder if it's not already there
                if not os.path.exists(os.path.join(output_folder, county_fp)):
                    os.mkdir(os.path.join(output_folder, county_fp))

                arcpy.FeatureClassToFeatureClass_conversion('local_places_lyr',
                                                            output_path,
                                                            clip_name)
                arcpy.AddMessage('Completed clipping: {0}'.format(county_fp))
            elif select_length == 0:
                arcpy.AddMessage('{0} contains no features'.format(county_fp))
            else:
                arcpy.AddMessage('{0} is malfunctioning'.format(county_fp))

    logging.info('Completed splitting places')

if __name__ == "__main__":
    counties = arcpy.GetParameterAsText(0)  # use their county data to clip their places, our data on our places
    places = arcpy.GetParameterAsText(1)
    output = arcpy.GetParameterAsText(2)  # file path to state folder where county folder should get made
    census_file = arcpy.GetParameterAsText(3)
    subtype = arcpy.GetParameterAsText(4)

    logging.basicConfig(filename=os.path.join(output, 'log.txt'), level=logging.DEBUG, format='%(message)s')
    logger = logging.getLogger()
    logger.info('\n')
    logger.info(make_header('Dividing local data into county folders'))

    arcpy.AddMessage('Beginning preprocesing to clip features....')

    # project data
    projected_counties = os.path.join(output, 'projected_local')
    if not os.path.exists(projected_counties):
        os.mkdir(projected_counties)

    # this should probs be a function
    targetDescribe = arcpy.Describe(census_file)
    targetSR = targetDescribe.SpatialReference

    arcpy.AddMessage('Projecting features....')
    head, tail = os.path.split(counties)
    cou_output = os.path.join(projected_counties, 'local_counties_projected.shp')
    arcpy.Project_management(counties, cou_output, targetSR)

    head, tail = os.path.split(places)
    pl_output = os.path.join(projected_counties, 'local_places_projected.shp')
    arcpy.Project_management(places, pl_output, targetSR)

    # spatial join of local counties and census counties
    arcpy.AddMessage('Transferring census information to local information')
    clip_to_these = os.path.join(projected_counties, 'local_joined.shp')
    arcpy.SpatialJoin_analysis(census_file,
                               cou_output,
                               clip_to_these,
                               'JOIN_ONE_TO_ONE',
                               'KEEP_ALL',
                               "",
                               'INTERSECT')

    arcpy.AddMessage('Clipping features....')
    clip_county_by_selection(clip_to_these, places, output, subtype)

    arcpy.AddMessage('Deleting intermediate files....')
    try:
        remove_files = find_files(projected_counties)
        for rf in remove_files:
            if rf.endswith('.shp'):
                arcpy.Delete_management(os.path.join(projected_counties, rf))
    finally:
        remove_again = find_files(projected_counties)
        for ra in remove_again:
            print ra
            os.remove(os.path.join(projected_counties, ra))

    os.rmdir(projected_counties)

    arcpy.AddMessage('Clipping complete')