__author__ = 'Lauren Makely'

import core
import bas
import os
import logging

swim = r'\\batch4.ditd.census.gov\mtdata003_geo_SWIM\BQARP\2016'
working_dir = r'H:\!!!HDriveStuff\BQARP'
template_mxd = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS\CARP\BQARP\Tools\Assessment.mxd'

if __name__ == "__main__":
    try:
        # for now, this just gets the ST code to put a temp folder in so the user can move them later or whatever
        # this will also be a permanent directory on the P drive eventually
        state_code = str(input("Which state is being processed? Please enter a two digit state code: "))
        swim = os.path.join(swim, state_code)
        state_dir = os.path.join(working_dir, state_code)
        if not os.path.exists(state_dir):
            os.mkdir(state_dir)

        logging.basicConfig(filename=os.path.join(state_dir, 'log.txt'), level=logging.DEBUG, format='%(message)s', filemode='w')
        logger = logging.getLogger()
        logger.info(core.make_header('  Processing state {}  '.format(state_code)))

        # a couple more directories get formed here
        unzipped_dir = os.path.join(state_dir, 'LOCAL_FILES')

        # run: which_zip on a swim/swecs folder (stores a list of values)
        current_zips = list(bas.which_zip(swim))
        logger.info('Unzipping the following to {0}:'.format(unzipped_dir))

        # run: extract_zip on chosen zip files. This might take a while.
        for zips in current_zips:
            logger.info('\n\t{0}'.format(zips))
            logger.info('\n\n')
            core.extract_zip(zips, unzipped_dir)

        # func: add all data to mxd
        print('Adding files to mxd...')
        logger.info(core.make_header('Adding files to mxd'))
        core.create_and_setup_mxd(template_mxd, state_dir, unzipped_dir)

    except:
        import sys
        print sys.exc_info()[0]
        import traceback
        print traceback.format_exc()

    finally:
        print "Press Enter to continue ..."
        raw_input()