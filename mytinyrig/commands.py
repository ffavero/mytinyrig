#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from mytinyrig.processing import polls
from mytinyrig.misc import package_files
from mytinyrig import __version__, __config__

VERSION = __version__.VERSION
DATE = __version__.DATE
AUTHOR = __version__.AUTHOR
MAIL = __version__.MAIL


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dump',  dest='dump',
                        help='Dump an empty yaml rig file',
                        action='store_true')
    parser.add_argument('-w', '--wallet',  dest='wallet',
                        help='Nicehash wallet address', type=str,
                        default='3Dsuk4X67SBwcFjVxrnCcoXn8jyowRqScw')
    parser.add_argument('-t', '--time',  dest='poltime',
                        help='Polling time in minutes',
                        type=int, default=30)
    args = parser.parse_args()
   
    api='https://api.nicehash.com/api?method=simplemultialgo.info'

    polling_time = args.poltime #* 60
    if args.dump is True:
        print yaml.safe_dump(nicehash.dump_empy(data), default_flow_style=False)
    else:
        MY_WORKERS = __config__.MY_WORKERS
        workers = package_files(MY_WORKERS, '.yaml')
        p = polls(workers, api, polling_time)
        p.start()


if __name__ == "__main__":
    main()
