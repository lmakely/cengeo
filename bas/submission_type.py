__author__ = 'Lauren Makely'


def submission_type(filenames):
    """
    figure out MTPS vs GUPS vs digital

    :param filenames:   list of tuples that consist of (dirname, filename). Checks the file names for
                        file types that indicate a specific type of digital submission
    :return:            string containing the type of submission
    """
    subty = []
    for path, name in filenames:
        if name.upper().endswith('FORM.DBF'):
            subty.append('MTPS')
        elif name.upper().endswith('.GUPS'):
            subty.append('GUPS')
        else:
            subty.append('DIGITAL')

    if 'GUPS' in subty:
        return 'GUPS'
    elif 'MTPS' in subty:
        return 'MTPS'
    else:
        return 'DIGITAL'