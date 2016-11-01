__author__ = 'Lauren Makely'

import core
import os


def which_zip(source_dir, *search_id):
    """
    Identifies zip files to be unzipped and then processed. If it finds no zip files, prints an error.
    If it finds multiple zip files that correspond with the search_id it needs then it will ask for the user
    to choose a zip file from a list of found files.

    :param source_dir:  directory where the zip file should be found
    :param search_id:   the id of the place being processed. if left blank, will return the whole directory of zip files
    :return results:    list of zipfile(s); by the end of the function, it is a single zipfile
    """

    zip_results = list(core.find_files(source_dir, '.zip'))

    if search_id:
        def find_search_term(search, search_list):
            for file_name in search_list:
                if search in file_name:
                    yield file_name
        results = list(find_search_term(search_id[0], zip_results))
    else:
        results = zip_results

    # checking to see if the list is empty or not
    if len(results) == 0:  # there is no ZIP file here
        print('Could not find any zipfiles')
        return None

    if len(results) > 0:  # there is more than one zipfile
        # the following gets printed later if there are multiple items in the results?
        question = """=================================================================================
More than one ZIP file was found for this state.
Please select from the list below.
Type its number or enter a list of numbers separated by spaces and press enter.
=================================================================================
"""

        # appends the list of multiple zips to the end of the question?
        for name in results:
            question += '{0}: {1}\n'.format(str(results.index(name)), name)

        while 1:
            core.notify()  # notifies user there's a problem
            x_list = list(int(x) for x in raw_input(question).split())  # asks user which zip file to use by index number

            # do nothing for the files that are not the chosen index
            if not x_list:
                return None

            # there was no input that made sense or was out of range
            elif max(x_list) > len(results):
                print("The value {0} could not be used, try again please.".format(max(x_list)))

            # index chosen and works
            else:
                zip_list = []
                for x in x_list:
                    print core.make_header('  Preparing to unzip: {0}  '.format(results[x]), '*')
                    # results is now a single zipfile to be passed on to another function
                    zip_list.append(os.path.join(source_dir, results[x]))
                return zip_list


if __name__ == "__main__":
    swim = r'H:\!!!HDriveStuff\BQARP\20\swim\20'
    unzip_these = which_zip(swim, 'KS')
    print unzip_these