import sys
from random import randrange, seed
from time import perf_counter
from itertools import chain
import dearpygui.dearpygui as dpg

from Quadtree import Rectangle, Quadtree
from Obstacle import Obstacle
from Swarm import Swarm


def rand_coords(limit=500):
    """Paire de coordonnées aléatoires"""
    return (randrange(limit), randrange(limit))


def update_naive():
    """Exécuté chaque frame"""
    nb_operations = 0

    obstacles = list(chain(swarm_obstacles, wall))
    for particule in swarm_particules:
        particule.move(1, 0)
        for obstacle in obstacles:
            nb_operations += 1
            if particule.check_collision(obstacle):
                swarm_particules.remove(particule)
                break
    # print(f"{nb_operations=}")


def update_quadtree():
    """Exécuté chaque frame"""
    quad.clear()
    quad.insert_all(chain(swarm_particules, swarm_obstacles, wall))

    nb_operations = 0
    for particule in swarm_particules:
        particule.move(1.5, 0)
        potential_collisions = set(quad.retrieve(particule)) - set([particule])
        for autre in potential_collisions:
            nb_operations += 1
            # particule.check_collision(autre)
            if particule.check_collision(autre):
                swarm_particules.remove(particule)
                break  # On retourne à la grande boucle
    # print(f"{nb_operations=}")


## Variables globales ##

WINDOW_DIMENSIONS = (600, 600)
MIN_COORD = int(min(WINDOW_DIMENSIONS) - 10)

NB_PARTICULES = 1000
RADIUS_PARTICULES = 3
coords_particules = [rand_coords(MIN_COORD) for _ in range(NB_PARTICULES)]
NB_OBSTACLES = 30
coords_obstacles = [rand_coords(MIN_COORD) for _ in range(NB_OBSTACLES)]

coords_wall = [(WINDOW_DIMENSIONS[0], y)
               for y in range(0,
                              MIN_COORD + Obstacle.RADIUS,
                              Obstacle.RADIUS * 2)]

seed(0)
dpg.create_context()

with dpg.window(tag="primary_window"):
    quad = Quadtree("primary_window", level=0,
                    bounds=Rectangle(0, 0, *WINDOW_DIMENSIONS))

    wall = Swarm.obstacles(coords_wall)

    swarm_particules = Swarm.particules(coords_particules, RADIUS_PARTICULES)
    swarm_obstacles = Swarm.obstacles(coords_obstacles)

    # obstacles = [*swarm_obstacles, *wall]

    # with dpg.handler_registry():
    #     dpg.add_mouse_move_handler(callback=update_naive, user_data=data)
dpg.set_primary_window("primary_window", True)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (200, 200, 200))
dpg.bind_theme(global_theme)


# Le (0, 0) n'est pas vraiment en haut à gauche donc il faut compenser
dpg.create_viewport(width=WINDOW_DIMENSIONS[0] + 30,
                    height=WINDOW_DIMENSIONS[1] + 50,
                    y_pos=0)
dpg.setup_dearpygui()
dpg.show_viewport()


# dpg.start_dearpygui()
# below replaces, start_dearpygui()


if len(sys.argv) > 1:
    update_function = update_naive
else:
    update_function = update_quadtree


t = perf_counter()
while dpg.is_dearpygui_running():
    update_function()
    dpg.render_dearpygui_frame()
print(f"temps de simulation : {perf_counter() - t}")
dpg.destroy_context()
