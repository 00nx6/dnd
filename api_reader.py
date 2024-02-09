# AI response expected format
ai_response = {
    "page_title": "The Forbidden Forest",
    "chapter": {
        "title": "Lost in the Woods",
        "story": "You find yourself lost in the dense woods of the Forbidden Forest, the twisted trees blocking out the sun. As you navigate through the thick underbrush, you stumble upon an ancient ruin, its crumbling stones whispering secrets of long-forgotten magic. Suddenly, a pack of snarling wolves emerges from the shadows, their eyes gleaming with hunger.",
        "enemies": [
            {
                "enemy_name": "Wolf Pack",
                "health": 20,
                "defense": 2,
                "damage": "1d6+2"
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

