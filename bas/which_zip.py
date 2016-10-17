__author__ = 'Lauren Makely'

import os
import core


def which_zip(source_dir, bas_id):
    """
    Identifies zip files to be unzipped and then processed. If it finds no zip files, prints an error.
    If it finds multiple zip files that correspond with the bas_id it needs then it will ask for the user
    to choose a zip file from a list of found files.

    :param source_dir:  directory where the zip file should be found
    :param bas_id:      the id of the place being processed
    :return results:    list of zipfile(s); by the end of the function, it is a single zipfile
    """

    # declare empty list for zip files
    results = []

    # loop through the directory to fill results
    for f in os.listdir(source_dir):
        # if the extension for a file is '.zip' it gets added to  results
        if f[-4:].lower() == '.zip':
            results.append(f)

    # checking to see if the list is empty or not
    if len(results) == 0:  # there is no ZIP file here
        print('Could not find any zipfiles')
        return None
    if len(results) == 1:  # there is only one zipfile
        return results[0]

    # th following gets printed later if there are multiple items in the results?
    question = """=========================================================================
More than one ZIP file was found for %s.
Please select one from the list below.
Type its number and press enter.
=========================================================================
""" % bas_id

    # appends the list of multiple zips to the end of the question?
    for name in results:
        question += '{index}: {zip}\n'.format(str(results.index(name)), name)

    while 1:
        core.notify()  # notifies user there's a problem
        x = raw_input(question)  # asks user which zip file to use by index number

        # do nothing for the files that are not the chosen index
        if not x:
            return None

        # index chosen and works
        elif x.isdigit() and int(x) < len(results):
            # this print statement is weird and needs to be cleaned up
            print core.make_header('   Running BASID: {id}   '.format(bas_id), '*')
            # results is now a single zipfile to be passed on to another function
            return results[int(x)]

        # there was no input that made sense or was out of range
        else:
            print("The value {0} could not be used, try again please.".format(x))