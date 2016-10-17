__author__ = 'Lauren Makely'

import os


def get_form_dbf(list_of_paths):
    """
    get form.dbf

    :param path:    path to bas id
    :return:        list of dbfs?
    """
    for files in list_of_paths:
        if files[1][-8:] == 'FORM.DBF':
            return os.path.join(*files)

    results = []
    for files in list_of_paths:
        if 'form' in files.lower():
            results.append(os.path.join(*files))
    if len(results) > 0:
        return results
    return None
