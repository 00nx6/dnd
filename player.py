from random import randint
from weapon import player_weapons
        
class Player:
    def __init__(self, weapons, name: str, subclass: str, is_npc: bool) -> None:
        self.__is_npc = is_npc
        self.__weapons = weapons
        self.__class = subclass
        # placeholder
        self.weapon, self.damage, self.modifier = player_weapons()[subclass]['level 1'].values()
        
        # self.__weapon = weapons[0]
        self.name = name
        self.__level = 1

        match subclass.lower():
            case 'fighter':
                self.health = 10
                self.defense = 2
            case 'rogue':
                self.health = 8
                self.defense = 1
            case 'mage':
                self.health = 6
                self.defense = 0
            case 'barbarian':
                self.health = 12
                self.defense = 0
            case _:
                self.health = 0
                self.defense = 0

        self.current_health = self.health

    def __str__(self):
        return f'{self.__weapons}'


    def attack(self, targets, target=None):
        """_summary_

        Args:
            targets (list): List of monsters in combat
            target (object, optional): Attack aimed at by the user. Defaults to None.
        """
        damage = 0
        dice = self.__weapon.get('dice', '1d4').split('d') # type: ignore

        for _ in range(1, int(dice[0])):
            damage += randint(1, int(dice[1]))

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
        self.defense += 1

        match self.__class.lower():
            case 'fighter':
                self.health += 10
            case 'rogue':
                self.health += 8
            case 'mage':
                self.health += 6
            case 'barbarian':
                self.health += 12
            case _:
                self.health = 0
        
        weapon_string = f"level {self.__level}"
        self.__weapon = self.__weapons.get(weapon_string, 'level 1') # type: ignore

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
        return self.__name

