__author__ = 'makel004'


import zipfile


def extract_zip(source, output):
    with zipfile.ZipFile(source, 'r') as zf:
        zf.extractall(output)