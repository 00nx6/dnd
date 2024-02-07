import random
import pickle
import os

INITIAL_HEALTH = 100
# [(noun, strength, reliability, weight,)...]
NOUNS = [('sword', 4, 8, 5), ('shield', 1, 8, 8), ('bow', 8, 2, 3), ('canon', 9, 2, 15), ('force field', 2, 7, 1), ('drone', 9, 2, 20), ('tank', 9, 7, 45)]
# [(adjective, multiplier,)...]
ADJECTIVES = [('wooden', 1), ('bronze', 2), ('steel', 3), ('diamond', 4), ('nanofiber', 5), ('unobtainium', 6), ('epic', 7), ('legendary', 8), ('eternal', 9)]


def ask_choice(prompt, choices):
    """Asks the user to choose one of the provided choices.

    Parameters
    ----------
    prompt: str
        The question to ask the user.
    choices: list or set
        The options the user can choose from. Each choice can be a string, or any other type
        as long as it can be converted to a string (using an `__str__` method).

    Returns
    -------
    The selected item out of choices.
    """
    choices = list(choices) # in case choices is a set, we want to convert it to a list
    if len(choices) == 0:
        raise ValueError("No options")
    while True:
        print(prompt)
        for index, choice in enumerate(choices):
            print(f"  {index+1}. {str(choice).capitalize()}")
        index = ask_int("> ") - 1
        if 0 <= index < len(choices):
            return choices[index]
        print("Invalid input, try again\n")

def ask_int(prompt="", min_value=None, max_value=None):
    """Like `input()`, but keeps repeating the question until the user enters a non-negative integer,
    that lies between the given boundaries.

    Parameters
    ----------
    prompt: str
        The question to ask the user.
    min_value: int or None
        An optional minimum allowed value (inclusive).
    max_value: int or None
        An optional maximum allowed value (inclusive).

    Returns
    -------
    int
        The value entered by the user.
    """
    while True:
        result = input(prompt)
        if result.isdigit():
            result = int(result)
            if (min_value is None or result >= min_value) and (max_value is None or result <= max_value):
                return result
        print("Invalid input, try again\n")


class Game:
    def __init__(self):
        """The constructor. It asks the user how many players should participate,
        creates objects for each, and stores them in a list in the `players`
        attribute."""
        try:
            with open('game_state.pickle', 'rb') as game_file:
                loaded_game = pickle.load(game_file)
                self.__dict__.update(loaded_game.__dict__)
        except (FileNotFoundError, pickle.UnpicklingError):
            self.__players = [Player() for _ in range(ask_int("How many players? ", 2, 6))]
            self.turn = 0


    def run(self):
        """Runs the actual game until someone wins."""
        while not self.declare_winner():
            player = self.__players[self.turn % len(self.__players)]
            if not player.is_dead(): # Skip dead players
                self.print_players(player)
                player.play_turn(self) # Pass a reference to this `Game` object
            self.turn += 1
            with open('game_state.pickle', 'wb') as game_file:
                pickle.dump(self, game_file)

    def print_players(self, current_player):
        """Prints all players (using the `Player.__str__` method), marking the current
        player with an arrow."""
        print()
        for player in self.__players:
            print(f'{"->" if player == current_player else "  "} {player}')
        print()

    def declare_winner(self) -> bool:
        """Checks if there's only one player left alive, and if so, prints a message declaring
        him/her the winner.

        Returns
        -------
        bool
            True when there's a winner, False if not.
        """
        alive_players = [player for player in self.__players if not player.is_dead()]

        if len(alive_players) == 1:
            print(f"{alive_players[0].get_name()} is the winner!")
            os.remove('game_state.pickle')
            return True
        return False
    
    def get_players(self):
        return self.__players


class Player:
    def __init__(self):
        self.__name = input("what is your name? ")
        self.__hp = INITIAL_HEALTH
        self.__weapons = []

    def play_turn(self, game: Game):

        if len(self.__weapons) > 0:
            options = ['heal', 'attack', 'find weapon', 'upgrade']
        else:
            options = ['heal', 'find weapon']
        action = ask_choice(f"{self.__name}, what will you do?", options)

        match action:
            case "heal":
                self.__heal()
            case "attack":
                self.__attack(game.get_players())
            case "find weapon":
                new_weapon = Weapon()
                self.__weapons.append(new_weapon)
                print(f"You have found a new weapon: {new_weapon}")
            case "upgrade":
                weapon = ask_choice("Which weapon would you like to upgrade?", self.__weapons)
                weapon.upgrade()
            case _:
                pass

        while self.get_weapon_weight() > 50:
            weapon = ask_choice("You are too heavy, which weapon would you like to drop?", self.__weapons)
            self.__weapons.remove(weapon)

    def __heal(self):
        self.__hp += max((INITIAL_HEALTH - self.__hp) // 2, 5)
        print(f"{self.__name} is starting to feel better: {self.__hp} hp")

    def is_dead(self):
        return self.__hp <= 0
    
    def sustain_damage(self, damage: int):
        self.__hp = max(self.__hp - damage, 0)
        if self.is_dead():
            print(f"{self.__name} died.")
        print(f"{self.__name} suffered {damage} damage.")

    def __str__(self):
        if self.is_dead():
            return f"{self.__name} (DEAD)"
        return f"{self.__name} ({self.__hp} hp, {self.get_weapon_count()} weapons, {self.get_weapon_weight()} kg)"

    def __attack(self, game_players):
        attack_options = [player for player in game_players if not player.is_dead() and player != self]
        target = ask_choice(f"{self.__name}, which player would you like to attack?", attack_options)
        weapon = ask_choice("With which weapon would you like to attack?", self.__weapons)
        target.sustain_damage(weapon.get_damage())

    def get_name(self):
        return self.__name
    
    def get_weapon_count(self):
        return len(self.__weapons)
    
    def get_weapon_weight(self):
        total_weight = 0
        for weapon in self.__weapons:
            total_weight += weapon.get_weight()
        return total_weight
    
class Weapon:

    def __init__(self):
        self.__noun, self.__strength, self.__reliability, self.__weight = random.choice(NOUNS)
        adjective, multiplier = random.choice(ADJECTIVES)
        self.__strength = round(self.__strength * multiplier / 5) # Apply the multiplier to strength
        self.__name = f"{adjective} {self.__noun}".title()
        
    def get_damage(self):
        if self.__reliability <= 0:
            return 1
        self.__reliability -= 1
        return self.__strength

    def __str__(self) -> str:
        if self.__reliability <= 0:
            return f"{self.__name} (BROKEN)"
        return f"{self.__name} ({self.__strength} strength, {self.__reliability} reliability, {self.__weight} kg)"
    
    def upgrade(self):
        upgrade_options = 1 if self.__reliability <= 0 else random.randint(1, 2)
        if upgrade_options == 1:
            self.__reliability += random.randint(1, 15)
        else:
            self.__strength += random.randint(1, 15)

        self.__weight += random.randint(1, 5)

    def get_weight(self):
        return self.__weight

if __name__ == "__main__":
    Game().run()
