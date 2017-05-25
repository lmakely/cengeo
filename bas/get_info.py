__author__ = 'Lauren Makely'

import arcpy
import os

def get_counties(change_list, usa_county_fc):
    out_list = []
    tmp = arcpy.MakeFeatureLayer_management(usa_county_fc, "in_memory\\counties")
    for fc in change_list:
        arcpy.SelectLayerByLocation_management(tmp, "WITHIN_A_DISTANCE", fc, '1 FEET', "ADD_TO_SELECTION")
    cur = arcpy.SearchCursor(tmp)
    for row in cur:
        out_list.append(row.STATEFP + row.COUNTYFP)
    arcpy.Delete_management(tmp)
    del cur
    return out_list


def get_form_dbf(list_of_paths):
    """
    get form.dbf

    :param path:    path to bas id
    :return:        list of dbfs?
    """
    for files in list_of_paths:
        if files[1][-8:] == 'FORM.DBF':
            return os.path.join(*files)

    results = []
    for files in list_of_paths:
        if 'form' in files.lower():
            results.append(os.path.join(*files))
    if len(results) > 0:
        return results
    return None
