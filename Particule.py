from math import dist
import dearpygui.dearpygui as dpg
import couleurs
from CerclePhysique import CerclePhysique


class Particule(CerclePhysique):
    """Une particule : un cercle physique qui peut bouger"""
    def __init__(self, node, coords, rayon=5, vitesse=1):
        super().__init__(node, list(coords), rayon, couleur=couleurs.NOIR)
        self.vitesse = vitesse
        # self.vivant = True

    def action_collision(self):
        # self.vivant = False
        self.vitesse = 0
        # dpg.delete_item(self.cercle)
        dpg.configure_item(self.cercle, fill=couleurs.ROUGE)

    def check_collision(self, objet):
        """Première passe de l'algorithme de collision : algorithme naïf"""
        # if self.vivant:
        if dist(self.coords, objet.coords) < self.rayon + objet.rayon:
            # print("hit")
            self.action_collision()
            # objet.action_collision()
            return True
        return False

    def move(self, delta_x, delta_y, vitesse=None):
        """Bouge la particule en relatif"""
        if vitesse is None:
            vitesse = self.vitesse
        # x, y = dpg.get_item_user_data(self.node)
        self.coords[0] += delta_x * vitesse
        self.coords[1] += delta_y * vitesse
        dpg.apply_transform(self.node, dpg.create_translation_matrix(self.coords))
        # dpg.set_item_user_data(self.node, (x + delta_x, y + delta_y))