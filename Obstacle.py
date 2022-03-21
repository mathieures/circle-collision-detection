from PhysicsCircle import PhysicsCircle
import colors

class Obstacle(PhysicsCircle):
    """
    An obstacle: a PhysicsCircle that freezes
    Particule objects coming in contact
    """
    __slots__ = []

    RADIUS = 9

    def __init__(self, node, coords):
        super().__init__(node, coords, radius=type(self).RADIUS, color=colors.GREY)


    def check_collision(self, objet):
        """The Obstacle does nothing"""

    def action_collision(self):
        """The Obstacle does nothing"""