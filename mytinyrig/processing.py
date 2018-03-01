from __future__ import division

from mytinyrig import nicehash
from mytinyrig.logs import mytinylog
from multiprocessing import Process
import subprocess
import operator
import shlex
import time
import yaml
import os


class process:

    def __init__(self, command):
        command = shlex.split(command)
        self.proc = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, bufsize=4096)

    def __iter__(self):
        for line in iter(self.proc.stdout.readline, ''):
            yield line.decode('utf-8').strip()

    def pid(self):
        return self.proc.pid

    def close(self):
        self.proc.kill()
        self.proc.stdout.close()


class polls:

    def __init__(self, workers_conf, api, timeout,
                 n, wallet, region, logdir):
        self.n = n
        self.wallet = wallet
        self.region = region
        self.api = api
        self.logdir = logdir
        self.log = mytinylog('mytinyrig', self.logdir).log
        self.workers_conf = workers_conf
        self.timeout = timeout
        self.stats = None
        self.refresh_stats()
        self.set_workers()

    def start(self):
        while True:
            self.refresh_stats()
            for worker in self.workers:
                worker.set_profit(self.stats)
                worker.check_running()
                line = 'Mining %s at worker %s: %f mBTC/day' % (
                    worker.running, worker.name,
                    worker.profits[worker.running].mean())
                self.log.info(line)
                # print (worker.name, worker.running,
                #    worker.profit[0], worker.commands[worker.running])
            time.sleep(self.timeout)

    def refresh_stats(self):
        try:
            data = nicehash.get_api(self.api)
            self.stats = nicehash.parse_stats(data)
        except IOError:
            if self.stats is None:
                self.log.warning('retrying API in 5 seconds')
                time.sleep(5)
                self.refresh_stats()
            else:
                pass

    def set_workers(self):
        self.workers = list()
        for conf in self.workers_conf:
            self.workers.append(
                worker(conf, self.stats, self.n,  self.wallet,
                       self.region, self.logdir, self.log))


class worker:

    def __init__(self, conf, stats, n, wallet,
                 region, logdir, parentlog):
        self.running = None
        self.logdir = logdir
        self.conf = conf
        self.n = n
        self.name = os.path.splitext(
            os.path.split(self.conf)[1])[0]
        with open(self.conf, 'rb') as conf_yaml:
            try:
                self.conf_data = yaml.load(conf_yaml)
            except yaml.YAMLError as exc:
                raise(exc)
        self.log = mytinylog(self.name, self.logdir).log
        self.log.propagate = False
        self.parentlog = parentlog
        self.commands = get_commands(self.conf_data, stats,
                                     wallet, region, self.name)
        self.profits = dict()
        for algo in self.commands:
            self.profits[algo] = statspay(self.n)

    def set_profit(self, stats):
        res = get_stats(self.conf_data, stats)
        for r in res:
            if not self.commands[r[0]]:
                pass
            elif r[1] > 0:
                self.profits[r[0]].add(r[1])

    def check_running(self):
        ranks = ranks_profits(self.profits)
        if self.running == ranks[0][0]:
            self.parentlog.info('keep mining %s' % self.running)
        else:
            self.parentlog.info('switch to mining %s' % ranks[0][0])
            if self.running is not None:
                self.log.info('Terminate process %s' % self.process.pid())
                self.process.proc.kill()
                self.stream_log.terminate()
            self.start_process(ranks[0][0])
            self.stream_log = Process(target=log_worker,
                                      args=(self.process, self.log, ))
            self.stream_log.start()
            self.running = ranks[0][0]

    def start_process(self, algo):
        self.process = process(self.commands[algo])


class statspay:

    def __init__(self, n):
        self.n = n
        self.pays = list()

    def add(self, value):
        self.pays.append(value)
        if len(self.pays) > self.n:
            del self.pays[0]

    def mean(self):
        try:
            return sum(self.pays) / len(self.pays)
        except ZeroDivisionError:
            return 0


def get_stats(conf_data, stats):
    res = list()
    for algo in conf_data['hashrate']:
        res.append(
            (algo['name'], algo['speed'] * stats[algo['name']]['pay'] / 1e6))
    return res


def ranks_profits(paystats):
    res = dict()
    for algo in paystats:
        res[algo] = paystats[algo].mean()
    return(sorted(res.items(), key=operator.itemgetter(1), reverse=True))


def get_commands(conf_data, stats, wallet, region, worker_name):
    res = dict()
    for algo in conf_data['hashrate']:
        algo_name = algo['name']
        port = stats[algo_name]['port']
        nicehash_url = '%(algo)s.%(region)s.nicehash.com' % {
            'algo': algo_name, 'region': region}
        command = algo['command'] % {
            'url': nicehash_url, 'port': port,
            'wallet': wallet, 'worker': worker_name}
        res[algo_name] = command
    return res


def log_worker(process, log):
    for line in process:
        log.info(line)


def dump_yaml(api):
    try:
        data = data = nicehash.get_api(api)
    except IOError:
        Exception('API is not available, retrying later.')
    return yaml.safe_dump(nicehash.dump_empy(data),
                          default_flow_style=False)
