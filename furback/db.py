import redis

class DB(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_scripts(self):
        return self.r.hkeys("scripts")
