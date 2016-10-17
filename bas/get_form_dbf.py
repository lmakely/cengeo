__author__ = 'Lauren Makely'

import os


def get_form_dbf(path):
    """
    get form.dbf

    :param path:    path to bas id
    :return:        list of dbfs?
    """
    for x, y, z in os.walk(path):
        for f in z:
            if f[-8:] == 'FORM.DBF':
                return x + '\\' + f

    results = []
    for x, y, z in os.walk(path):
        for f in z:
            if 'form' in f.lower():
                results.append(x+'\\'+f)
    if len(results):
        return results
    return None
