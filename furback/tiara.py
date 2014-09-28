import subprocess
import os

def Insult():
    return subprocess.Popen(["node","/vagrant/plugins/Insult.js"], stdout=subprocess.PIPE).communicate()[0]

def Respond(tweet):
    os.system("echo '%s' >> ./plugins/tweets.txt" % tweet.replace("'"," "))
    res =  subprocess.Popen(["node","/vagrant/plugins/Respond.js"], stdout=subprocess.PIPE).communicate()[0].strip()
    os.system("echo '%s' >> ./plugins/tweets.txt" % res.replace("'"," "))
    return res
