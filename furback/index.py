from collections import namedtuple, defaultdict, Counter
import re

bad_stuff = re.compile(r"[\.,-\/#!$%\^&\*;\?:{}=\-_`~()]")

Script = namedtuple("Script", ("name", "words", "priority", "body"))
Runner = namedtuple("Runner", ("words", "runner"))

class Index(object):
    def __init__(self):
        self.runner_id = 1
        # idx maps each word to a set of scripts
        self.idx = defaultdict(lambda: [])
        # info maps each script name to a Script()
        self.info = {}
        # runners is an array of Runners()
        self.runners = []

    def script(self, name, words, priority, body):
        existing = self.info.get(name, None)
        self.info[name] = Script(name, words, int(priority), body)
        if existing is None:
            # first time we have seen this script
            for word in words:
                self.idx[word].append(name)
        else:
            # we need to figure out what to add and remove
            to_remove = existing.words - words
            to_add = words - existing.words

            for word in to_remove:
                self.idx[word].remove(name)
            for word in to_add:
                self.idx[word].append(name)

    def listen_for(self, words, runner):
        print("Listening for %s" % words)
        self.runners = [ r for r in self.runners if r.runner != runner ]
        self.runners.append(Runner(words, runner))

    def lookup(self, text):
        # prune dead runners
        self.runners = [r for r in self.runners if r.runner.running() ]

        tokens = re.sub(bad_stuff, "", text.lower()).split(" ")

        for token in tokens:
            print("Checking for runners: `%s`" % token)

            # short circuit match runners
            for info in self.runners:
                # protect against runners dieing between beginning of lookup and here
                if info.runner.running():
                    for word in info.words:
                        if word in token:
                            print("Found runner: `%s` in `%s`" % (word, token))
                            return info.runner

        matches = Counter()
        for token in tokens:
            for word in self.idx.keys():
                if word in token:
                    for script_name in self.idx[word]:
                        print("Found matching script: %s because `%s` in `%s`" % (script_name, word, token))
                        matches[script_name] += 1

        if len(matches):
            # get a sorted list of all scripts ordered by their match count, priority and name
            sorted_scripts = sorted(self.info.values(), key=lambda i: (matches[i.name], i.priority, i.name), reverse=True)
            script = sorted_scripts[0]
            print("Found script: %s (%d, %d, %s)" % (script.name, matches[script.name], script.priority, script.name))
            return script.body
