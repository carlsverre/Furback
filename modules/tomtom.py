from furback import furby

directions_starbucks = ["Head west in 24th Street towards York Street",
                        "Then turn right on Bryant Street",
                        "Then turn left onto mariposa street",
                        "The starbucks is on your left",
                        "But Phillz is better"]

directions_phillz = ["Head west in 24th Street towards York Street",
                     "The Phillz is on your left",
                     "Can you get me a dancing waters?"]
def SayDirections(dirs):
    for s in dirs[:-1]:
        furby.say(s)
        furby.wait(0.5000)
    furby.wait(0.5000) # wait longer before the joke at the end
    furby.say(dirs[-1])

def Handle(query):
    if "starbucks" in query:
        SayDirections(directions_starbucks)
    elif if "phil" in query or "fil" in query:
        SayDirections(directions_phillz)
        furby.do("fart")
        

if __name__ == "__main__":
    query = furby.get_input()
    Handle(query)
