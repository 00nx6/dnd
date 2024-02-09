from random import randint
from weapon import player_weapons
from typing import Any

# needed for rendering
def return_class_name_list():
    return list(player_weapons().keys())


def class_attributes(subclass):
    match subclass.lower():
        case 'fighter':
            health = 10
            defense = 2
        case 'rogue':
            health = 8
            defense = 1
        case 'mage':
            health = 6
            defense = 0
        case 'barbarian':
            health = 12
            defense = 0
        case _:
            return None, None

    return health, defense

# needed for rendering
def gen_lvl1_info(taken_class=''):
    lvl1_list = []
    for subclass in player_weapons():
        if taken_class and taken_class == subclass:
            continue
        
        health, defense = class_attributes(subclass)

        og_dct = player_weapons()[subclass]['level 1']
        og_dct.pop('name', 'modifier')
        
        og_dct.update(subclass=subclass, health=health, defense=defense) # type: ignore

        lvl1_list.append(og_dct)

    return lvl1_list

print(gen_lvl1_info('Fighter'))

class Player:
    def __init__(self, name: str, subclass: str) -> None:
        self.subclass = subclass
        self.name = name
        self.__level = 1
        self.health, self.defense = class_attributes(subclass)
        self.weapons, self.damage, self.modifier = player_weapons()[subclass]['level 1'].values()
        self.__current_health = self.health
        if name == subclass:
            self.is_npc = True

    def attack(self, targets, target=None):
        damage = 0
        dice = self.__weapon.get('dice', '1d4').split('d') # type: ignore

        for _ in range(1, int(dice[0])):
            damage += randint(1, int(dice[1]))

        damage += self.__weapon.get('modifier', 0) # type: ignore

        if self.is_npc:
            target = targets[randint(0, len(targets))]
            target.take_damage(damage)
            return
        if target is None:
            return
        target.take_damage(damage)
        return
    
    def level_up(self):
        self.__level += 1
        self.defense += 1

        match self.subclass.lower():
            case 'fighter':
                self.__health += 10
            case 'rogue':
                self.__health += 8
            case 'mage':
                self.__health += 6
            case 'barbarian':
                self.__health += 12
            case _:
                self.__health = 0
        
        weapon_string = f"level {self.__level}"
        self.weapon = self.weapons.get(weapon_string, 'level 1') # type: ignore

    def take_damage(self, damage: int):
        if (damage - self.defense) <= 0:
            return
        self.__current_health -= (damage - self.defense)
        # return if health is below / equals 0?
    
    def heal_to_full(self):
        self.__current_health = self.health

    def get_current_health(self):
        return self.__current_health
    
    def get_max_health(self):
        return self.health

    def get_name(self):
        return self.name



