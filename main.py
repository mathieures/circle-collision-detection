import sys
from random import randrange, seed
from time import perf_counter
from itertools import chain
import dearpygui.dearpygui as dpg

from Quadtree import Rectangle, Quadtree
from Obstacle import Obstacle
from Swarm import Swarm


def rand_coords(limit=500):
    """Couple of random coordinates"""
    return (randrange(limit), randrange(limit))

def update_naive():
    """Executed every frame"""
    # nb_operations = 0
    obstacles = list(chain(swarm_obstacles, wall))
    for particule in swarm_particules:
        # Movement
        particule.move(1, 0)
        # Collision detection
        for obstacle in obstacles:
            # nb_operations += 1
            if particule.check_collision(obstacle):
                swarm_particules.remove(particule)
                break
    # print(f"{nb_operations=}")

def update_quadtree():
    """Executed every frame"""
    quad.clear()
    quad.insert_all(chain(swarm_particules, swarm_obstacles, wall))

    # nb_operations = 0
    for particule in swarm_particules:
        # Movement
        particule.move(1.5, 0)
        # Collision detection
        potential_collisions = set(quad.retrieve(particule)) - set([particule])
        for other in potential_collisions:
            # nb_operations += 1
            if particule.check_collision(other):
                swarm_particules.remove(particule)
                break # Go back to the outer loop
    # print(f"{nb_operations=}")


## Global variables ##

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
                             int(Obstacle.RADIUS * 1.7))]
                             # Obstacle.RADIUS * 2)]

seed(0)
dpg.create_context()

with dpg.window(tag="primary_window"):
    quad = Quadtree("primary_window", level=0, bounds=Rectangle(0, 0, *WINDOW_DIMENSIONS))

    wall = Swarm.obstacles(coords_wall)

    swarm_particules = Swarm.particules(coords_particules, RADIUS_PARTICULES)
    swarm_obstacles = Swarm.obstacles(coords_obstacles)

dpg.set_primary_window("primary_window", True)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (200, 200, 200))
dpg.bind_theme(global_theme)


# (0, 0) si not exactly teh top left corner with dpg so this centers the viewport better
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
