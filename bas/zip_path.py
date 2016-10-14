__author__ = 'Lauren Makely'

import os


def zip_path(basid):
    """

    :param basid:   entity ID entered by user at the beginning
    :return:        file path to the appropriate swecs location
    """
    st = basid[1:3]
    if basid[0] == '1':  # incplace
        swecsgeocode = basid[1:3]+basid[-5:]
    elif basid[0] == '2':  # county
        swecsgeocode = basid[1:6]
    elif basid[0] == '3':  # cousub
        swecsgeocode = basid[1:]
    elif basid[0] == '4':  # aial
        swecsgeocode = basid[3:7]
    elif basid[0] == '0':  # concity
        swecsgeocode = basid[1:3]+basid[-5:]
    return os.path.join(swim_dir, st, basid)