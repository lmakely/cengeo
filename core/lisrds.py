__author__ = 'Lauren Makely'

import os


def lisrds(counties_list, out_path):
    """
    Creates a text file to be placed in the geo_area/BAS/BLISRDS_STAGE folder named for the county being processed.
    Currently only orders the edge_vw layer

    :param counties_list:   list of counties to be processed
    :param out_path:        path to output folder
    :return:
    """

    for cou in counties_list:
        f_file = os.path.join(out_path, cou, '.txt')
        f = open(f_file, 'w')
        f.close()