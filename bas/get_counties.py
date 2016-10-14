__author__ = 'Lauren Makely'

import arcpy


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