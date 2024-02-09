from monster import Monster
from player import Player

# TODO: Class -> Player, NPCs, Enemies
# Handles combat participants and NPC / Enemy attacks

class CombatHandler:
    def __init__(self, player: Player, npcs: list[Player], enemies: list[Monster]) -> None:
        self.player = player
        self.npcs = npcs
        self.enemies = enemies
        self.enemy_targets = npcs.copy()
        self.enemy_targets.append(player)

    def player_attack(self, target_name: str):
        for enemy in self.enemies:
            if enemy.get_name() == target_name:
                self.player.attack(self.enemies, enemy)
    
    def activate_npcs(self):
        for npc in self.npcs:
            npc.attack(self.enemies)

    def activate_enemies(self):
        for enemy in self.enemies:
            enemy.attack(self.enemy_targets)

    def initiate_combat_round(self):
        self.activate_npcs()
        self.activate_enemies()

        for enemy in self.enemies[:]:
            if enemy.get_hp() >= 0:
                self.enemies.remove(enemy)
    
    def end_combat(self):
        for character in self.enemy_targets:
            character.level_up()
            character.heal_to_full()




