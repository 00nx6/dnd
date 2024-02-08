from random import randint


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
    while True:
        print(prompt)
        if not len(choices):
            print("  No options.")
            return None
        for index, choice in enumerate(choices):
            print(f"  {index+1}. {str(choice).capitalize()}")
        index = ask_int("> ") - 1
        if 0 <= index < len(choices):
            return choices[index]

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
        target.take_damage(damage)
        return
    
    def level_up(self):
        self.__weapon = self.__weapons[self.__level-1]
