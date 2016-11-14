__author__ = 'Lauren Makely'

import core
import os
import logging

swim = r'\\batch4.ditd.census.gov\mtdata003_geo_SWIM\BQARP\2016'
lisrds = r''
working_dir = r'H:\!!!HDriveStuff\BQARP'
template_mxd = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\Assessment.mxd'


# figure out where the heck this file is going. build regex (eventually) to identify the STCOU in a file name (or not)
# for now, this just gets the ST code to put a temp folder in so the user can move them later or whatever
# this will also be a permanent directory on the P drive eventually
st_id = str(input("Which state is being processed? Please enter a two digit state code: "))
swim = os.path.join(swim, st_id)
state_dir = os.path.join(working_dir, st_id)

logging.basicConfig(filename=os.path.join(state_dir, 'log.txt'), level=logging.DEBUG, format='%(message)s', filemode='w')
logger = logging.getLogger()
logger.info(core.make_header('  Processing state {}  '.format(st_id)))

# a couple more directories get formed here
unzipped_dir = os.path.join(state_dir, 'LOCAL_FILES')

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
core.create_and_setup_mxd(template_mxd, state_dir, unzipped_dir)