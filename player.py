# imports here


class Player:
    def __init__(self, weapon, name: str, player_class: str, is_npc: bool) -> None:
        self.__is_npc = is_npc
        self.__weapon = weapon
        self.__name = name
        match player_class:
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

    def attack(self):
        if self.__is_npc:
            return 'attack automatically'
        return 'attack after choice'

