from random import randint
from weapon import Weapon

class Player:
    def __init__(self, weapons: list[Weapon], name: str, player_class: str, is_npc: bool) -> None:
        self.__is_npc = is_npc
        self.__weapons = weapons
        self.__weapon = weapons[0]
        self.__name = name
        self.__level = 1

        match player_class.lower():
            case 'fighter':
                self.__health = 10
            case 'rogue':
                self.__health = 8
            case 'mage':
                self.__health = 6
            case 'barbarian':
                self.__health = 12
            case _:
                self.__health = 0
        self.__current_health = self.__health

    def attack(self, targets, target=None):
        damage = 0
        dice = self.__weapon.get('dice', '1d4').split('d') # type: ignore

        for _ in range(1, int(dice[0])):
            damage += randint(1, dice[1])

        damage += self.__weapon.get('modifier', 0) # type: ignore

        if self.__is_npc:
            target = targets[randint(0, len(targets))]
            target.take_damage(damage)
            return
        if target is None:
            return
        target.take_damage(damage)
        return
    
    def level_up(self):
        self.__level += 1
        self.__weapon = self.__weapons[self.__level-1]

    def take_damage(self, damage: int):
        self.__current_health -= damage
        # return if health is below / equals 0?

    def get_current_health(self):
        return self.__current_health
    
    def get_max_health(self):
        return self.__health
    
    def heal_to_full(self):
        self.__current_health = self.__health




