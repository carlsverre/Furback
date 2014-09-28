import sys
import select
import signal
import random

_initial_input = None

FURBY_COMMANDS = {
    "sleep": 700,
    "burp": 701,
    "fart": 704,
    "wakeup": 705,
    "happy": 710,
    "cough": 711,
    "yawn": 718,
    "whisper": 719,
    "hypno": 820,
    "food" : 350, 
}

def _wait_input(timeout):
    r, w, e = select.select([ sys.stdin ], [], [], timeout)
    if sys.stdin in r:
        new = sys.stdin.readline().strip()
        sys.stderr.write("Received input: `%s`\n" % new)
        return new
    else:
        sys.stderr.write("No input received after %f seconds\n" % timeout)
        sys.exit(0)

def _exit(signal, frame):
    sys.stderr.write("Exiting due to signal\n")
    sys.exit(0)

def _init():
    global _initial_input

    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)

    _initial_input = _wait_input(1)
    return _initial_input

def get_input():
    return _initial_input

def listen_for(words, timeout=1):
    sys.stdout.write('listen_for %s\n' % ','.join(str(w).strip() for w in words))
    sys.stdout.flush()

    r, w, e = select.select([ sys.stdin ], [], [], timeout)
    if sys.stdin in r:
        new = sys.stdin.readline()
        return new
    else:
        sys.exit(0)

def say(output):
    for line in output.strip().split("\n"):
        line = line.strip()
        if line:
            sys.stdout.write("say %s\n" % line)
    sys.stdout.flush()

def wait(wait_time):
    sys.stdout.write("wait %f\n" % wait_time)
    sys.stdout.flush()

def do(command_name):
    assert command_name in FURBY_COMMANDS, "Must specify a valid furby command"
    sys.stdout.write("do %d\n" % FURBY_COMMANDS[command_name])
    sys.stdout.flush()

def sing():
    sys.stdout.write("do %d\n" % random.choice([721,722,723,734]))
    sys.stdout.flush()
    
