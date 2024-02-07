# OOP: Accessing

## 1. Private attributes
- Modify your code to convert all class attributes to private attributes, 
    - meaning that you need to prefix them with two underscore and that you make sure they are only accessed by methods of the class itself. 
    - In order to interact with other classes, you may no longer touch their attributes. 
    - Instead, you should ask the other class nicely to do what you want it to do, by calling a method on it.


 From this point onwards, we expect you to use __only private attributes__ (with two underscores) in your classes in __all of your OOP assignments!__ This is not something that is commonly done in Python code you'll find 'in the wild', but it will help you learn __*abstraction*__ in code, and when done right it sure helps readability. 

## 2. Weapon class
Create a class named __Weapon__ with the following methods:

##### A constructor:
Should create attributes for the weapon's name, strength, reliability and weight, the values for which are semi-randomly provided by this code:

##### get_damage:
 - decrements the weapon's reliability by 1 (due to wear and tear)
 - returns the amount of damage the weapon now does to an opponent. 
 - This is calculated by multiplying the strength with a random integer between 0 and the weapon's reliability.

__str__: 
Should return:
 - Bronze Bow (12 strength, 5 reliability, 4 kg).
    - When the reliability is 0, the return value should be similar to: Bronze Bow (BROKEN).

##### upgrade: 
Increases either the strength or the reliability of the weapon with some random amount [1..15]. 
- increases the weapon's weight with a random amount [1..5]. 
 - Afterwards, it prints the stats for the upgraded weapon (relying on __str__).
 
#### 3. Extend Player

When it's a players turn, he/she should get two additional options:
##### Find a weapon
 - This should instantiate a new Weapon and add it to a (private) list of weapons that the object should have as an attribute.
##### Upgrade a weapon. 
 - This should allow the user to select (using ask_choice) one of his/her weapons, for which the upgrade method must be called.
- The attack method should be modified,     
    - asks the user to select a weapon used for the attack. 
    - The damage to the selected opponent should be determined by the weapon's get_damage method.

    
Two new methods should be implemented:
- get_weapon_count
    - which should return the number of weapons the player is holding.
 - get_weapon_weight
    -  return the total weight for all weapons the player is holding.
    - __str__ method should be updated to return something like this: 
        - `Peter (100 hp, 3 weapons, 44 kg),` making use of the above two methods.

At the end of each turn, the play_turn method should check:
 - the player's weapon weight doesn't exceed 50 kg, 
    - player cannot carry more than 50kg. - The player is asked to select weapons to drop (remove from the list of weapons) until the weight is below 50kg


#### 4. Save/load

We want to be able to automatically save the game after each turn, and resume it when we next start the game.

- After each turn, have Game.run use pickle to save the state of the entire Game object to a file.
- Instead of just creating a Game() on startup, the application should see if the save file exists, 
    - if it does use pickle to restore the Game object. 
        -Note that the constructor won't be called in this case - it will just set all attributes to how they were. This includes restoring any other objects (indirectly) referred to be these attributes.
    
- Note: that the turn variable is not preserved. It should be though, in order for the correct player to play first.



