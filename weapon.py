def player_weapons():
    return {
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
