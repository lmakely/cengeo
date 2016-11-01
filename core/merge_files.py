__author__ = 'Lauren Makely'

import arcpy
import os
import logging


# Process: Merge
def merge_files(input_datasets, output_dataset):
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

