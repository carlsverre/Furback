import subprocess
import os

def Insult():
    return subprocess.Popen(["node","Insult.js"], stdout=subprocess.PIPE).communicate()[0]

def Respond(tweet):
    os.system("echo '%s' >> tweets.txt" % tweet)
    return subprocess.Popen(["node","Respond.js"], stdout=subprocess.PIPE).communicate()[0]
