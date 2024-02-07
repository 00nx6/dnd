from flask import Flask, render_template, request, redirect
from random import randint

app = Flask(__name__)

app.config['TEMPLATE_AUTO_RELOAD'] = True

@app.route('/class_setup', methods=['POST', 'GET'])
def setup():
    return render_template('setup.html',
                           classes=[SubClass(), SubClass(), SubClass(), SubClass()],
                           nav_title='Welcome.')

class SubClass:
    def __init__(self):
        self.hp = 12
        self.name = 'Archer'
        self.img_src = '../static/courser.png'

def main():
    pass

if __name__ == '__main__':
    main()

"""
what i have so far for the prompt:

I have created a dictionary to store information for a DND like story game, the contents of this will be used according to the comments left in the dictionary. you will return it in the exact same format.

Here is a bit more information about the contents and how it has to be populated:
the `page_title` refers to a main title that will be displayed at the top of the screen, the next obj in the list will have most of the information,
the title will refer to the current chapter title,
description will be where the story is portrayed.
When there is a`variable_type: int` given as a value, the expected value will be returned as a single int for that entry.
When there is a `format`, it should be a string in the format provided. Otherwise everything will be explained in the comments in the dictionary. I will paste it after this message. Populate it as if we were playing an actual game of DND and thats how you stored the information.

--dict

the entries 'enemies' , 'friendly_npc'  and 'interact'  only need to be populated when they are a part of the story, so when youre talking to an character, they should be in the friendly_npc list, or if youre in battle the enemies youre fighting should be in the enemies list or if there are no items mentioned in the story the `interact` section should be left empty. Only populate `enemies`, `friendly_npc` and `interact` when the entries were mentioned by name in the story.

you will populate it as if you were a game master in this game and this is how you stored the information

from this point on i will only enter one of the options provided in the main story, can you keep generating dictionaries based on the options i pick?
"""


ai_response = {
    'page_title': 'Usually referring to the current story arc or location',
    'chapter': {
        # will be displayed to the user.
        'title': 'current story chapter',
        # contains a short story
        'story': 'max 150 words',
        # options to move forward in the story.
        'story_actions': {
            'npc_option': [
                'example: Purchase offered goods', 'example: Accept Quest'
                ],
                'enemy_option': [
                    'example: attack enemy', 'example: loot corpse'
                ],
                'entity_options': [
                    'example: pull lever', 'example: open chest'
                ]
            },
        # list of enemies in combat with
        # only populate if mentioned by name in the story
        'enemies': [
            {
                'enemy_name': 'Variable_type: text',
                'health': 'variable_type: int',
                'defense': 'Variable_type: int',
                'damage': 'format: 1d6+2, Variable_type:string',
                'inventory': 'weapon name',
                'attacks': {
                    # im still not sure how attacks work
                    # but please fill in the blanks
                    'attack 1': 'attack name'
                },
            },
            # ...
        ],
        # list of friendly_npcs in the vicinity
        # only refers to quest givers traders and usually interact-able town NPCs
        # only populate if mentioned by name in the story
        'friendly_npc': [
            {
                'name': 'variable_type; text',
                'race': 'variable_type: text',
                'type': 'variable_type: text, example: Elf',
                'role': 'merchant',
                'has_quest': 'variable_type: bool, if has quest for player true else false',
                'items_for_sale': [
                    'item1', 'item2'
                ]
            },
            {
                'name': 'variable_type; text',
                'race': 'variable_type: text',
                'type': 'variable_type: text, example: Dark Elf',
                'role': 'Variable_type: text, example: Tyrant king of Nilfgaard',
                'has_quest': 'variable_type: bool, if has quest for player true else false'
                
            }
        ],
        # objects that can be interacted with in the nearby vicinity
        # should be used in exploration parts of the story
        # can be left blank in combat situations/exploration situations
        # only populate if mentioned by name in the story
        
        'interact': [
            {
                'name': 'chest',
                'type': 'object',
            },
            {
                'name': 'lever',
                'type': 'object',
                'consequence': 'variable_type: string, example: Pull the lever and the door opens.'
            }
        ]
    }
}

