from mytinyrig import nicehash
from mytinyrig.logs import log
from multiprocessing import Process
import subprocess
import operator
import signal
import shlex
import time
import yaml
import os


class process:

    def __init__(self, command):
        command = shlex.split(command)
        self.proc = subprocess.Popen(command,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            bufsize=4096)

    def __iter__(self):
        for line in iter(self.proc.stdout.readline, ''):
            yield line.decode('utf-8').strip()

    def pid(self):
        return self.proc.pid

    def close(self):
        self.proc.kill()
        self.proc.stdout.close()


class polls:

    def __init__(self, workers_conf, api, timeout, logdir):
        self.api = api
        self.logdir = logdir
        self.log = log('mytinyrig', self.logdir).log
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
                    worker.running, worker.name, worker.profit[0]['mbtc'])
                self.log.info(line)
                #print (worker.name, worker.running,
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
            self.workers.append(worker(conf, self.logdir, self.log))

class worker:

    def __init__(self, conf, logdir, parentlog):
        self.running = None
        self.logdir = logdir
        self.conf = conf
        self.name = os.path.splitext(
            os.path.split(self.conf)[1])[0]
        with open(self.conf, 'rb') as conf_yaml:
            try:
                self.conf_data = yaml.load(conf_yaml)
            except yaml.YAMLError as exc:
                raise(exc)
        self.log = log(self.name, self.logdir).log
        self.parentlog = parentlog
        self.commands = get_commands(self.conf_data)

    def set_profit(self, stats):
        profit = list()
        res = get_stats(self.conf_data, stats)
        for r in res:
            if not self.commands[r[0]]:
                pass
            elif r[1] > 0:
                profit.append({
                    'name': r[0], 'mbtc': r[1]})
        self.profit = profit

    def check_running(self):
        if self.running == self.profit[0]['name']:
            self.parentlog.info('keep mining %s' % self.running)
        else:
            self.parentlog.info('switch to mining %s' % self.profit[0]['name'])
            if self.running is not None:
                self.log.info('Terminate process %s' % self.process.pid())
                self.process.proc.kill()
                self.stream_log.terminate()
            self.start_process(self.profit[0]['name'])
            self.stream_log = Process(target=log_worker,
                args=(self.process, self.log, ))
            self.stream_log.start()
            self.running = self.profit[0]['name']

    def start_process(self, algo):
        self.process = process(self.commands[algo])

def get_stats(conf_data, stats):
    res = dict()
    for algo in conf_data['hashrate']:
        res[algo['name']] = algo['speed'] * stats[algo['name']] / 1e6
    return(sorted(res.items(), key=operator.itemgetter(1), reverse=True))

def get_commands(conf_data):
    res = dict()
    for algo in conf_data['hashrate']:
        res[algo['name']] = algo['command']
    return res

def log_worker(process, log):
    for line in process:
        log.info(line)
