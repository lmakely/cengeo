__author__ = 'Lauren Makely'

import os


def get_shps(list_of_paths):
    """
    Creates a list of shapefiles within an entire directory. Recursively searches through a whole folder to find all the
    shapefiles within.

    :param list_of_paths:   expecting a list of tuples consisting of (dirname, filenames). Use os.walk() and store
                            values from there for best results. See below for example.
    :return:                list of shapefiles
    """

    results = []
    for files in list_of_paths:
        for f in files[1]:
            if f.endswith('.shp'):
                results.append((files[0], f))
    return results


if __name__ == "__main__":
    path = r'C:\some_drive'
    f_list = []

    for x, y, z in os.walk(path):
        f_list.append((x, z))

    shp_list = get_shps(f_list)

    change_files = []
    for shp in shp_list:
        if 'changes' in shp[1]:
            change_files.append(shp)

    for chng in change_files:
        print chng