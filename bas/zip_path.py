__author__ = 'Lauren Makely'

import os


def zip_path(return_dir, bas_id):
    """
    I'm really not sure if this should be a function or what the heck its for.

    :param return_dir:  file path to swim directory where the file should be?
    :param bas_id:      entity ID entered by user at the beginning
    :return:            file path to the appropriate swecs location
    """
    st = bas_id[1:3]
    if bas_id[0] == '1':  # incplace
        swecs_geo_code = bas_id[1:3]+bas_id[-5:]
    elif bas_id[0] == '2':  # county
        swecs_geo_code = bas_id[1:6]
    elif bas_id[0] == '3':  # cousub
        swecs_geo_code = bas_id[1:]
    elif bas_id[0] == '4':  # aial
        swecs_geo_code = bas_id[3:7]
    elif bas_id[0] == '0':  # concity
        swecs_geo_code = bas_id[1:3]+bas_id[-5:]
    return os.path.join(return_dir, st, bas_id)