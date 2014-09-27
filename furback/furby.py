import sys
import fileinput

FURBY_COMMANDS = {
    "sleep": 862,
    "laugh": 863,
    "burp": 864,
    "fart": 865,
    "purr": 866,
    "sneeze": 867,
    "sing": 868,
    "talk": 869,
}

def listen():
    for line in fileinput.input():
        yield line

def say(output):
    for line in output.split("\n"):
        sys.stdout.write("say %s\n" % line.strip())

def wait(wait_time):
    sys.stdout.write("wait %f\n" % wait_time)

def do(command_name):
    assert command_name in FURBY_COMMANDS, "Must specify a valid furby command"
    sys.stdout.write("do %d\n" % FURBY_COMMANDS[command_name])
