__author__ = 'Lauren Makely'

"""
THIS IS AN ARC TOOLBOX FUNCTION AND WILL NOT WORK OUTSIDE OF ARC!

For a stand alone function, see core module.
"""

import arcpy
import os


arcpy.env.overwriteOutput = True
arcpy.env.workspace = arcpy.GetParameterAsText(0)

input_shps = arcpy.env.workspace
output_folder = arcpy.GetParameterAsText(1)

for item in input_shps.split(';'):
    folder, out_name = os.path.split(item)
    out = os.path.join(output_folder, out_name)
    arcpy.Copy_management(item, out)
    arcpy.Delete_management(item)