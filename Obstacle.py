from PhysicsCircle import PhysicsCircle
import colors


class Obstacle(PhysicsCircle):
    """Un obstacle, qui ne laisse pas passer les particules"""
    RADIUS = 9

    def __init__(self, coords):
        super().__init__(coords, radius=type(self).RADIUS, color=colors.GREY)
    # def __init__(self, node, coords):
    #     super().__init__(node, coords, radius=type(self).RADIUS, color=colors.GREY)


    def check_collision(self, other):
        """L'obstacle ne fait rien"""

    def action_collision(self):
        """L'obstacle ne fait rien"""