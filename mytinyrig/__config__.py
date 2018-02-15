import os
from mytinyrig.misc import try_import

MY_WORKERS = os.environ.get('MY_WORKERS')

if MY_WORKERS:
    base, name = os.path.split(os.path.abspath(MY_WORKERS))
    my_workers = try_import(base, name)
    MY_WORKERS = my_workers
else:
    base, name = os.path.split(os.path.abspath(__file__))
    my_workers = try_import(base, 'workers')
    MY_WORKERS = my_workers
