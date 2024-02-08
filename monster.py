class Monster:
    def __init__(self, name, hp, defense, weapon) -> None:
        self.__name = name
        self.__hp = hp
        self.__defense = defense
        self.__weapon = weapon

    def get_name(self):
        return self.__name

    def get_hp(self):
        return self.__hp

    def get_defense(self):
        return self.__defense
    
    def get_weapon(self):
        return self.__weapon

