import sys
from random import randrange, seed
from time import perf_counter
from itertools import chain

import dearpygui.dearpygui as dpg
from Obstacle import Obstacle
from Swarm import Swarm

from Quadtree import Rectangle, Quadtree


def rand_coords(limit=500):
    """Paire de coordonnées aléatoires"""
    return (randrange(limit), randrange(limit))

def update_naive():
    """Exécuté chaque frame"""
    nb_operations = 0

    obstacles = list(chain(swarm_obstacles, mur))
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
    quad.insert_all(chain(swarm_particules, swarm_obstacles, mur))

    nb_operations = 0
    for particule in swarm_particules:
        particule.move(1.5, 0)
        potential_collisions = set(quad.retrieve(particule)) - set([particule])
        for autre in potential_collisions:
            nb_operations += 1
            # particule.check_collision(autre)
            if particule.check_collision(autre):
                swarm_particules.remove(particule)
                break # On retourne à la grande boucle
    # print(f"{nb_operations=}")


## Variables globales ##

DIMENSIONS_FENETRE = (600, 600)
MIN_COORD = int(min(DIMENSIONS_FENETRE) - 10)

NB_PARTICULES = 1000
RADIUS_PARTICULES = 3
coords_particules = [rand_coords(MIN_COORD) for _ in range(NB_PARTICULES)]
NB_OBSTACLES = 30
coords_obstacles = [rand_coords(MIN_COORD) for _ in range(NB_OBSTACLES)]

coords_mur = [(DIMENSIONS_FENETRE[0], y)
              for y in range(0,
                             MIN_COORD + Obstacle.RADIUS,
                             Obstacle.RADIUS * 2)]

seed(0)
dpg.create_context()

with dpg.window(tag="primary_window"):
    quad = Quadtree("primary_window", level=0, bounds=Rectangle(0, 0, *DIMENSIONS_FENETRE))

    mur = Swarm.obstacles(coords_mur)

    swarm_particules = Swarm.particules(coords_particules, RADIUS_PARTICULES)
    swarm_obstacles = Swarm.obstacles(coords_obstacles)

    # obstacles = [*swarm_obstacles, *mur]

    # with dpg.handler_registry():
    #     dpg.add_mouse_move_handler(callback=update_naive, user_data=data)
dpg.set_primary_window("primary_window", True)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (200, 200, 200))
dpg.bind_theme(global_theme)


dpg.create_viewport(width=DIMENSIONS_FENETRE[0] + 30,
                    height=DIMENSIONS_FENETRE[1] + 50,
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
