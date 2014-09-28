from furback import furby
from furback import tiara
import random

if __name__ == '__main__':
    furby.say(tiara.Insult())
    furby.do(random.choice(["cough", "fart", "burp"]))
