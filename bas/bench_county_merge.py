__author__ = 'Lauren Makely'

import arcpy
import os


def bench_county_merge(bench_dir, bench_base, bas_yy_county_merge):
    """
    Used to create merged file of counties named for the bas year
        example: 'BAS16countyMerge.shp'
    This is generally only used once per BAS cycle to create a shapefile of all the counties in the US.
    If something gets updated though this should be rerun.

    :param bench_dir:            directory of benchmark data?
    :param bench_base:           base name of benchmark files?
    :return bas_yy_county_merge: output name for benchmark shapefile

    Example usage:
        from cengeo import bas

        bench_dir = os.path.join(geoShape, 'bas16_2015')
        bench_base = 'bas16_2015_'
        bas_yy_county_merge = os.path.join(geo_area, 'ABEUS\bas16countymerge.shp')

        bas.bench_county_merge(bench_dir, bench_base, bas_yy_county_merge)
    """

    merge_list2 = list(os.path.join(bench_dir, x, bench_base, 'county_', x, '.shp')
                       for x in os.listdir(bench_dir)
                       if len(x) == 2)
    arcpy.Merge_management(merge_list2, bas_yy_county_merge)