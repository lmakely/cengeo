__author__ = 'Lauren Makely'

import shutil
import os


def move_file(input_shp, output_folder, extension):
    """
    Takes in a folder and identifies all the files in that folder of that extension. Then it moves the files
    (and any related files) to the new folder. Works best with shapefiles.

    :param input_shp:       file to be moved (need to test this with wildcard values)
    :param output_folder:   folder file should be moved to
    :return:
    """
    if input_shp.endswith(extension):
        print('----------------------------------------------------------------------------------')

        if os.path.exists(output_folder) is False:
            os.mkdir(output_folder)

        folder, name = os.path.split(input_shp)

        print("About to move all files associated with the following file: {0}".format(name))
        ext = len(extension)
        name_no_ext = name[:-ext]
        print name_no_ext
        move_list = os.listdir(folder)  # creates a list of files in the directory

        for move in move_list:
            if name_no_ext in move:
                print('Moving: {0}'.format(move))
                move_files = os.path.join(folder, move)
                shutil.move(move_files, output_folder)

if __name__ == "__main__":
    wrks = r'C:\shapefiles'
    otps = r'C:\outputs'

    for path, recur, files in os.walk(wrks):
        for f in files:
            shp = os.path.join(path, f)
            move_file(shp, otps, '.xls')
        break