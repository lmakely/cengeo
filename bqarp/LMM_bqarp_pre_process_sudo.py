__author__ = 'Lauren Makely'

import core
import os
import logging

swim = r'\\batch4.ditd.census.gov\mtdata003_geo_SWIM\BQARP\2016'
lisrds = r''
working_dir = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP'
template_mxd = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Assessment.mxd'


# def bqarp_preprocess(zip_file):
# figure out where the heck this file is going. build regex (eventually) to identify the STCOU in a file name (or not)
# for now, this just gets the ST code to put a temp folder in so the user can move them later or whatever
# this will also be a permanent directory on the P drive eventually
state_code = str(input("Which state is being processed? Please enter a two digit state code: "))
swim = os.path.join(swim, state_code)
state_dir = os.path.join(working_dir, state_code)

logging.basicConfig(filename=os.path.join(state_dir, 'log.txt'), level=logging.DEBUG, format='%(message)s', filemode='w')
logger = logging.getLogger()
logger.info(core.make_header('  Processing state {}  '.format(state_code)))

# a couple more directories get formed here
unzipped_dir = os.path.join(state_dir, 'SWIM_FILES')

# run: which_zip on a swim/swecs folder (stores a list of values)
current_zips = list(core.which_zip(swim))
logger.info('Unzipping the following to {0}:'.format(unzipped_dir))

# run: extract_zip on chosen zip files. This might take a while.
for zips in current_zips:
    logger.info('\n\t{0}'.format(zips))
    core.extract_zip(zips, unzipped_dir)

# function?: pull lisrds data like bas does (not currently possible so order it)
# function: move LISRDS data to workspace or just access it


# func: add all data to mxd?
print('Adding files to mxd...')
logger.info(core.make_header('Adding files to mxd'))
logger.info('\n')
core.create_and_setup_mxd(template_mxd, state_dir, unzipped_dir)