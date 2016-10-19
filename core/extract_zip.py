__author__ = 'makel004'


import zipfile


def extract_zip(source, output):
    """
    Function goes to zip file and unzips it to the specified output location.

    :param source:  path of zip file to be unzipped
    :param output:  path to folder where unzipped files should be placed
    :return:        nothing (files will be placed in folder)
    """
    with zipfile.ZipFile(source, 'r') as zf:
        zf.extractall(output)