from random import randint, choice
import pickle as pickle_rick
INITIAL_HEALTH = 100

def ask_choice(prompt, choices):
    """ask_choice

    Args:
        prompt (text): Text displayed to the user
        choices (list): choices presented to the user

    Raises:
        ValueError: Raised when no options are given

    Returns:
        list item: chosen item from choices
    """
    choices = list(choices)
    if len(choices) == 0:
        raise ValueError("No options")
    while True:
        print(prompt)
        for index, _choice in enumerate(choices):
            print(f"  {index+1}. {str(_choice).capitalize()}")
        index = ask_int("> ") - 1
        if 0 <= index < len(choices):
            return choices[index]

def ask_int(prompt="", min_value=None, max_value=None):
    """_summary_

    Args:
        prompt (str, optional): what ever is displayed next to used input eg. ' > ' in ask_choice. Defaults to "".
        min_value (int, optional): Minimum value for accepted input. Defaults to None.
        max_value (int, optional): maximum value for accepted input. Defaults to None.

    Returns:
        int: user input
    """
    while True:
        result = input(prompt)
        if result.isdigit():
            result = int(result)
            if (min_value is None or result >= min_value) and (max_value is None or result <= max_value):
                return result


class Game:
    def __init__(self):
        count = ask_int("How many players? ", 2, 6)
        self.__players = [Player(num) for num in range(count)]

    def run(self):
        # Main game loop
        turn = 0
        while not self.declare_winner(): # While theres no winner
            player = self.__players[turn % len(self.__players)]
            if not player.is_dead(): # Skip dead players
                self.print_players(player)
                player.play_turn(self) # Pass a reference to this `Game` object
            pickle_my_game_state(self)
            turn += 1
            
    def print_players(self, current_player):
        print()
        for player in self.__players:
            print(f'{"->" if player == current_player else "  "} {player}')
        print()

    def declare_winner(self):
        players = [player for player in self.__players if not player.is_dead()]
        if len(players) == 1:
            print(f'{players[0]} has won the game.')
            return True
        return False
    
    def get_target(self, target):
        # next just returns first item if no other arguments are given, same as [0]
        return next(player for player in self.__players if target == player)
    
    def players(self, current):
        return [player for player in self.__players if player != current and not player.is_dead()]

    
class Player:
    def __init__(self, num) -> None:
        self.__hp = INITIAL_HEALTH
        self.__name = input(f'Enter name for player {num + 1}: ')
        self.__weapons = []
        
    def __str__(self) -> str:
        if self.__hp > 0:
            return f'{self.__name} ({self.__hp} HP, {self.get_weapon_count()} weapons, {self.get_weapon_weight()} KG)'
        
        return f'{self.__name}'

    def get_weapon_count(self) -> int:
        return len(self.__weapons)
    
    def get_weapon_weight(self) -> int:
        weight = 0
        for weapon in self.__weapons:
            weight += weapon.get_weight()
        return weight

    def weapon_upgrade(self) -> None:
        if len(self.__weapons) > 1:
            chosen_weapon = ask_choice(prompt='Which weapon do you want to upgrade?',
                                        choices=self.__weapons)
            chosen_weapon.upgrade()
        else:
            self.__weapons[0].upgrade()
        
    def is_dead(self) -> bool:
        return self.__hp <= 0

    def heal(self) -> None:
        # calculates hp_heal as half of the difference between initial health and current hp
        # if hp_heal is below 5, 5 is defaulted to.
        hp_heal = int(max((INITIAL_HEALTH - self.__hp) / 2, 5))
        if self.__hp < 30:
            print(f'{self.__name} is returning from the brink of death.')
        elif self.__hp < 70:
            print(f'{self.__name} is starting to feel better.')
        else:
            print(f'{self.__name} is feeling great.')
        
        print(f'{self.__name} healed for {hp_heal} to {hp_heal + self.__hp}')
        self.__hp += hp_heal
        
    def attack(self, game) -> None:
        """
        Args:
            game (obj): current game instance
        """
        target_selection = ask_choice(prompt='Which player would do you want to attack?',
                                    choices=game.players(self))
        if len(self.__weapons) > 1:
            attack_weapon = ask_choice(prompt='Which weapon do you to use?',
                                        choices=[weapon for weapon in self.__weapons if not weapon.is_broken()])
        else:
            attack_weapon = self.__weapons[0]
        
        target = game.get_target(target_selection)
        target.sustain_damage(damage=attack_weapon.get_damage())
    
    def sustain_damage(self, damage):
        """
        Args:
            damage (int): Number to be deducted from player's health
        """
        self.__hp -= damage
        
        print(f'{self.__name} was attacked for {damage} point(s) damage.')
        if self.is_dead():
            print(self, 'has perished')

    def play_turn(self, game):
        """
        Args:
            game (obj): Current game instance
        """

        choices = [
            'Attack',
            'Heal',
            'Find weapon',
            'Upgrade weapon'
        ]
        # if player has no weapons options needing a weapon are disabled
        if not self.__weapons:
            choices.pop(choices.index('Attack'))
            choices.pop(choices.index('Upgrade weapon'))
        
        choice = ask_choice(prompt=f'{self.__name}, What will you do?', choices=choices)
        
        match choice.lower():
            case 'heal':
                self.heal()
            case 'attack':
                self.attack(game)
            case 'find weapon':
                self.__weapons.append(Weapon())
                print(f'{self.__name} found:', self.__weapons[-1])
            case 'upgrade weapon':
                self.weapon_upgrade()
            case _:
                pass
        
        while self.get_weapon_weight() > 50:
            self.force_drop()
            
        self.weapon_status()
    
    def weapon_status(self):
        for weapon in self.__weapons:
            if weapon.is_broken():
                print(weapon, f'It\'s now junk and {self.__name} dropped it.')
                self.__weapons.pop(self.__weapons.index(weapon))
    
    def force_drop(self):
        print('You are carrying too many weapons, and have exceeded 50KGs of weight.')
        print('-------------')
        _choice = ask_choice(prompt='Select which weapons to drop.',
                             choices=self.__weapons)
        
        self.__weapons.pop(self.__weapons.index(_choice))
        print('-------------')
        print(_choice, 'Was dropped.')
        
        
class Weapon:
    def __init__(self):
        # [(noun, strength, reliability, weight)...]
        self.__weapon_types = [
            ('sword', 4, 8, 5),
            ('shield', 1, 8, 8),
            ('bow', 8, 2, 3),
            ('canon', 9, 2, 15),
            ('force field', 2, 7, 1),
            ('drone', 9, 2, 20),
            ('tank', 9, 7, 45)
        ]
        
        # [(adjective, multiplier)...]
        self.__modifiers = [
                ('wooden', 1),
                ('bronze', 2),
                ('steel', 3),
                ('diamond', 4),
                ('nanofiber', 5),
                ('unobtainium', 6),
                ('epic', 7),
                ('legendary', 8),
                ('eternal', 9)
            ]
        
        # choice is random.choice
        self.__weapon_type, self.__strength, self.__reliability, self.__weight = choice(self.__weapon_types)
        self.__weapon_modifier, self.__multiplier = choice(self.__modifiers)
        
    def __str__(self) -> str:
        if not self.is_broken():
            return f'\n{self.__weapon_modifier.upper()} {self.__weapon_type.upper()}\nStrength: {self.__strength}\nWeight: {self.__weight}\nReliability: {self.__reliability}'
        return f'{self.__weapon_modifier.upper()} {self.__weapon_type.upper()} (BROKEN)'
    
    def upgrade(self) -> None:
        # basic variable, underscore to not redefine imported function
        _choice = choice([self.__reliability, self.__strength])
        _choice += randint(0, 15)

        self.__weight += randint(0, 5)
        print(self)
    
    def get_damage(self) -> int:
        strength = round(self.__strength * self.__multiplier / 5)
        # if the weapons durability is above 0 itll get a random multiplier in the range of 1 to durability
        # else defaults to 0 because weapon is broken
        damage = strength * randint(1, self.__reliability) if self.__reliability else 0
        
        self.decrement()
        return damage
    
    def is_broken(self) -> bool:
        return self.__reliability == 0
    
    def decrement(self) -> None:
        self.__reliability -= 1

    def get_weight(self) -> int:
        return self.__weight

def pickle_my_game_state(game):
    pickled_rick = pickle_rick.dumps(game)
    with open('file', 'ab') as file:
        pickle_rick.dump(pickled_rick, file)
    
def unpickle_my_game_state():
    with open('file', 'rb') as file:
        pickled_game = pickle_rick.load(file)
    return pickle_rick.loads(pickled_game)

def main():
    try:
        game = unpickle_my_game_state()
        if not game:
            raise ValueError()
    except ValueError:
        game = Game()

    game.run()
    
if __name__ == '__main__':
    main()
