#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import operator
import argparse
from mytinyrig.misc import package_files
from mytinyrig import nicehash
from mytinyrig import __version__, __config__

VERSION = __version__.VERSION
DATE = __version__.DATE
AUTHOR = __version__.AUTHOR
MAIL = __version__.MAIL


def get_rig_stats(rig_hashrate, stats):
    res = dict()
    with open(rig_hashrate, 'rb') as rig_yaml:
        try:
             data = yaml.load(rig_yaml)
        except yaml.YAMLError as exc:
            raise(exc)
    for algo in data['hashrate']:
        res[algo['name']] = algo['speed'] * stats[algo['name']] / 1e6
    return(sorted(res.items(), key=operator.itemgetter(1), reverse=True))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dump',  dest='dump',
                        help='Dump an empty yaml file',
                        action='store_true')
    args = parser.parse_args()
   
    api='https://api.nicehash.com/api?method=simplemultialgo.info'

    data = nicehash.get_api(api)

    if args.dump is True:
        print yaml.safe_dump(nicehash.dump_empy(data), default_flow_style=False)
    else:

        stats = nicehash.parse_stats(data)
        MY_RIGS = __config__.MY_RIGS
        rigs = package_files(MY_RIGS, '.yaml')
        for rig in rigs:
            res = get_rig_stats(rig, stats)
            print('\t - Profitability for rig %s:' %
                os.path.splitext(os.path.split(rig)[1])[0])
            for r in res:
                print ('%s: daily: %f mBTC/day' % (r[0], r[1]))
if __name__ == "__main__":
    main()
