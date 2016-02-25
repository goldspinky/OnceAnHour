import ctypes
import time
import random
import shelve
import dbhash
import os

starttime = time.time()

class Player(object):
    def __init__(self, experience, level, hours_run, profession, race, blue_coins, dungeon_progress, dungeon_string, ilvl, item_name, spells_unlearned, spells_learned, profession_parts, gold, ascendancy_counter, name):
        self.experience = experience
        self.level = level
        self.hours_run = hours_run
        self.profession = profession
        self.race = race
        self.blue_coins = blue_coins
        self.dungeon_progress = dungeon_progress
        self.dungeon_string = dungeon_string
        self.ilvl = ilvl
        self.item_name = item_name
        self.spells_unlearned = ['Eat Feast', 'LIGHTNING BOLT!', 'Saysay\'s Sight', 'Crown of Experience', 'Enchanted Hammer Strike']
        self.spells_learned = []
        self.profession_parts = profession_parts
        self.gold = gold
        self.ascendancy_counter = ascendancy_counter
        self.name = name

    def update(self, repeats=1): #gives the player experience, levels her up, and checks for additional functions (e.g., raiding at level 20)
        if repeats == 1:
            print("-----")
            self.time_printer() #make sure the player doesn't gain multiple hours/gain multiple time bonuses in a single update
            self.time_bonus()           
        while repeats > 0:
            repeats -= 1            
            self.pick_profession_race()
            self.daily_quest() #execute all other functions first so the player gets their real experience & level in the current update instead of the next cycle
            self.dungeon_dive()
            self.raid()
            self.learn_spell()
            self.cast_spell()
            self.gain_profession_parts()
            self.tithe()
            self.OAH_computing()
            if self.ascendancy_counter > 0:
                min_xp = (35.0/(self.ascendancy_counter**1.11))
                max_xp = (50.0/(self.ascendancy_counter**1.11))
            else:
                min_xp = 35
                max_xp = 50
        else:
            net_exp_gain = (random.uniform(min_xp, max_xp))*((self.blue_coins/100.0)+1.0)
            self.experience += net_exp_gain
            print("You are currently level " + str(self.level) + "." + " You are %.1f" % self.experience + "% towards your next level.")
            start_level = self.level
            while self.experience >= 100:
                self.level += 1
                self.experience -= 100
                if data.truncateLevelSpam == False:
                    print("Ding! You are now level " + str(self.level) + "!")
                elif self.experience < 100:
                    print("Ding! You were level " + str(start_level) + " and are now level " + str(self.level) + "!")

            self.ascend()

    def pick_profession_race(self):
        if self.profession == None:
            self.profession = random.choice(data.professionNames)
        if self.race == None:
            self.race = random.choice(data.raceNames)
            print("You are a " + self.race + " " + self.profession + ".") 

    def time_printer(self):
        self.hours_run += 1
        if self.hours_run == 2:
            print("Once An Hour has been running for " + str(self.hours_run-1) + " hour. <" + time.strftime("%Y-%m-%d %H:%M:%S") + ">")
        else:
            print ("Once An Hour has been running for " + str(self.hours_run-1) + " hours. <" + time.strftime("%Y-%m-%d %H:%M:%S") + ">")

    def time_bonus(self):
        if self.hours_run >= 24:
            if self.hours_run % (24*28) == 1:
                print("You earned a monthly reward! You get a satchel full of blue coins. You had %.1f" % (self.blue_coins) + " blue coins and you now have %.1f" % (self.blue_coins+(self.hours_run/1.5)) + ".")
                self.blue_coins += self.hours_run
            elif self.hours_run % (24*7) == 1:
                self.update(7)
                print("You earned a weekly reward! You get a potion of experience. You quaff the potion of experience. You feel enlightened!")
            elif self.hours_run % 24 == 1:
                self.update(3)
                print("You earned a daily reward! You get a lesser potion of experience. You quaff the lesser potion of experience. You feel enlightened!")

    def daily_quest(self):
        if random.randint(1, 2) == 2:
            daily_string = "You completed a daily quest: "
            daily_blue_coins = random.randint(1, 3+self.ascendancy_counter)
            if daily_blue_coins > 100:
                daily_blue_coins = 100
            self.blue_coins += daily_blue_coins
            quest_string = random.choice(data.dailyQuestChoices)
            if daily_blue_coins != 1:
                daily_string = daily_string + quest_string +  ". You got " + str(daily_blue_coins) + " blue coins! You are gaining %.1f" % ((self.blue_coins/1.0)+1.0) + "% bonus experience from blue coins."
            else:
                daily_string = daily_string + quest_string + ". You got a blue coin. You are gaining %.1f" % ((self.blue_coins/1.0)+1.0) + "% bonus experience from blue coins."
            print(daily_string)
            
    def dungeon_dive(self):
        if self.level >= 10:
            if self.dungeon_progress == 102:
                print("You queue for a random dungeon.")
                self.dungeon_progress = 101
            elif self.dungeon_progress == 101:
                if random.randint(1, 10) != 1:
                    self.dungeon_string = random.choice(data.dungeonChoices)
                    print("You join a group in " + self.dungeon_string + "!")
                    self.dungeon_progress = 100
                else:
                    print("The servers go down for maintenance and interrupt your queue.")
            elif self.dungeon_progress <= 100:
                self.dungeon_progress -= random.randint(20, 50)
                if self.dungeon_progress > 0:
                    print("You AFK in a corner while your group fights the boss of " + self.dungeon_string + ". The boss has " + str(self.dungeon_progress) + "% health left.")
                else:
                    if self.ascendancy_counter == 0:
                        dungeon_exp = ((random.uniform(75.0, 125.0)*((self.blue_coins/100.0)+1.0)))
                    else:
                        dungeon_exp = ((random.uniform(75.0, 125.0)*((self.blue_coins/100.0)+1.0)))/(self.ascendancy_counter**2)
                    self.dungeon_progress = 102
                    self.experience += dungeon_exp
                    print("Your group kills the boss of " + self.dungeon_string + " and then votes to kick you. You earned %.1f" % dungeon_exp  + "% experience.")

    def raid(self):
        if self.level >= 20:
            self.generate_item_name()
            ilvl_gain = random.randint(2, 6)
            self.ilvl += ilvl_gain
            if self.ilvl <= 69:
                print("You raid the Cave of Low Level Players with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 144:
                print("You raid the Dungeon of Dragon Cosplayers with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 305:
                print("You raid the Pit with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 404:
                print("You raid the Network Admin\'s Office with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 666:
                print("You raid the Hobbit Hole of Mayhem with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 1000:
                print("You raid The Raid of Raids with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 1337:
                print("You raid Ulduar with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 1666:
                print("You raid Dante\'s interpretation of the afterlife with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 2001:
                print("You raid the Y2K Bug\'s Lair with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 2222:
                print("You raid Highpass Held High Hold with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 2771:
                print("You raid N.W.A\'s Chevrolet with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 3333:
                print("You raid the Snake Pit with your crew. That\'s right, the Snake Pit. You gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 3454:
                print("You raid Highway 3 with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 4000:
                print("You raid A Location Not Owned By The Tolkein Estate with your crew and gain " + str(ilvl_gain) + " item levels!")
            elif self.ilvl <= 4679:
                print("You raid a random assortment of numbers and letters with your crew and gain " + str(ilvl_gain) + " item levels!")
            else:
                print("You raid LFR by yourself and gain " + str(ilvl_gain) + " item levels...")

            print("Your +" + str(self.ilvl-ilvl_gain) + " " + str(self.item_name) + " is now +" + str(self.ilvl) + ".")

    def generate_item_name(self):
        if data.forceItemName == "":
            if self.item_name == "":
                rand_title = random.choice(data.itemTitles)
                rand_element = random.choice(data.itemElements)
                rand_type = random.choice(data.itemTypes)
                rand_prefix = random.choice(data.itemPrefixes)
                rand_suffix = random.choice(data.itemSuffixes)
                full_item_name = rand_title + '\'s ' + rand_element + ' ' + rand_type + ' of the ' + rand_prefix + ' ' + rand_suffix
                self.item_name = full_item_name
        else:
            self.item_name = data.forceItemName

    def learn_spell(self):
        if self.level >= 30 and self.spells_unlearned:
            if random.randint(1,6) == 6:
                pick_me = random.choice(self.spells_unlearned)
                self.spells_unlearned.remove(pick_me)
                self.spells_learned.append(pick_me)
                print("You learned how to cast " + pick_me + "!")

    def cast_spell(self):
        if self.level >= 30 and self.spells_learned:
            if random.randint(1,3) == 3:
                pick_me = random.choice(self.spells_learned)
                if pick_me == "Eat Feast":
                    self.experience += random.randint(0, 150)
                    print("You cast Eat Feast. You feel full.")
                if pick_me == "LIGHTNING BOLT!":
                    self.experience += 15
                    print("LIGHTNING BOLT! LIGHTNING BOLT! LIGHTNING BOLT!")
                if pick_me == "Saysay\'s Sight":
                    self.level += 1
                    print("You peer into the past and return with a bucket full of knowledge. You are now level " + str(self.level) + ".")
                if pick_me == "Crown of Experience":
                    self.experience += 45
                    print("You cast Crown of Experience. A shimmering crown of gold appears on your head and then disappears in a flash of light.")
                if pick_me == "Enchanted Hammer Strike":
                    improve_ilvl = random.randint(1, 6)
                    improve_counter = 2
                    while improve_counter == 2:
                        improve_counter = random.randint(1, 2)
                        improve_ilvl += random.randint(1, 6)
                    else:
                        print("You roll up to the Mythic Forge with your Enchanted Hammer and Strike away, improving your item level from " + str(self.ilvl) + " to " + str(self.ilvl+improve_ilvl) + ".")
                        self.ilvl += improve_ilvl

    def gain_profession_parts(self): 
        if self.level >= 40:
            profession_check = data.professionNames.index(self.profession)
            profession_switch = data.professionMissions[profession_check]
            if random.randint(1, 6) == 6 and self.profession_parts < 277:
                print("<<<<<< PARTS >>>>>>: " + str(self.profession_parts))
                num_of_parts = random.randint(21, 45)
                self.profession_parts += num_of_parts
                if self.profession_parts < 277:
                    print("You collect " + str(num_of_parts) + " parts for your " + profession_switch + ". You need " + str(277-self.profession_parts) + " more.")
                else:
                    print("You\'ve collected enough parts to build your " + profession_switch + "!")
            elif self.profession_parts >= 277:
                exp_gained = random.randint(3, 12)
                ilvl_gained = random.randint(2, 6)
                self.experience += exp_gained
                self.ilvl += ilvl_gained
                print("You go on a mission with your " + profession_switch + " and return with " + str(exp_gained) + "% extra experience and " + str(ilvl_gained) + " extra item levels.")

    def tithe(self):
        if self.level >= 50:
            race_check = data.raceNames.index(self.race)
            race_switch = data.raceTemples[race_check]
            gold_gained = random.randint(11, 22)
            self.gold += gold_gained
            if self.gold < 222:
                print("Your people are constructing the " + race_switch + " in your honor! They\'ve recently raised " + str(gold_gained) + " gold for it and need " + str(222-self.gold) + " more.")
            elif self.gold < 722:
                print("Your people pay tithe at the " + race_switch + ". They\'ve recently donated " + str(gold_gained) + " gold and you have " + str(self.gold-222) + " banked.")
            elif self.gold >= 722:
                self.gold -= 500
                if random.randint(1, 2) == 1:
                    lvl_gained = self.ilvl//100
                    ilvl_gained = self.level*2
                    if self.ascendancy_counter == 0:
                        print("You take 500 gold and spend it on yoga practice, enhancing your mind, body, and soul. You gained " + str(lvl_gained) + " levels.")
                    else:
                        print("You take 500 gold and spend it on Jedi training, enhancing your mind, body, and soul. You gained " + str(lvl_gained) + " levels and " + str(ilvl_gained) + " item levels.")
                        self.ilvl += ilvl_gained
                    self.level += lvl_gained
                else:
                    spell_spam = random.randint(23, 46)
                    print("You take 500 gold and build a magical tower of awesomeness. It prompty explodes into a flurry of spells.")
                    while spell_spam > 0:
                        spell_spam -= 1
                        self.cast_spell()

    def OAH_computing(self):
        if data.OAHInput == 9801:
            if random.randint(1, 3) == 3:
                machine_random = random.randint(1, 3)
                if machine_random == 1:
                    self.blue_coins += 1
                    print("Your certified OAH Computer dispenses a tiny blue coin. Nice!")
                elif machine_random == 2:
                    self.experience += 25
                    print("Your certified OAH Computer dispenses some spicy calculus facts. Radical!")
                elif machine_random == 3:
                    self.ilvl += 2
                    print("Your certified OAH Computer dispenses a pamphlet on ancient blacksmithing. TIL!")

    def ascend(self):
        if pc.level >= (100 + (50*pc.ascendancy_counter)):
            print(">>>ASCENSION<<<")
            print("You feel profoundly tired. You wake up smelling like cheese dust and in the same place you were " + str(pc.hours_run) + " hours ago. All you have with you of your past life are %.1f" % pc.blue_coins + " blue coins.")
            print(">>>ASCENSION<<<")
            pc.experience = 0
            pc.level = 1
            pc.ilvl = 0
            pc.race = None
            pc.profession = None
            pc.gold = 0
            pc.profession_parts = 0
            pc.item_name = ""
            pc.dungeon_progress = 102
            pc.ascendancy_counter += 1

pc = Player(experience=0, level=1, hours_run=0, profession=None, race=None, blue_coins=0, dungeon_progress=102, dungeon_string="", ilvl=0, item_name="", spells_unlearned=0, spells_learned=0, profession_parts=0, gold=0, ascendancy_counter=0, name="YAK")

def importData(filename):
    import imp
    f = open(filename)
    global data
    data = imp.load_source("data", "", f)
    f.close()
    if data.widthX != 80 or data.heightY != 30:
        os.system("mode con: cols=" + str(data.widthX) + " lines=" + str(data.heightY))
    if pc.profession != None:
        print("You are a level " + str(pc.level) + " " + str(pc.race) + " " + str(pc.profession) + ". You have ascended " + str(pc.ascendancy_counter) + " time(s).")
        print("You are gaining %.1f " % ((pc.blue_coins/1.0)+1.0) + "% bonus experience from blue coins.")
    print("The game will update once every " + str(data.waitTimeInSeconds) + " seconds.")
    print("On update, the game will display a popup message with the text '" + str(data.popUpMessage) + "'.")
    if data.popUpEnabled == True:
        print("On update, the game will create a popup.")
    else:
        print("On update, the game will not create a popup.")
    if data.simulateHours < pc.hours_run:
        print("The game is not simulating any extra hours of playtime.")
    else:
        print("The game is simulating up to " + str(data.simulateHours) + " hours worth of play.")
    if data.forceItemName != "":
        print("The game is forcing the item name to be " + str(data.forceItemName) + ".")
    if int(data.OAHInput) == 9801:
        print("Your certified OAH Computer prints out a smiley face.")
    elif int(data.OAHInput) == 970299:
        print("Your certified OAH Computer prints out a confused face.")
    elif int(data.OAHInput) == 99:
        print("Your certified OAH Computer prints out a scared face.")
    elif int(data.OAHInput) != 0:
        print("Your certified OAH Computer prints out a sad face.")
    elif int(data.OAHInput) == 0:
        print("Your certified OAH Computer dispenses an OAH Computer Manual: input integers into your OAH Computer in config.txt.")

def save_meta():
    file = shelve.open('meta', 'c')
    file['pc'] = pc
    file.close()

def load_meta():
    global pc
    file = shelve.open('meta', 'c')
    pc = file['pc']
    pc.hours_run -= 1
    if pc.experience >= 35:
        pc.experience -= 35
    if pc.ilvl >= 6:
        pc.ilvl -= 2
    file.close()

try:
    load_meta()
except KeyError:
    print("No saved data available...")

importData("config.txt")

def simulateHours(num):
    if num > pc.hours_run:
        difference = num - pc.hours_run
        og_difference = difference
        while difference > 0:
            difference -= 1
            pc.update()
        else:
            print("Finished simulating playtime. Successfully simulated " + str(og_difference) + " hours of data.")
            save_meta()

def go_machine():
    if int(data.OAHInput) != 9801:
        if random.randint(1, 3) == 3:
            random_code = random.randint(1, 3) #abyq
            if random_code == 1:
                print("Your certified OAH Computer prints out a punch card: OAH106: GOT 99 PROBLEMS")
            elif random_code == 2:
                print("Your certified OAH Computer prints out a punch card: OAH212: IF PROBLEMS SQUARED AWAY")
            elif random_code == 3:
                print("Your certified OAH Computer prints out a punch card: OAH318: AIN\'T GOT NO PROBLEMS NO MORE")

while True:
    if data.popUpEnabled:
        ctypes.windll.user32.MessageBoxA(0, data.popUpMessage, "Once An Hour...", 0)
    if data.simulateHours > 0:
        simulateHours(data.simulateHours)
    pc.update()
    go_machine()
    save_meta()
    time.sleep(data.waitTimeInSeconds - ((time.time() - starttime) % data.waitTimeInSeconds))
