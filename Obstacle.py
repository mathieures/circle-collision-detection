from CerclePhysique import CerclePhysique
import couleurs

class Obstacle(CerclePhysique):
    """Un obstacle, qui ne laisse pas passer les particules"""
    RAYON = 9
    def __init__(self, node, coords):
        super().__init__(node, coords, rayon=type(self).RAYON, couleur=couleurs.GRIS)

    def check_collision(self, objet):
        """L'obstacle ne fait rien"""
        pass

    def action_collision(self):
        """L'obstacle ne fait rien"""
        pass