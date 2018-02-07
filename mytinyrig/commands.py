#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import json
import yaml
import operator
import argparse
from mytinyrig import __version__, __config__

VERSION = __version__.VERSION
DATE = __version__.DATE
AUTHOR = __version__.AUTHOR
MAIL = __version__.MAIL

def get_nh_data(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data

def parse_nh_stats(data, algos):
    paying = dict()
    res = data['result']['simplemultialgo']
    for algo in res:
        name = algos[algo['algo']]
        pay = float(algo['paying'])
        paying[name] = pay
    return paying

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

def dump_empy_yaml(algos):
    empty = list()
    for algo in algos:
        empty.append({'name': algos[algo], 'speed': 0, 'command': ''})
    return {'hashrate' : empty}

def main():
    MY_RIGS = __config__.MY_RIGS
    print MY_RIGS
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rig',  dest='rig',
                        help='Rig benchmark hashrate yaml file',
                        type=str)
    parser.add_argument('-d', '--dump',  dest='dump',
                        help='Dump an empty yaml file',
                        action='store_true')
    args = parser.parse_args()
   
    if args.dump is False and args.rig is None:
        raise(Exception('Either -r or -d argument is required'))

    api='https://api.nicehash.com/api?method=simplemultialgo.info'
    algos = {
      0: 'Scrypt', 1: 'SHA256', 2: 'ScryptNf',
      3: 'X11', 4: 'X13', 5: 'Keccak',
      6: 'X15', 7: 'Nist5', 8: 'NeoScrypt',
      9: 'Lyra2RE', 10: 'WhirlpoolX', 11: 'Qubit',
      12: 'Quark', 13: 'Axiom', 14: 'Lyra2REv2',
      15: 'ScryptJaneNf16', 16: 'Blake256r8', 17: 'Blake256r14',
      18: 'Blake256r8vnl', 19: 'Hodl', 20: 'DaggerHashimoto',
      21: 'Decred', 22: 'CryptoNight', 23: 'Lbry',
      24: 'Equihash', 25: 'Pascal', 26: 'X11Gost',
      27: 'Sia', 28: 'Blake2s', 29: 'Skunk'}

    if args.dump is True:
        print yaml.dump(dump_empy_yaml(algos), default_flow_style=False)
    else:
        data = get_nh_data(api)

        stats = parse_nh_stats(data, algos)
        res = get_rig_stats(args.rig, stats)
        for r in res:
            print '%s: daily: %f mBTC/day' % (r[0], r[1])
if __name__ == "__main__":
    main()
