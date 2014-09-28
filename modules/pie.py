from furback import furby

ingredients = ["one nine inch pie crust",
               "eight granny smith apples",
               "three tablespoons all purpose flour",
               "one half cup packed brown sugar"]




if __name__ == "__main__":
    furby.say("to make this recipe you will need")
    for s in ingredients:
        furby.say(s)
        furby.wait(0.2)

    furby.listen_for(["what"], 30) 

    furby.say("Preheat oven to 425 degrees Farenheight. Melt the butter in a saucepan. Stir in flour to form a paste. Add water, white sugar and brown sugar, and bring to a boil. Reduce temperature and let simmer.")

    furby.listen_for(["what","then","next"], 30) 

    furby.say("Place the bottom crust in your pan. Fill with apples, mounded slightly. Cover with a lattice work crust. Gently pour the sugar and butter liquid over the crust. Pour slowly so that it does not run off.")        

    furby.listen_for(["what","then","next"], 30) 

    furby.say("Bake 15 minutes in the preheated oven. Reduce the temperature to 350 degrees Farenheight. Continue baking for 35 to 45 minutes, until apples are soft.")
    
    furby.listen_for(["thank"], 30)

    furby.do("burp")
    furby.wait(2.0)
    furby.do("food")
