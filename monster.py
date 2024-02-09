from random import randint
from player import Player

class Monster:
    def __init__(self, name, hp, defense, weapon) -> None:
        self.__name = name
        self.__hp = hp
        self.__defense = defense
        self.__weapon = weapon.split(' ')[0]
        if len(self.__weapon.split("+")) > 1:
            self.__weapon_dice = self.__weapon.split("+")[0]
            self.__weapon_bonus = int(self.__weapon.split("+")[1])
        else:
            self.__weapon_dice = self.__weapon
            self.__weapon_bonus = 0


    def get_name(self):
        return self.__name

    def get_hp(self):
        return self.__hp

    def get_defense(self):
        return self.__defense
    
    def get_weapon(self):
        return self.__weapon
    

    def take_damage(self, damage: int):
        if (damage - self.__defense) <= 0:
            return
        self.__hp -= (damage - self.__defense)

    def attack(self, targets: list[Player]):
        damage = 0
        dice = self.__weapon_dice.split('d')

        for _ in range(1, int(dice[0])):
            damage += randint(1, int(dice[1]))

        damage += self.__weapon_bonus

        target = targets[randint(0, len(targets))]
        target.take_damage(damage)

