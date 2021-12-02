"""
Classe utilisée pour l'affichage d'images n'ayant pas d'influence sur l'univers physique du jeu.

NORMALEMENT plus rapide que d'utiliser la classe entité (qui est un classe abstraite)
"""


class Sprite:
    def __init__(self, image, position=(0, 0)):
        self.image = image
        self.position = position

    def draw(self, surface):
        surface.draw(self.image, self.position)
