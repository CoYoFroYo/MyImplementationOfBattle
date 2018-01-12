from classes.game import Person, BackgroundColors
from classes.magic import Spell
from classes.inventory import Item
import random

#Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

#Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

#Create some items
potion = Item("Potion", "potion", "Heals 50 HP",  50)
hiPotion = Item("Hi-Potion", "potion", "Heals 100 HP",  100)
superPotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaElixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

#Instantiate People
playerSpells = [fire, thunder, blizzard, meteor, quake, cure, cura]
playerItems = [{"item": potion, "quantity": 15}, {"item": hiPotion, "quantity": 5},
               {"item": superPotion, "quantity": 5}, {"item": elixir, "quantity": 5},
               {"item": megaElixir, "quantity": 2}, {"item": grenade, "quantity": 5}]
player = Person("Valos:", 3260, 132, 300 , 34, playerSpells, playerItems)
player2 = Person("Cody :", 4160, 188, 311 , 34, playerSpells, playerItems)
player3 = Person("Robot:", 3089, 174, 288 , 34, playerSpells, playerItems)
players = [player, player2, player3]

enemySpells = [fire, meteor, cure]
enemy = Person("Imp  ", 1250, 130, 560, 325, enemySpells, [])
enemy2 = Person("Magus", 18200, 223, 525, 25, enemySpells, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, enemySpells, [])
enemies = [enemy, enemy2, enemy3]


running = True

print(BackgroundColors.FAIL + BackgroundColors.BOLD + "ENEMIES ATTACK!" + BackgroundColors.ENDC )
while running:
    print("============================")
    print("\n")
    print("NAME      HP                 MP")
    for player in players:
        player.getStats()
    print("\n")
    for enemy in enemies:
        enemy.getEnemyStats()
    for player in players:
        player.chooseAction()
        index = int(input("Choose action:")) - 1

        #Chose Attack
        if index == 0:
            dmg = player.generateDamage()
            enemy = player.chooseTarget(enemies)
            enemies[enemy].takeDamage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage. Enemy HP:",
                  enemies[enemy].getHp())
            if enemies[enemy].getHp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has been defeated.")
                del enemies[enemy]

        #Chose Magic
        elif index == 1:
            player.chooseMagic()
            magicChoice = int(input("Choose magic:")) - 1
            if magicChoice == -1:
                continue
            spell = player.magic[magicChoice]
            magicDmg = spell.generateDamage()
            currentMp = player.getMp()
            if spell.cost > currentMp:
                print(BackgroundColors.FAIL + "\nNot enough MP\n" + BackgroundColors.ENDC)
                continue
            player.reduceMp(spell.cost)
            if spell.type == "white":
                player.heal(magicDmg)
                print(BackgroundColors.OKGREEN + "\n" + spell.name + " heals for", str(magicDmg),
                      "HP.", BackgroundColors.ENDC)
            elif spell.type == "black":
                enemy = player.chooseTarget(enemies)
                enemies[enemy].takeDamage(magicDmg)
                print(BackgroundColors.OKBLUE + "\n" + spell.name + " deals",
                      str(magicDmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + BackgroundColors.ENDC)
                if enemies[enemy].getHp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has been defeated.")
                    del enemies[enemy]

        #Chose item
        elif index == 2:
            player.chooseItem()
            itemChoice = int(input("Choose item:")) - 1
            if player.items[itemChoice]["quantity"] == 0:
                print(BackgroundColors.FAIL + "\n" + "None left..." + BackgroundColors.ENDC)
                continue
            player.items[itemChoice]["quantity"] -= 1
            if itemChoice == -1:
                continue
            item = player.items[itemChoice]["item"]
            if item.type == "potion":
                player.heal(item.prop)
                print(BackgroundColors.OKGREEN + "\n" + item.name + " heals for", str(item.prop),
                      "HP.", BackgroundColors.ENDC)
            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in player:
                        i.hp = player.maxHp
                        i.mp = player.maxMp
                else:
                    player.hp = player.maxHp
                    player.mp = player.maxMp
                print(BackgroundColors.OKGREEN + "\n" + item.name + " fully restores HP/MP", BackgroundColors.ENDC)
            elif item.type == "attack":
                enemy = player.chooseTarget(enemies)
                enemies[enemy].takeDamage(item.prop)
                print(BackgroundColors.FAIL + "\n" + item.name +
                      " deals", str(item.prop), "points of damage to"+ enemies[enemy].name.replace(" ", "")
                      + BackgroundColors.ENDC)
                if enemies[enemy].getHp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has been defeated.")
                    del enemies[enemy]
    # Turn Stats
    defeatedEnemies = 0
    for enemy in enemies:
        if enemy.getHp() == 0:
            defeatedEnemies += 1
        if defeatedEnemies == 2:
            print(BackgroundColors.OKGREEN + "You win!" + BackgroundColors.ENDC)
            running = False
        defeatedPlayers = 0
        for player in players:
            if player.getHp() == 0:
                defeatedPlayers += 1
        if defeatedPlayers == 2:
            print(BackgroundColors.FAIL + "Your enemies have defeated you!" + BackgroundColors.ENDC)
            running = False

    #Enemy's Turn
    for enemy in enemies:
        enemyChoice = random.randrange(0, 2)
        if enemyChoice == 0:
            target = random.randrange(0, 3)
            enemyDmg = enemy.generateDamage()
            players[target].takeDamage(enemyDmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "")
                  + " for " + str(enemyDmg))
        elif enemyChoice == 1:
            spell, magicDmg = enemy.chooseEnemySpell()
            enemy.reduceMp(spell.cost)
            if spell.type == "white":
                enemy.heal(magicDmg)
                print(BackgroundColors.OKGREEN + "\n" + spell.name + " heals " + enemy.name + " for", str(magicDmg),
                      "HP.", BackgroundColors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].takeDamage(magicDmg)
                print(enemy.name.replace(" ", ""), "'s " + spell.name, "deals", str(magicDmg) + " to "
                      + players[target].name.replace(" ", ""))
                if players[target].getHp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[player]



