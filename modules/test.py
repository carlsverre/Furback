from furback import furby

text = furby.get_input()

furby.say("ITS COMING")
furby.do("hypno")
furby.do("hypno")
furby.do("hypno")
furby.do("fart")

text = furby.listen_for(["hungry"], timeout=10)

furby.say("You said: %s" % text)
