__author__ = 'Lauren Makely'

import core
import os


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