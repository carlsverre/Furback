import sys
import select

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
}

def get_input():
    return sys.stdin.readline()

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
        sys.stdout.write("say %s\n" % line.strip())
    sys.stdout.flush()

def wait(wait_time):
    sys.stdout.write("wait %f\n" % wait_time)
    sys.stdout.flush()

def do(command_name):
    assert command_name in FURBY_COMMANDS, "Must specify a valid furby command"
    sys.stdout.write("do %d\n" % FURBY_COMMANDS[command_name])
    sys.stdout.flush()
