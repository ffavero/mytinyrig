import multiprocessing
import subprocess
import shlex


class process:

    def __init__(self, command):
        command = shlex.split(command)
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                     bufsize=4096)

    def __iter__(self):
        for line in self.proc.stdout:
            yield line.decode('utf-8')

    def pid(self):
        return self.proc.pid

    def close(self):
        kill_subproc(self.proc)
        self.proc.stdout.close()
