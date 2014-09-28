import subprocess
import os

def Insult():
    return subprocess.Popen(["node","/vagrant/plugins/Insult.js"], stdout=subprocess.PIPE).communicate()[0]

def Respond(tweet):
    os.system("echo '%s' >> ./plugins/tweets.txt" % tweet)
    return subprocess.Popen(["node","/vagrant/plugins/Respond.js"], stdout=subprocess.PIPE).communicate()[0]
