from math import dist
import dearpygui.dearpygui as dpg

import colors
from PhysicsCircle import PhysicsCircle


class Particule(PhysicsCircle):
    """A particule: a PhysicsCircle that can move"""
    __slots__ = ["speed"]

    def __init__(self, node, coords, radius=5, speed=1):
        super().__init__(node, list(coords), radius, color=colors.BLACK)
        self.speed = speed
        # self.alive = True


    def action_collision(self):
        # self.alive = False
        self.speed = 0
        # dpg.delete_item(self.circle)
        dpg.configure_item(self.circle, fill=colors.RED)

    def check_collision(self, objet):
        """Check if there is a collision between this Particule and another PhysicsCircle"""
        # if self.alive:
        if dist(self.coords, objet.coords) < self.radius + objet.radius:
            # print("hit")
            self.action_collision()
            # objet.action_collision()
            return True
        return False

    def move(self, delta_x, delta_y, speed=None):
        """Moves the Particule with relative coordinates"""
        if speed is None:
            speed = self.speed
        self.coords[0] += delta_x * speed
        self.coords[1] += delta_y * speed
        dpg.apply_transform(self.node, dpg.create_translation_matrix(self.coords))
