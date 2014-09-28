import requests as r
import random
from furback import furby

def RandomFilmInTheaters():
    requestStr = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?page_limit=16&page=1&country=us&apikey=g2kvspudnrghwq8nfyak258t"
    result = r.get(requestStr)
    if result.status_code == 200:
        return random.choice(result.json()['movies'])
    else:
        return {"title": "The Furby Movie"}

film = None

def RatingOpinion(rating):
    if rating < 40:
        return random.choice(["It looks lame.", "I heard it sucks.", "I bet its boring.", "Eww."])
    elif rating < 60:
        return random.choice(["It looks ok-ish.", "I heard its boring.", "Looks mediocre.", "Seriously?"])
    elif rating < 80:
        return random.choice(["It looks pretty good.", "Sounds like fun.", "Laugh a minute!", "I'd see that."])
    return random.choice(["It looks awesome!", "Its gonna blow your mine!", "Best movie ever.", "Lets go!"])


def Handle(query):
    global film
    if "theater" in query or "movie" in query:
        film = RandomFilmInTheaters()
        furby.say("Go see %s. %s" % (film['title'], RatingOpinion(film["ratings"]["audience_score"])))
        query = furby.listen_for(["who","actor","star"], timeout=60.0)
        Handle(query)
    elif film and "who" in query or "actor" in query or "star" in query:
        furby.say("It's starring %s.  %s." % (random.choice(film["abridged_cast"])["name"], 
                                              random.choice(["What a hottie","I don't like them", "I love them", "What a hearthrob", "I'd see that", 
                                                             "LAME", "I'd tap that"])))

if __name__ == "__main__":
    query = furby.get_input()
    Handle(query)
