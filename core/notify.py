__author__ = 'makel004'

import winsound


# plays a notification sound, unsure if actually works
def notify():
    """
    Attempts to notify user that some kind of input is needed from them. Function may not work on all systems
    """

    try:
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    except:
        pass