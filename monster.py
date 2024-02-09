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

