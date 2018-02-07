import os
from mytinyrig.misc import try_import

MY_RIGS = os.environ.get('MY_RIGS')

if MY_RIGS:
    base, name = os.path.split(os.path.abspath(MY_RIGS))
    my_rigs = try_import(base, name)
    MY_RIGS = my_rigs
else:
    base, name = os.path.split(os.path.abspath(__file__))
    my_rigs = try_import(base, 'rigs')
    MY_RIGS = my_rigs
