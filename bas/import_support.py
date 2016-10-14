__author__ = 'Lauren Makely'

import arcpy
import dicts
import shutil
import os


def import_support(gdb, county_list, folder, state, src_root, src_base):
    """
    Used to format gdb properly before processing shp into them

    :param gdb:         input gdb for features to be created in
    :param county_list: list of counties from user to be processed
    :param folder:      st_folder\basid?
    :param state:       state code being processed
    :param src_root:    folder containing benchmark files to be added (?)
    :param src_base:    benchmark files to be added (?)
    :return:
    """

    if state == '02':  # Alaska
        arcpy.CreateFeatureDataset_management(
            gdb,
            "benchmark",
            "PROJCS['NAD_1983_Alaska_Albers',"
            "GEOGCS['GCS_North_American_1983',"
            "DATUM['D_North_American_1983', "
            "SPHEROID['GRS_1980',6378137.0,298.257222101]],"
            "PRIMEM['Greenwich', 0.0],"
            "UNIT['Degree', 0.0174532925199433]], "
            "PROJECTION['Albers'], "
            "PARAMETER['False_Easting',0.0],"
            "PARAMETER['False_Northing',0.0], "
            "PARAMETER['Central_Meridian',-154.0],"
            "PARAMETER['Standard_Parallel_1',55.0], "
            "PARAMETER['Standard_Parallel_2',65.0],"
            "PARAMETER['Latitude_Of_Origin',50.0],"
            "UNIT['Meter',1.0]];-13752200 -8948200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
        )
    elif state == '15':  # Hawaii
        arcpy.CreateFeatureDataset_management(
            gdb,
            "benchmark",
            "PROJCS['Hawaii_Albers_Equal_Area_Conic', "
            "GEOGCS['GCS_North_American_1983',"
            "DATUM['D_North_American_1983', "
            "SPHEROID['GRS_1980',6378137.0,298.257222101]],"
            "PRIMEM['Greenwich',0.0], "
            "UNIT['Degree',0.0174532925199433]], "
            "PROJECTION['Albers'], "
            "PARAMETER['False_Easting',0.0],"
            "PARAMETER['False_Northing',0.0], "
            "PARAMETER['Central_Meridian',-157.0],"
            "PARAMETER['Standard_Parallel_1',8.0], "
            "PARAMETER['Standard_Parallel_2',18.0],"
            "PARAMETER['Latitude_Of_Origin',13.0],"
            "UNIT['Meter',1.0]];-22487400 -7108900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
        )
    else:  # contiguous USA 48
        arcpy.CreateFeatureDataset_management(
            gdb,
            "benchmark",
            "PROJCS['USA_Contiguous_Albers_Equal_Area_Conic_USGS_version',"
            "GEOGCS['GCS_North_American_1983', "
            "DATUM['D_North_American_1983',"
            "SPHEROID['GRS_1980',6378137.0,298.257222101]], "
            "PRIMEM['Greenwich',0.0],"
            "UNIT['Degree',0.0174532925199433]], "
            "PROJECTION['Albers'],"
            "PARAMETER['False_Easting',0.0], "
            "PARAMETER['False_Northing',0.0],"
            "PARAMETER['Central_Meridian',-96.0], "
            "PARAMETER['Standard_Parallel_1',29.5],"
            "PARAMETER['Standard_Parallel_2',45.5], "
            "PARAMETER['Latitude_Of_Origin',23.0],"
            "UNIT['Meter',1.0]];-16901100 -6972200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
        )
    support_fd = os.path.join(gdb, 'benchmark')

    if state in dicts.ccd_list:
        cou_subtype = 'ccd'
    else:
        cou_subtype = 'mcd'
    merge_lyr_list = ['aial', 'arealm', 'cdp', 'concity', 'county', 'edges', 'offset', 'place', 'pointlm', 'water']

    for county in county_list:
        shutil.copytree(os.path.join(src_root, county), os.path.join(folder, county))

    for cou in county_list:
        in_path = os.path.join(folder, cou, src_base, cou_subtype, '_{0}.shp'.format(cou))
        out_fd = os.path.join(support_fd, 'bas_cousub')
        arcpy.Merge_management(in_path, out_fd)

    for lyr in merge_lyr_list:
        for x in county_list:
            in_folder = os.path.join(folder, x, src_base, lyr, '_{0}.shp'.format(x))
            out_fd_lyr = os.path.join(support_fd, 'bas_{0}'.format(lyr))
            arcpy.Merge_management(in_folder, out_fd_lyr)