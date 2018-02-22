import urllib
import json


def get_api(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


def parse_stats(data):
    paying = dict()
    res = data['result']['simplemultialgo']
    for algo in res:
        name = algo['name']
        pay = float(algo['paying'])
        port = int(algo['port'])
        paying[name] = {'pay': pay,
                        'port': port}
    return paying


def dump_empy(data):
    empty = list()
    res = data['result']['simplemultialgo']
    for algo in res:
        empty.append({'name': algo['name'], 'speed': 0, 'command': ''})
    return {'hashrate': empty}
