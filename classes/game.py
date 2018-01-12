import random
from .magic import Spell
import pprint


class BackgroundColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items ):
        self.name = name
        self.maxHp = hp
        self.hp = hp
        self.maxMp = mp
        self.mp = mp
        self.atkHigh = atk + 10
        self.atkLow = atk - 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generateDamage(self):
        return random.randrange(self.atkLow, self.atkHigh)

    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxHp:
            self.hp = self.maxHp

    def getHp(self):
        return self.hp

    def getMaxHp(self):
        return self.maxHp

    def getMp(self):
        return self.mp

    def getMaxMp(self):
        return self.maxMp

    def reduceMp(self, cost):
        self.mp -= cost

    def chooseAction(self):
        i = 1
        print("\n" + BackgroundColors.BOLD + self.name + BackgroundColors.ENDC)
        print(BackgroundColors.OKBLUE + BackgroundColors.BOLD + "      ACTIONS" + BackgroundColors.ENDC)
        for item in self.actions:
            print("    ", str(i) + ":", item)
            i += 1

    def chooseMagic(self):
        i = 1
        print(BackgroundColors.OKBLUE + BackgroundColors.BOLD + "      MAGIC" + BackgroundColors.ENDC)
        for spell in self.magic:
            print("    ", str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def chooseItem(self):
        i = 1
        print(BackgroundColors.OKBLUE + BackgroundColors.BOLD + "      ITEMS:" + BackgroundColors.ENDC)
        for item in self.items:
            print("    ", str(i) + ".", item["item"].name, ":", item["item"].description,
                  "(x" + str(item["quantity"]) + ")")
            i += 1

    def chooseTarget(self, enemies):
        i = 1
        print("\n" + BackgroundColors.FAIL + BackgroundColors.BOLD + "     TARGET" + BackgroundColors.ENDC)
        for enemy in enemies:
            if enemy.getHp() != 0:
                print("     " + str(i) + ":" + enemy.name)
                i += 1
        choice = (int(input("Choose target:")) - 1)
        return choice

    def getEnemyStats(self):
        hpBar = ""
        barTicks = (self.hp / self.maxHp) * 100 / 2
        while barTicks > 0:
            hpBar += "█"
            barTicks -= 1
        while len(hpBar) < 50:
            hpBar += " "
        hpString = str(self.hp) + "/" + str(self.maxHp)
        currentHp = ""
        if len(hpString) < 11:
            decreased = 11 - len(hpString)
            while decreased > 0:
                currentHp += " "
                decreased -= 1
            currentHp += hpString
        else:
            currentHp = hpString
        print("                    ____________________________________________________")
        print(BackgroundColors.BOLD + self.name + "   " +
              currentHp + "|" + BackgroundColors.FAIL
              + hpBar + BackgroundColors.ENDC + "|")

    def getStats(self):

        #HP Bar
        hpBar = ""
        barTicks = (self.hp/self.maxHp) * 100 / 4
        while barTicks > 0 :
            hpBar += "█"
            barTicks -= 1
        while len(hpBar)  < 25:
            hpBar += " "

        #MP Bar
        mpBar = ""
        mpBarTicks = (self.mp / self.maxMp) * 100 / 10
        while mpBarTicks > 0:
            mpBar += "█"
            mpBarTicks -= 1
        while len(mpBar) < 10:
            mpBar += " "

        #White Space
        hpString = str(self.hp) + "/" + str(self.maxHp)
        currentHp = ""
        if len(hpString) < 9:
            decreased = 9 - len(hpString)
            while decreased > 0:
                currentHp += " "
                decreased -= 1
            currentHp += hpString
        else:
            currentHp = hpString
        mpString = str(self.mp) + "/" + str(self.maxMp)
        currentMp = ""
        if len(mpString) < 7:
            decreased = 7 - len(mpString)
            while decreased > 0:
                currentMp += " "
                decreased -= 1
            currentMp += mpString
        else:
            currentMp = mpString

        #HP/MP Bars
        print("                  ___________________________         ____________")
        print(BackgroundColors.BOLD + self.name + "   " +
              currentHp +  "|" + BackgroundColors.OKGREEN
              + hpBar + BackgroundColors.ENDC + "|  " + currentMp +  "|"
              + BackgroundColors.OKBLUE + mpBar + BackgroundColors.ENDC + "|")

    def chooseEnemySpell(self):
        magicChoice = random.randrange(0, len(self.magic))
        spell = self.magic[magicChoice]
        magicDmg = spell.generateDamage()
        pct = self.hp/self.maxHp* 100
        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.chooseEnemySpell()
        else:
            return spell, magicDmg

