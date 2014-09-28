import redis
import time

class DB(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.sub = self.r.pubsub()
        self.sub.subscribe("changes")

    def save_script(self, name, content, priority, words):
        self.r.hmset(name, {
            "name": name,
            "created": time.time(),
            "body": content,
            "priority": priority,
            "words": ','.join(words)
        })
        self.r.sadd("scripts", name)
        self.r.publish("changes", name)

    def get_scripts(self):
        script_names = self.r.smembers("scripts") or []
        scripts = [self.r.hgetall(s) for s in script_names]
        for script in scripts:
            script['words'] = {w.strip() for w in script['words'].split(',') if w.strip()}
        return scripts

    def get_changes(self):
        out = self.sub.get_message()
        if out is not None:
            return out['data']
