__author__ = 'Lauren Makely'

import arcpy


def desc_shp(shp):
    """
    prints list of filed names and their types.
    :param shp: esri shapefile
    :return:    list of attribute fields

    example output:
    NAME       TYPE
    ====================
    FID        OID
    Shape      Geometry
    OBJECTID_1 Integer
    OBJECTID   Integer
    STATEFP    String
    COUNTYFP   String
    ====================
    """

    print('{:10s} {}'.format('NAME', 'TYPE'))
    print('====================')
    for f in arcpy.ListFields(shp):
        print('{:10s} {}'.format(f.name, f.type))
    print('====================')