__author__ = 'Lauren Makely'

import os


def lisrds(counties_list, out_path):
    """
    Creates text files. Not sure why it does this as the folder is currently empty.

    Nick, add clarification?

    :param counties_list:   list of counties to be processed
    :param out_path:        path to output folder
    :return:
    """

    for cou in counties_list:
        f_file = os.path.join(out_path, cou, '.txt')
        f = open(f_file)
        f.close()