from random import randint

class Player:
    def __init__(self):
        self.name = 'Lajos'
        self.subclass = 'Archer'
        self.damage = '1d6+2'
        self.defense = '4'

class Enemy:
    def __init__(self):
        self.name = 'Goblin'
        self.subclass = 'Archer'
        self.damage = '1d6+2'
        self.defense = '4'

player = Player()
enemies = [Enemy() for _ in range(4)]

def damage_calc(player):
    dice_roll, base = player.damage.split('+')
    no_rolls, sided_dice = dice_roll.split('d')
    damage = 0
    for _ in range(int(no_rolls)):
        damage += randint(1, int(*sided_dice))
        damage += int(base)
    return damage


