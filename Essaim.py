import dearpygui.dearpygui as dpg
from Particule import Particule
from Obstacle import Obstacle


class Essaim:
    """Un essaim d'objets, un groupe quoi"""
    @classmethod
    def particules(cls, coordonnees, rayon):
        """Essaim, mais de particules"""
        result = cls(coordonnees)
        for coords in result.coordonnees:
            # On crée un objet node (en gros une matrice)
            with dpg.draw_node() as particule_node:
                # On se déplace au bon endroit
                dpg.apply_transform(particule_node, dpg.create_translation_matrix(coords))
                particule = Particule(particule_node, coords, rayon=rayon, vitesse=1)
                result.objets.append(particule)
        return result

    @classmethod
    def obstacles(cls, coordonnees):
        """Essaim, mais d'objets Obstacle"""
        result = cls(coordonnees)
        for coords in result.coordonnees:
            # On crée un objet node (en gros une matrice)
            with dpg.draw_node() as obstacle_node:
                # On se déplace au bon endroit
                dpg.apply_transform(obstacle_node, dpg.create_translation_matrix(coords))
                obstacle = Obstacle(obstacle_node, coords)
                result.objets.append(obstacle)
        return result

    def __init__(self, coordonnees):
        self.coordonnees = coordonnees

        self.objets = []

    def __len__(self):
        return len(self.objets)

    def __iter__(self):
        """Sert pour l'unpacking"""
        return iter(self.objets)

    def remove(self, objet):
        """Supprime un objet de la liste"""
        self.objets.remove(objet)