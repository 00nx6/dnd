from random import randint

class Player:
    def __init__(self, weapons, name: str, player_class: str, is_npc: bool) -> None:
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

    def attack(self, targets, target=None):
        damage = 0
        dice = self.__weapon.get('dice', '1d4').split('d')

        for _ in range(1, int(dice[0])):
            damage += randint(1, dice[1])

        damage += self.__weapon.get('modifier', 0)

        if self.__is_npc:
            target = targets[randint(0, len(targets))]
            target.take_damage(damage)
            return
        if target is None:
            return
        target.take_damage(damage)
        return
    
    def level_up(self):
        self.__weapon = self.__weapons[self.__level-1]
