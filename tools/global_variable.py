def _init():
    global GLOBALS_DICT
    GLOBALS_DICT = {}

def _set(name, value):
    try:
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False

def _get(name):
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return 0