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


def which_zip_single_response(source_dir, *search_id):
    """
    Identifies zip files to be unzipped and then processed. If it finds no zip files, prints an error.
    If it finds multiple zip files that correspond with the search_id it needs then it will ask for the user
    to choose a zip file from a list of found files.

    :param source_dir:  directory where the zip file should be found
    :param search_id:   the id of the place being processed. if left blank, will return the whole directory of zip files
    :return results:    list of zipfile(s)
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
        question = """=========================================================================
More than one ZIP file was found for this state.
Please select from the list below.
Type its number or enter a list of numbers separated by spaces and press enter.
=========================================================================
"""
        # appends the list of multiple zips to the end of the question?
        for name in results:
            question += '{0}: {1}\n'.format(str(results.index(name)), name)

        while 1:
            core.notify()  # notifies user there's a problem
            x_list = [int(x) for x in raw_input(question).split()]  # asks user which zip file to use by index number

            # do nothing for the files that are not the chosen index
            if not x_list:
                return None

            # there was no input that made sense or was out of range
            elif max(x_list) > len(results):
                print("The value {0} could not be used, try again please.".format(max(x_list)))

            # index chosen and works
            else:  # turn this into a generator later
                zip_list = []
                for x in x_list:
                    print core.make_header('  Preparing to unzip: {0}  '.format(results[x]), '*')
                    # results is now a single zipfile to be passed on to another function
                    zip_list.append(os.path.join(source_dir, results[x]))
                return zip_list


def cannot_id_changes(shp_tuples):
    """
    This script asks the user to identify  any changes shapefiles in the event that other steps did not locate them.

    :param shp_tuples:  set of .shp files that were already identified in the get_shp function.
                        Consists of (dirname, filenames)
    :return:            no idea yet but I think it's a list of changes identified by user input
    """
    no_changes_list = [os.path.join(path, name) for path, name in shp_tuples]
    print no_changes_list

    question = """=========================================================================
                The following shapefiles could not be identified.
                Which, if any, are changes files?
                Input a list of the numbers for each shapefile that is a changes file,
                do not enter anything if you are unsure.
                To see a list of Attribute fields for a given shapefile
                enter 'desc #' where the number corresponds to the shapefile of interest.
                =========================================================================
                """
    for name in no_changes_list:
        index = no_changes_list.index(name)
        question += '{0}: {1}\n'.format(index, name)
    while 1:
        core.notify()
        x = raw_input(question)

        if not x:
            return None

        elif x.startswith('desc '):
            try:
                descx = int(x.split(' ')[1])
                if descx <= len(no_changes_list)-1:
                    print 'Describing {0}, {1}:'.format(descx, no_changes_list[descx])
                    core.desc_shp(no_changes_list[descx])
                else:
                    print 'Could not describe item "{0}". It is out of range.'.format(x[5:])
                continue
            except:
                print 'Could not describe item "{0}". It is out of range.'.format(x[5:])
                continue

        else:
            try:
                listx = list(int(y) for y in x.split(','))
            except:
                print 'Could not parse list "{0}". Please try again.'.format(x)
                continue

        out_list = []
        try:
            for z in listx:
                out_list.append(no_changes_list[z])
        except:
            print 'Could not use list. Value "{0}" is out of range.'.format(z)
            continue

        else:
            return out_list

if __name__ == "__main__":
    wrksp = r'C:\some_dir'
    files = []
    for x, y, z in os.walk(wrksp):
        files.append((x, z))

    shp_tup = core.get_shps(files)
    print shp_tup
    cannot_id_changes(shp_tup)

if __name__ == "__main__":
    swim = r'H:\!!!HDriveStuff\BQARP\20\swim\20'
    unzip_these = which_zip(swim, 'KS')
    print unzip_these