# D&D

## TODO:
 - Make the prompt
   - return correct format
   - understand setting/classes
   - make monsters, quests, items,

    
 - Class for interpreting API responses 
     - Class for managing the level that were in -
     - Class for managing monsters - Sem
     - Class to manage quests
     - When defeating an enemy:
        - Upgrade weapon
     - Level up
        - 1: 1
        - 2: 2
        - 3: 4
        - 4: 8
     - Capped kill requirements at:
        - 5: 10

- Rework player for classes and character customisation levels and upgradable inventory
  
- NPC players, sub classes - Sem
- Setup starting Classes
    - Fighet
    - Mage
    - Barbarian
    - Rogue

## Bonus things for quality of life:
- Type of damange ?
- Crits/Faliure
- Perks?
 - resistances
 - skills


## Pseudo code
### On startup:
the user is asked to pick a class, given a showing of their stats and starting weapons. It is explained that the classes not picked will be given as team mates.

the user is asked to enter a short prompt for the story scenario, or leave blank for gpt to freestyle.

the prompt as `system` is sent to the openAi API.

The prompt specifies:
   - what kind of weapons are in the game
   - what the current level of the part is
   - what kind of story it should generate
   - return the same dict as fed but properly populated
   - there is 1 player and 3 mute companion npcs
      - cannot be interacted with
   - try to steer the situation towards combat
   - feel free to add other stuff to make it more interesting if you have time
      
Once the response is received the main title is displayed
and the displayed story gets updated.

the response contains `actions`, each action will be rendered as a button under the story

if the dict contains `enemies`, a class called `Combat` will take effect where we do turn based attacks against the monster.
<!-- 
   maybe remove friendly npcs? we want to focus more on the combat and exploration aka. `the fun bits` 
-->
if the dict contains `friendly_npcs` their interactivity options get presented under the main story

if the dict contains `interact` items they should be presented as options to interact with
- display them as prompts for the user to interact with under the main story.
when selected, it will return a pre-written prompt for the bot
   e.g:
      - `The player pulled the lever on the wall.`
      - `The player opened the chest and found an item.`

continue game loop
   
### Combat:
Combat is a class that takes the enemies from the dict and the player
with his companions and pauses the story. (meaning no more calls until the battle is decided)

Enemies will be stored in the combat instance.

damage is given as `1d6 + 2` translating to 1 dice roll of a 6 sided dice + 2 as a base damage. 

If damage done doesn't exceed def then attack will miss.
 - there is a chance for the attack to completely miss.
 - there is a chance for the attack to register as a crit (2x damage).

This is for Sem to figure out how to make fair.

Having 3 comrades, they will also each attempt an attack with the same rules.

Upon victory or enemy slain a weapon upgrade is made.

displays a cool picture, ripped straight off google search.

__weapon__:
Contains weapon 
   - name 
   - durability
   - damage formulae 
   - link to icon (link to local storage of small png)

__companions__:
Base mute companions.
Has inventory, random weapons inside based on team level.
They have an appropriate amount of health, defense based on team level. Ask Sem.
Sends current weapon to companions subclass, receives damage value based on its formula. Ask sem

__party__:
Contains the player and companions.

Mainly manages turns in combat for the npcs and also keeps track of party level. This decides how strong companions are.

The amount of enemies to be slain before a party level up is as follows:
Level: number_of_enemies
   - 1: 1
   - 2: 2
   - 3: 4
   - 4: 8
   - 5: 10
max cap: 10 enemies

Also influences enemy strength, higher level party = higher level enemies.

__player__:
Should ideally be a class

Has a name, inventory, and a class. ask sem

when performing an attack a weapon is selected from the inventory if there is 1 available

that weapon is passed onto the player class subclass

receives damage from players class subclass

__player class__:
subclass of player

receives weapon details from the player class, calculates damage, then returns damage to player

contains the players health value, damage formula and defense
these change based on level, appropriate values need to be decided.

Available classes: 
   - Figher
   - Mage
   - Barbarian
   - Rogue

__enemy__:
Should ideally be a class
They will have: 
   - hp: int
   - dmg: text
   - def: int

Has a name, inventory, and a class. ask sem

when performing an attack a weapon is selected from the inventory if there is 1 available that weapon is passed onto the monster type subclass
receives damage from monster type subclass

__enemy type__:
subclass of monster

receives weapon details or modifiers from the monster class, calculates damage, returns damage to monster

contains the monster health value, damage formula and defense
these change based on level, appropriate values need to be decided.

Available enemy types: 
   - goblin
   - orc
   - dragon
   - ask sem



