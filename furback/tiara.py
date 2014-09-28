import subprocess
import os

def Insult():
    return subprocess.Popen(["node","/vagrant/Furback/plugins/Insult.js"], stdout=subprocess.PIPE).communicate()[0]

def Respond(tweet):
    os.system("echo '%s' >> tweets.txt" % tweet)
    return subprocess.Popen(["node","/vagrant/Furback/plugins/Respond.js"], stdout=subprocess.PIPE).communicate()[0]
