from furback import furby
import tiara
import ranomd

if __name__ == '__main__':
    furby.say(tiara.Insult())
    if random.choice([True,False]):
        furby.do(random.choice(["laugh","fart","sneeze"]))
