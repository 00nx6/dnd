# import urllib.request
from openai import OpenAI # `poetry add openai`
import json

# Configure the OpenAI API to work through our server (for payment credits)
openai = OpenAI(
    api_key="YOUR_TOKEN_GOES_HERE", # dldr7bh6dp55
    base_url="https://openai.sd42.nl/api/providers/openai/v1"
)

player_weapons = {
        'Fighter': {
            'level 1': {'name': 'Dagger', 'damage': '1d4', 'modifier': 0},
            'level 2': {'name': 'Shortsword', 'damage': '1d4', 'modifier': 2},
            'level 3': {'name': 'Longsword', 'damage': '1d12', 'modifier': 0},
            'level 4': {'name': 'Battleaxe', 'damage': '2d6', 'modifier': 2},
            'level 5': {'name': 'Greatsword', 'damage': '2d10', 'modifier': 0},
        },

        'Mage': {
            'level 1': {'name': 'Magic Missile', 'damage': '1d4', 'modifier': 0},
            'level 2': {'name': 'Firebolt', 'damage': '1d4', 'modifier': 1},
            'level 3': {'name': 'Lightning Bolt', 'damage': '3d4', 'modifier': 0},
            'level 4': {'name': 'Frost Nova', 'damage': '4d4', 'modifier': 0},
            'level 5': {'name': 'Meteor Swarm', 'damage': '4d4', 'modifier': 1},
        },

        'Barbarian': {
            'level 1': {'name': 'Club', 'damage': '1d4', 'modifier': 1},
            'level 2': {'name': 'Handaxe', 'damage': '1d6', 'modifier': 1},
            'level 3': {'name': 'Greataxe', 'damage': '1d12', 'modifier': 1},
            'level 4': {'name': 'Maul', 'damage': '2d10', 'modifier': -2},
            'level 5': {'name': 'Halberd', 'damage': '2d12', 'modifier': -2},
        },

        'Rogue': {
            'level 1': {'name': 'Shortbow', 'damage': '1d4', 'modifier': 0},
            'level 2': {'name': 'Dagger', 'damage': '1d4', 'modifier': 1},
            'level 3': {'name': 'Rapier', 'damage': '1d4', 'modifier': 4},
            'level 4': {'name': 'Twin Blades', 'damage': '2d8', 'modifier': 0},
            'level 5': {'name': 'Poisoned Twin Blades', 'damage': '2d8', 'modifier': 2},
        }
    }
ai_response = {
    'page_title': 'Usually referring to the current story arc or location',
    'chapter': {
        # will be displayed to the user.
        'title': 'current story chapter',
        # contains a short story
        'story': 'max 150 words',
        # options to move forward in the story.
        # list of enemies in combat with
        # only populate if mentioned by name in the story
        'enemies': [
            {
                'enemy_name': 'Variable_type: text',
                'health': 'variable_type: int',
                'defense': 'Variable_type: int',
                'damage': 'format: 1d6+2, Variable_type:string'
            },
            # ...
        ]
    }
}



prompt = f"""
I have created a dictionary to store information for a DND like story game, the contents of this will be used according to the comments left in the dictionary. you will return it in the exact same format.

Here is a bit more information about the contents and how it has to be populated:
the `page_title` refers to a main title that will be displayed at the top of the screen, the next obj in the list will have most of the information,
the title will refer to the current chapter title,
description will be where the story is portrayed.
When there is a`variable_type: int` given as a value, the expected value will be returned as a single int for that entry.
When there is a `format`, it should be a string in the format provided. Otherwise everything will be explained in the comments in the dictionary. I will paste it after this message. Populate it as if we were playing an actual game of DND and thats how you stored the information.

you will populate it as if you were a game master in this game and this is how you stored the information.

the story should always lead to an encounter and face  a monster. We want enemies for 5 levels.. If they kill all the enemies and level up then they move on to a new area where a new encounter awaits. For each encounter give a random amount of monsters (1 to 4)

the monster damage health and defense is based on these weapons, in one round of combat all 4 classes get one turn on the monster and the monster gets one turn too. damage is calculated by the damage of the player weapons - the monsters defense. An enemy should be killed in about 3 rounds. the campaign starts at level 1 and scale the monsters  later on when player levels also increase.

These are the possible weapons:

{json.dumps(player_weapons)}

Here's an example response:

{json.dumps(ai_response)}

Make sure you respond with only a valid JSON object.
"""

# Ask the LLM for a joke
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompt}
    ],
)
joke = response.choices[0].message.content
print(joke)


# # Convert the joke to spoken audio and save it as an MP3 file
# response = openai.audio.speech.create(model="tts-1", voice="alloy", input=joke)
# response.stream_to_file("joke.mp3")

# # Create a DALL-E image for the joke
# response = openai.images.generate(model="dall-e-3", prompt=joke, quality="standard", n=1, size="1024x1024")
# urllib.request.urlretrieve(response.data[0].url, 'joke.png')
