#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from mytinyrig.processing import polls, dump_yaml
from mytinyrig.misc import package_files
from mytinyrig import __version__, __config__

VERSION = __version__.VERSION
DATE = __version__.DATE
AUTHOR = __version__.AUTHOR
MAIL = __version__.MAIL


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dump',  dest='dump',
                        help='Print an empty yaml worker file',
                        action='store_true')
    parser.add_argument('-w', '--wallet',  dest='wallet',
                        help='Nicehash wallet address', type=str,
                        default='3Dsuk4X67SBwcFjVxrnCcoXn8jyowRqScw')
    parser.add_argument('-r', '--region',  dest='region',
                        help='Nicehash servers region', type=str,
                        choices=['eu', 'usa', 'hk', 'jp', 'in', 'br'],
                        default='eu')
    parser.add_argument('-t', '--time',  dest='poltime',
                        help='Polling time in minutes',
                        type=int, default=30)
    parser.add_argument('-n', '--n-mean',  dest='n_avg',
                        help=('Number of polls saved '
                              'to compute the mean profitability'),
                        type=int, default=5)
    parser.add_argument('-l', '--logdir',  dest='logdir',
                        help='Logs output folder',
                        type=str, default=os.getcwd())
    parser.add_argument('-c', '--confdir',  dest='confdir',
                        help=('Folder containing the workers '
                              'yaml configurations'), type=str)
    args = parser.parse_args()

    api = 'https://api.nicehash.com/api?method=simplemultialgo.info'

    polling_time = args.poltime * 60
    if args.dump is True:
        print(dump_yaml(api))
    else:
        MY_WORKERS = __config__.get_config(args.confdir)
        workers = package_files(MY_WORKERS, '.yaml')
        with open(os.devnull, 'w') as dev_null:
            p = polls(workers, api, polling_time,
                      args.n_avg, args.wallet, args.region, args.logdir, sys.stderr, dev_null)
            p.start()


if __name__ == "__main__":
    main()
