from flask import Flask, render_template, redirect, request, url_for
from player import Player as Pr
from player import gen_lvl1_info, return_class_name_list
from combat_handler import CombatHandler
from openAI import OpenAIInterpreter


game_content = {}

ai_interpreter = OpenAIInterpreter()

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True

# Welcome page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def user():
    user_name = request.form['user_name']
    return redirect(url_for('setup', user_name=user_name))


# class setup
@app.route('/class_setup', methods=['GET'])
def setup():
    user_name = request.args.get('user_name')
    return render_template('setup.html',
                           classes=gen_lvl1_info(),
                           user_name=user_name
                        )
    
@app.route('/class/<user_info>', methods=['GET'])
def return_class(user_info):
    """_summary_

    Args:
        user_info (str): string containing user name, and player class, format: subclass=Rogue;user_name=Lajos;

    Returns:
        redirect: redirects to story
    """
    if not user_info.startswith('subclass='):
        redirect('/')
    
    player_class, user_name = (value.split('=')[-1] for value in user_info.rstrip(';').split(';'))

    return redirect(url_for('story', player_class=player_class, user_name=user_name))


def init_class(user_name, player_subclass):
    player = Pr(name=user_name, subclass=player_subclass)
    npcs = [Pr(name=subclass, subclass=subclass) for subclass in return_class_name_list() if subclass != player_subclass]

    return player, npcs

@app.route('/story', methods=['GET'])
def story():
    player_subclass = request.args.get('player_class')
    user_name = request.args.get('user_name')

    player_class, npcs = init_class(user_name=user_name, player_subclass=player_subclass)

    game_content['player'] = player_class
    game_content['npcs'] = npcs

    response = {
    'page_title': 'Usually referring to the current story arc or location',
    'chapter': {
        # will be displayed to the user.
        'title': 'current story chapter',
        # contains a short story
        'story': "Welcome, brave adventurers, to the mystical realm of Eldoria, where magic and monsters reign supreme. The land is cloaked in ancient mysteries, and a palpable tension hangs in the air as unseen forces vie for control. As you step into the bustling city of Eldoria's Crossroads, a mysterious letter arrives, beckoning you to the Moonlight Citadel. Rumors of a long-lost artifact, the Astral Keystone, have surfaced, and its rediscovery could tip the balance of power in the realm. Your party, a diverse group of warriors, mages, and rogues, has been chosen by fate to embark on this perilous quest. From the shadowy Whispering Woods to the fiery depths of the Dragon's Maw, you will face formidable challenges, forge alliances, and unravel the secrets that bind Eldoria. The fate of the realm rests in your hands, and as the sun sets on the horizon, your journey into the unknown begins. May your swords stay sharp, spells true, and courage unwavering in this epic Dungeons & Dragons adventure!",

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
    # if 'ongoing' in game_content:
    #     response = ai_interpreter.get_next_chapter(player_class.level)
    # else:
    #     response = ai_interpreter.get_opener()
    #     game_content['ongoing'] = True
    
    # if response is None:
    #     game_content['enemies'] = []
    #     resp = {}
    # else:
    #     game_content['enemies'] = response.get_chapter_enemies()
    #     resp = response.get_ai_response()
    # print(resp)
    return render_template('story.html',
                           res=response,
                           player_class=player_class,
                           npcs=npcs,
                           nav_title='current story chapter'
                           )

@app.route('/story/combat', methods=['GET'])
def combat():
    response = {
    'page_title': 'Usually referring to the current story arc or location',
    'chapter': {
        # will be displayed to the user.
        'title': 'current story chapter',
        # contains a short story
        'story': "Welcome, brave adventurers, to the mystical realm of Eldoria, where magic and monsters reign supreme. The land is cloaked in ancient mysteries, and a palpable tension hangs in the air as unseen forces vie for control. As you step into the bustling city of Eldoria's Crossroads, a mysterious letter arrives, beckoning you to the Moonlight Citadel. Rumors of a long-lost artifact, the Astral Keystone, have surfaced, and its rediscovery could tip the balance of power in the realm. Your party, a diverse group of warriors, mages, and rogues, has been chosen by fate to embark on this perilous quest. From the shadowy Whispering Woods to the fiery depths of the Dragon's Maw, you will face formidable challenges, forge alliances, and unravel the secrets that bind Eldoria. The fate of the realm rests in your hands, and as the sun sets on the horizon, your journey into the unknown begins. May your swords stay sharp, spells true, and courage unwavering in this epic Dungeons & Dragons adventure!",

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
                'enemy_name': 'Dog',
                'health': 20,
                'defense': 5,
                'damage': '1d6+2',
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
    return render_template('combat.html',
                           res=response,
                           player_class=game_content['player'],
                           npcs=game_content['npcs'])
                           

@app.route('/story/combat/<enemy>')
def enemy_selection(enemy):
    ch = CombatHandler(game_content['player'], game_content['npcs'], game_content['enemies'])
    ch.player_attack(enemy)
    results = ch.initiate_combat_round()
    game_content['player'] = results.get('player', '')
    game_content['npcs'] = results.get('npcs', '')
    game_content['enemies'] = results.get('enemies', '')
    return redirect('/story/combat')

if __name__ == '__main__':
    app.run(debug=True)


ai_response = {
    'page_title': 'Usually referring to the current story arc or location',
    'chapter': {
        # will be displayed to the user.
        'title': 'current story chapter',
        # contains a short story
        'story': "Welcome, brave adventurers, to the mystical realm of Eldoria, where magic and monsters reign supreme. The land is cloaked in ancient mysteries, and a palpable tension hangs in the air as unseen forces vie for control. As you step into the bustling city of Eldoria's Crossroads, a mysterious letter arrives, beckoning you to the Moonlight Citadel. Rumors of a long-lost artifact, the Astral Keystone, have surfaced, and its rediscovery could tip the balance of power in the realm. Your party, a diverse group of warriors, mages, and rogues, has been chosen by fate to embark on this perilous quest. From the shadowy Whispering Woods to the fiery depths of the Dragon's Maw, you will face formidable challenges, forge alliances, and unravel the secrets that bind Eldoria. The fate of the realm rests in your hands, and as the sun sets on the horizon, your journey into the unknown begins. May your swords stay sharp, spells true, and courage unwavering in this epic Dungeons & Dragons adventure!",

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

