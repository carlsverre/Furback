from furback import furby
from furback import yelp
import random

text = furby.get_input()

search = None

terms = ["bar", "restaurant", "dinner", "lunch", "brunch", "cafe", "coffee"]
for term in terms:
    if term in text:
        search = term
        break

businesses = yelp.search(search, limit=10)
current_business = None

def say_business():
    global current_business
    business = random.choice(businesses)
    businesses.remove(business)
    current_business = yelp.business(business['id'])

    furby.say("You should check out %s, it is rated %d stars on Yelp." % (business['name'], int(business['rating'])))

def say_review():
    if "reviews" in current_business and current_business['reviews']:
        review = random.choice(current_business["reviews"])
        current_business['reviews'].remove(review)
        furby.say("%s said: %s" % (review["user"]["name"], review["excerpt"]))
    else:
        furby.say("No more reviews for %s. It must be terrible." % current_business['name'])

say_business()

while True:
    furby.say("Want to hear a review or should I find another business?")
    more = furby.listen_for(["more", "review", "else", "another", "business"], timeout=60)

    if "more" in more or "else" in more or "another" in more or "business" in more:
        say_business()
    elif "review" in more:
        say_review()
