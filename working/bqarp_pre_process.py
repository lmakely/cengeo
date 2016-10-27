__author__ = 'Lauren Makely'

import os
import logging
import arcpy
import zipfile
import winsound

swim = r'\\batch4.ditd.census.gov\mtdata003_geo_SWIM\BQARP\2016'
lisrds = r''
working_dir = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP'
template_mxd = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\Assessment.mxd'


def notify():
    """
    Attempts to notify user that some kind of input is needed from them. Function may not work on all systems
    """

    try:
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    except:
        pass


def extract_zip(source, output):
    """
    Function goes to zip file and unzips it to the specified output location.

    :param source:  path of zip file to be unzipped
    :param output:  path to folder where unzipped files should be placed
    :return:        nothing (files will be placed in folder)
    """
    with zipfile.ZipFile(source, 'r') as zf:
        zf.extractall(output)


def find_files(search_folder, *search_string):
    """
    Generates a list of files that matches the search criteria.

    :param search_folder:   folder to search within
    :param search_string:   filetype to look for
    :return:                path for the files  that contain the search string
    """
    for f in os.listdir(search_folder):
        # if the extension for a file is '.zip' it gets produced
        for ext in search_string:
            if f.endswith(ext):
                yield f


def create_and_setup_mxd(template_mxd, where_to_save_mxd, directory_of_features):
    """

    :param where_to_save_mxd:   file path to project folder
    :param folder_to_walk:      file path to data folder. all data inside (even in a geodatabase) will be added to mxd
    :return:
    """

    logger = logging.getLogger()

    # setup mxd and map document
    arcpy.env.overwriteOutput = True
    mxd = arcpy.mapping.MapDocument(template_mxd)
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

    add_these_shps = find_files(directory_of_features, '.shp')
    add_these_fcs = find_files(directory_of_features, '.gdb')

    for gdb in add_these_fcs:
        arcpy.env.workspace = os.path.join(directory_of_features, gdb)
        fcs = arcpy.ListFeatureClasses()
        for fc in fcs:
            try:
                add_layer = arcpy.mapping.Layer(fc)
                logger.info(fc)
                arcpy.mapping.AddLayer(df, add_layer, "AUTO_ARRANGE")
            except:
                logger.info('Failed to add {} to mxd'.format(fc))
                continue

        mxd_layers = arcpy.mapping.ListLayers(mxd)

        for shp in add_these_shps:
            if shp in mxd_layers:
                pass
            else:
                try:
                    add_layer = arcpy.mapping.Layer(os.path.join(directory_of_features, shp))
                    logger.info(shp)
                    arcpy.mapping.AddLayer(df, add_layer, "AUTO_ARRANGE")
                except:
                    logger.info('Failed to add {} to mxd'.format(shp))
                    continue

    output_mxd = os.path.join(where_to_save_mxd, 'BQARP_Assessment.mxd')
    logger.info('Saving mxd to {}'.format(output_mxd))
    mxd.saveACopy(output_mxd)


def make_header(my_string, char='*'):
    """
    formats a header that will use any character and fit to any length string

    :param my_string:   string to be printed as the header
    :param char:        the character that will frame the header
    :return:

    example:
        from cengeo import core
        bas_id = "32613169140"
        print cengeo.core.make_header("BAS ID: {ID}".format(bas_id), "+")

    output example (from above):
        +++++++++++++++++++++++
        + BAS ID: 32613169140 +
        +++++++++++++++++++++++

    """
    my_string = "{c} {s} {c}".format(c=char, s=my_string)
    output = "{b}\n{s}\n{b}".format(b=char * len(my_string), s=my_string)
    return output


def which_zip(source_dir, *search_id):
    """
    Identifies zip files to be unzipped and then processed. If it finds no zip files, prints an error.
    If it finds multiple zip files that correspond with the search_id it needs then it will ask for the user
    to choose a zip file from a list of found files.

    :param source_dir:  directory where the zip file should be found
    :param search_id:   the id of the place being processed. if left blank, will return the whole directory of zip files
    :return results:    list of zipfile(s); by the end of the function, it is a single zipfile
    """

    zip_results = list(find_files(source_dir, '.zip'))

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
            notify()  # notifies user there's a problem
            x_list = [int(x) for x in raw_input(question).split()]  # asks user which zip file to use by index number

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
                    print make_header('  Preparing to unzip: {0}  '.format(results[x]), '*')
                    # results is now a single zipfile to be passed on to another function
                    zip_list.append(os.path.join(source_dir, results[x]))
                return zip_list


# for now, this just gets the ST code to put a temp folder in so the user can move them later or whatever
# this will also be a permanent directory on the P drive eventually
state_code = str(input("Which state is being processed? Please enter a two digit state code: "))
swim = os.path.join(swim, state_code)
state_dir = os.path.join(working_dir, state_code)

logging.basicConfig(filename=os.path.join(state_dir, 'log.txt'), level=logging.DEBUG, format='%(message)s', filemode='w')
logger = logging.getLogger()
logger.info(make_header('  Processing state {}  '.format(state_code)))

# a couple more directories get formed here
unzipped_dir = os.path.join(state_dir, 'SWIM_FILES')

# run: which_zip on a swim/swecs folder (stores a list of values)
current_zips = list(which_zip(swim))
logger.info('Unzipping the following to {0}:'.format(unzipped_dir))

# run: extract_zip on chosen zip files. This might take a while.
for zips in current_zips:
    logger.info('\n\t{0}'.format(zips))
    extract_zip(zips, unzipped_dir)

# function?: pull lisrds data like bas does (not currently possible so order it)
# function: move LISRDS data to workspace or just access it


# func: add all data to mxd?
print('Adding files to mxd...')
logger.info(make_header('Adding files to mxd'))
logger.info('\n')
create_and_setup_mxd(template_mxd, state_dir, unzipped_dir)