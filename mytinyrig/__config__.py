import os
from mytinyrig.misc import try_import


def get_config(configdir):

    if configdir is not None:
        MY_WORKERS = configdir
    elif os.environ.get('MY_WORKERS'):
        MY_WORKERS = os.environ.get('MY_WORKERS')
    else:
        base, name = os.path.split(os.path.abspath(__file__))
        MY_WORKERS = os.path.join(base, 'workers')
    base, name = os.path.split(os.path.abspath(MY_WORKERS))
    my_workers = try_import(base, name)
    return my_workers
