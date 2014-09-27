import redis

class DB(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.sub = self.r.pubsub()
        self.sub.subscribe("changes")

    def get_scripts(self):
        script_names = self.r.get("scripts") or []
        return [self.r.hgetall(s) for s in script_names]
            
        self.sub_output = self.r.pubsub()
        self.sub_output.subscribe("text_output")

    def get_changes(self):
        out = self.sub.get_message()
        if out is not None:
            return out['data']
