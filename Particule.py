from math import dist
from collections import namedtuple

import numpy as np
from numba import jit

import dearpygui.dearpygui as dpg

import colors
from PhysicsCircle import PhysicsCircle


Circle = namedtuple("Circle", ["coords", "radius"])


@jit(nopython=True)
# @jit("float32(float32[:], float32[:])", nopython=True)
def distance(point_1, point_2):
    """Retourne la distance euclidienne entre deux points"""
    # point_1 = np.array(point_1)
    # point_2 = np.array(point_2)
    diff = point_1 - point_2
    return np.sqrt(diff.dot(diff))
    # return dist(point_1, point_2)


# @jit(nopython=True)
def check_collision_circles(circle_1, circle_2):
    """Retourne True s'il y a une collision entre les deux cercles"""
    coords_1 = np.array(circle_1.coords)
    coords_2 = np.array(circle_2.coords)
    if distance(coords_1, coords_2) < circle_1.radius + circle_2.radius:
        # print("hit")
        # circle_1.action_collision()
        # circle_2.action_collision()
        return True
    return False


class Particule(PhysicsCircle):
    """Une particule : un cercle physique qui peut bouger"""

    def __init__(self, coords, radius=5, speed=1):
        super().__init__(list(coords), radius=radius, color=colors.BLACK)
    # def __init__(self, node, coords, radius=5, speed=1):
    #     super().__init__(node, list(coords), radius, color=colors.BLACK)
        self.speed = speed
        # self.alive = True


    def action_collision(self):
        # self.alive = False
        self.speed = 0
        # dpg.delete_item(self.circle)
        dpg.configure_item(self.circle, fill=colors.RED)

    def check_collision(self, other):
        """Vérifie la collision entre la particule et un autre cercle"""
        collision = check_collision_circles(Circle(self.coords, self.radius),
                                            Circle(other.coords, other.radius))
        if collision:
            self.action_collision()

    def move(self, delta_x, delta_y, speed=None):
        """Bouge la particule en relatif"""
        if speed is None:
            speed = self.speed
        self.coords[0] += delta_x * speed
        self.coords[1] += delta_y * speed
        # dpg.apply_transform(self.node, dpg.create_translation_matrix(self.coords))
        dpg.configure_item(self.circle, center=self.coords)