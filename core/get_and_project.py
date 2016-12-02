__author__ = 'Lauren Makely'


import arcpy
import os

def get_and_project(output, input_file):
    """
    this is not done but already figured out. wanted to preserve the info and clean up later into a real function
    :param output:
    :param input_file:
    :return:
    """
 # project data
    projected_counties = os.path.join(output, 'projected_local')
    if not os.path.exists(projected_counties):
        os.mkdir(projected_counties)

    # this should probs be a function
    targetDescribe = arcpy.Describe(input_file)
    targetSR = targetDescribe.SpatialReference
    arcpy.Project_management(counties, cou_output, targetSR)