__author__ = 'Lauren Makely'

import os


def get_form_dbf(path):
    """
    generator that yields any fielpath that ends in "FORM.DBF" within a directory

    :param path:    path to bas id
    :return:        list of dbfs?
    """
    
    for x, y, z in os.walk(path):
        for f in z:
            if f.endswith('FORM.DBF'):
                yield os.path.join(x,f)
