__author__ = 'Lauren Makely'


def make_header(my_string, char='*'):
    """
    formats a header that will use any character and fit any length string

    :param my_string:   string to be printed as the header
    :param char:        the character that will frame the header
    :return:
    """
    my_string = "{c} {s} {c}".format(c=char, s=my_string)
    output = "{b}\n{s}\n{b}".format(b=char * len(my_string), s=my_string)
    return output