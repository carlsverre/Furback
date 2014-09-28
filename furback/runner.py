import tempfile
import os
import subprocess
import stat
import copy
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
PYTHON = os.path.join(ROOT, "python_env", "bin", "python")

class Runner(object):
    def __init__(self, script_content):
        self.script_file = tempfile.NamedTemporaryFile(delete=False)
        os.chmod(self.script_file.name, stat.S_IREAD | stat.S_IEXEC | stat.S_IWRITE)
        self.script_file.write(script_content)
        self.script_file.flush()
        self.script_file.close()

    def __del__(self):
        os.unlink(self.script_file.name)

    def run(self):
        env = copy.deepcopy(os.environ)
        env['PYTHONPATH'] = ':'.join(sys.path)

        self.proc = subprocess.Popen([PYTHON, self.script_file.name], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)

    def write(self, text):
        self.proc.stdin.write(text + "\n")
        self.proc.stdin.flush()

    def read(self):
        return self.proc.stdout.readline()

    def running(self):
        return self.proc.poll() is None
