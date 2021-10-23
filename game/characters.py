import random

default_characters = {
                   #HP  MP Att Def Sp target
    'knight':     [250, 0, 20, .5, 10, 10],
    'archer':     [200, 0, 14, .3, 15, 4],
    'thief':      [160, 0,  10, .2, 20, 3],
    'white mage': [110, 100, 3, .1, 5, 2],
    'black mage': [120, 140, 30, .1, 5, 3]
}

class Character:
    def __init__(self, name=None, hp=0, mp=0, attack=0, defense=0, speed=0, target=0, preset=None):
        if preset.lower() in default_characters:
            self._create_default_char(preset, name, hp, mp, attack, defense, speed, target)
        else:
            self.name = name
            self.hp = hp
            self.mp = mp
            self.attack = attack
            self.defense = defense
            self.speed = speed
            self.target = target # chance to get targeted

        self.hp_max = self.hp
        self.start_hp = self.hp
        self.mp_max = self.mp
        self.start_mp = self.mp
        self.lvl = 1
        self.exp = 0  # 130 exp until next level: 1.14%
        self.dead = False
        self.damage_lost = 0


    def _create_default_char(self, preset, name=None, hp=0, mp=0, attack=0, defense=0, speed=0, target=0):
        if name:
            self.name = name
        else:
            self.name = f"Unnamed {preset}"
        if hp:
            self.hp = hp
        else:
            self.hp = default_characters[preset][0]
        if mp:
            self.mp = mp
        else:
            self.mp = default_characters[preset][1]
        if attack:
            self.attack = attack
        else:
            self.attack = default_characters[preset][2]
        if defense:
            self.defense = defense
        else:
            self.defense = default_characters[preset][3]
        if speed:
            self.speed = speed
        else:
            self.speed = default_characters[preset][4]
        if target:
            self.target = target # chance to get targeted
        else:
            self.target = default_characters[preset][5]


    def add_exp(self, exp: int=0, set_level=None):
        prev_level = self.lvl

        self.exp += exp

        # Check what level the experience is at
        next = 100
        total = 0
        for lvl in range(1, 100):

            next = int(next * 1.14)
            # print(lvl, 'total experience:', total, 'For next level:', next)
            if self.exp >= total and self.exp < total + next:
                self.lvl = lvl

            # If setting to a specific level:
            if set_level:
                if lvl == set_level:
                    self.exp = total
                    self.lvl = lvl

            total += next

        # Check if gained any levels, and adjust stats
        levels = self.lvl - prev_level
        if levels:
            self._adjust_stats(self.lvl)


    def _adjust_stats(self, levels):
        self.hp_max = int(sum([(10 * (1.07 ** lvl)) for lvl in range(1, levels)]) + self.start_hp)
        self.hp = self.hp_max
        self.mp_max = int(sum([(5 * (1.01 ** lvl)) for lvl in range(1, levels)]) + self.start_mp)
        self.mp = self.mp_max


    def _print_stats(self):
        # Just for testing purposes
        print(self.name)
        print("Level: ", self.lvl)
        print("Exp: ", self.exp)
        print("HP: ", self.hp)
        print("MP: ", self.mp)
        print("Attack: ", self.attack)
        print("Defense: ", self.defense)
        print("Speed: ", self.speed)
        print("Target: ", self.target)



class Enemies:
    def __init__(self, type):
        if type == 'Goblin':
            self.name = 'Goblin'
            self.health = 30
            self.defense = .2
            self.attack = 7
            self.speed = 8
            self.target = 10

        if type == 'Goblin Mage':
            self.name = 'Goblin Mage'
            self.health = 50
            self.defense = .3
            self.attack = 12
            self.speed = 10
            self.target = 12

        if type == 'Ork':
            self.name = 'Ork'
            self.health = 50
            self.defense = .4
            self.attack = 15
            self.speed = 10
            self.target = 8

        if type == 'Slime':
            self.name = 'Slime'
            self.health = 17
            self.defense = .75
            self.attack = 6
            self.speed = 1
            self.target = 10

        if type == 'Goblin King':
            self.name = 'Goblin King'
            self.health = 100
            self.defense = .7
            self.attack = 30
            self.speed = 15
            self.target = 5

        if type == 'Slime King':
            self.name = 'Slime King'
            self.health = 350
            self.defense = .8
            self.attack = 35
            self.speed = 5
            self.target = 5


def enemy_group(group):
    # Added to list in order of speed
    if group == 'Group A':
        num = random.randint(2,5) # Slimes
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Slime'))
        return group_list

    if group == 'Group B':
        num = random.randint(2,4) # Goblins
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Goblin'))
        return group_list

    if group == 'Group C':
        num = random.randint(2,4) # Slimes
        num2 = random.randint(1,3) # Goblins
        group_list = []
        for _ in range(num2):
            group_list.append(Enemies('Goblin'))
        for _ in range(num):
            group_list.append(Enemies('Slime'))
        return group_list

    if group == 'Group D':
        num = random.randint(1,4) # Goblins
        num2 = random.randint(2,2) # Goblin Mage
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Goblin'))
        for _ in range(num2):
            group_list.append(Enemies('Goblin Mage'))
        return group_list

    if group == 'Group E':
        num = random.randint(2,4) # Ork
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Ork'))
        return group_list

    if group == 'Group F':
        num = random.randint(1,3) # Ork
        num2 = random.randint(0,2) # Goblin Mage
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Ork'))
        for _ in range(num2):
            group_list.append(Enemies('Goblin Mage'))
        return group_list

    if group == 'Group Goblin King':
        num = random.randint(2,2) # Goblin King
        num2 = random.randint(0,1) # Goblin
        group_list = []
        for _ in range(num):
            group_list.append(Enemies('Goblin King'))
        for _ in range(num2):
            group_list.append(Enemies('Goblin'))
        return group_list

    if group == 'Group Boss': # Slime King Boss + Slime
        num = random.randint(0,0)
        group_list = []
        group_list.append(Enemies('Slime King'))
        for _ in range(num):
            group_list.append(Enemies('Slime'))
        return group_list


# -----------------------------------------------------------
if __name__ == "__main__":
    arjen = Character(name="Arjen", preset='knight')
    arjen.add_exp(200)
    arjen._print_stats()
    arjen.add_exp(set_level=50)
    arjen._print_stats()
    arjen.add_exp(set_level=2)
    arjen._print_stats()




# end
