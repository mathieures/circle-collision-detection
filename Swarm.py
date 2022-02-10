import dearpygui.dearpygui as dpg

from Particule import Particule
from Obstacle import Obstacle


class Swarm:
    """Un essaim d'objects, un groupe quoi"""
    @classmethod
    def particules(cls, coordinates, radius):
        """Essaim, mais de particules"""
        result = cls(coordinates)
        for coords in result.coordinates:
            # On crée un objet node (en gros une matrice)
            with dpg.draw_node() as particule_node:
                # On se déplace au bon endroit
                dpg.apply_transform(particule_node, dpg.create_translation_matrix(coords))
                particule = Particule(particule_node, coords, radius=radius, speed=1)
                result.objects.append(particule)
        return result

    @classmethod
    def obstacles(cls, coordinates):
        """Essaim, mais d'objets Obstacle"""
        result = cls(coordinates)
        for coords in result.coordinates:
            # On crée un objet node (en gros une matrice)
            with dpg.draw_node() as obstacle_node:
                # On se déplace au bon endroit
                dpg.apply_transform(obstacle_node, dpg.create_translation_matrix(coords))
                obstacle = Obstacle(obstacle_node, coords)
                result.objects.append(obstacle)
        return result


    def __init__(self, coordinates):
        self.coordinates = coordinates

        self.objects = []

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        """Sert pour l'unpacking"""
        return iter(self.objects)


    def remove(self, objet):
        """Supprime un objet de la liste"""
        self.objects.remove(objet)