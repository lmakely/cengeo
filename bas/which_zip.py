__author__ = 'Lauren Makely'

import core


def which_zip(source_dir, *search_id):
    """
    Identifies zip files to be unzipped and then processed. If it finds no zip files, prints an error.
    If it finds multiple zip files that correspond with the search_id it needs then it will ask for the user
    to choose a zip file from a list of found files.

    :param source_dir:  directory where the zip file should be found
    :param search_id:   the id of the place being processed. if left blank, will return the whole directory of zip files
    :return results:    list of zipfile(s); by the end of the function, it is a single zipfile
    """

    results = core.find_files(source_dir, '.zip')

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
                """ % search_id

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
            print core.make_header('   Running BASID: {id}   '.format(search_id), '*')
            # results is now a single zipfile to be passed on to another function
            return results[int(x)]

        # there was no input that made sense or was out of range
        else:
            print("The value {0} could not be used, try again please.".format(x))