__author__ = 'Lauren Makely'

import os


def submission_type(path):
    """
    figure out MTPS vs digital

    :param path:    path to processing folder for the specific bas id
    :return:        string containing the type of submission
    """
    for x, y, z in os.walk(path):
        for f in z:
            if f[-8:].upper() == 'FORM.DBF':
                return 'MTPS'
            elif f[-5:].upper() == '.GUPS':
                return 'GUPS'
    return 'DIGITAL'