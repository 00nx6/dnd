# AI response expected format
ai_response = {
    'page_title': 'The Forbidden Forest',
    'chapter': {
        'title': 'Lost in the Woods',
        'story': "You find yourself lost in the heart of the Forbidden Forest. The dense canopy blocks out most of the sunlight, leaving you in near darkness. Strange sounds echo around you, and you can't shake the feeling of being watched.",
        'enemies': [
            {
                'enemy_name': 'Darkwood Goblins',
                'health': 15,
                'defense': 12,
                'damage': '1d6+2 slashing'
            },
            {
                'enemy_name': 'Shadow Wolves',
                'health': 20,
                'defense': 14,
                'damage': '1d8+1 piercing'
            }
        ]
    }
}

class ResponseHandler:
    def __init__(self, ai_response: dict) -> None:
        self.__title = ai_response.get('page_title', 'title')
        self.__chapter = ai_response.get('chapter', {'title': '', 'story': '', 'enemies': []})

    def get_title(self):
        return self.__title
    
    def get_chapter(self):
        return self.__chapter
    
    def get_chapter_title(self):
        return self.__chapter.get('title', '')
    
    def get_chapter_story(self):
        return self.__chapter.get('story', '')
    
    def get_chapter_enemies(self):
        return self.__chapter.get('enemies', '')

