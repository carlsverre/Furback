from furback import furby
from furback import tiara
import random

if __name__ == '__main__':
    furby.say(tiara.Insult())
    if random.choice([True,False]):
        furby.do(random.choice(["cough","fart","burp"]))
