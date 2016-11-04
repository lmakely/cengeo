__author__ = 'Jeff Ely'

import os


def increment_filename(filename, ext):
    """
    Checks if a filename exists, and increments a digit on the end of it
    until it creates a filename that does not already exist
    """
    i = 1
    while os.path.exists(filename):
        fname = filename.replace(ext, "")
        sufx_fmt = "_{}"

        # if file already has suffix integer, replace it by an integer one greater
        if fname.endswith(sufx_fmt.format(i-1)):
            fname = fname.replace(sufx_fmt.format(i-1), sufx_fmt.format(i))
        else:
            fname += sufx_fmt.format(i)
            i += 1
        filename = fname + ext
        return filename
