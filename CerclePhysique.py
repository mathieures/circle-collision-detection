import dearpygui.dearpygui as dpg
from Rectangle import Rectangle


"""
TODO : implanter un quad/octree
       Ah, sinon, faire des tests sur un truc à part et "recopier" ici
       genre en affichant des points, et des lignes où on coupe, etc.
       https://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374
"""


class CerclePhysique:
    """Un objet physique, dont le node est donné par dpg dans le main"""
    @property
    def bounding_box(self):
        """
        La bounding box pour insérer plus facilement dans
        le quadtree, sous la forme x, y, width, height
        """
        bb_x = self.coords[0] - self.rayon // 2
        bb_y = self.coords[1] - self.rayon // 2
        return Rectangle(bb_x, bb_y, self.rayon * 2, self.rayon * 2)

    def __init__(self, node, coords, rayon, couleur):
        self.node = node
        self.coords = coords
        self.rayon = rayon

        # On dessine
        self.cercle = dpg.draw_circle((0, 0), self.rayon, fill=couleur)

    def action_collision(self):
        """Méthode appelée quand l'objet est sujet à une collision"""
        raise NotImplementedError

    def check_collision(self, objet):
        """Détecte les collisions avec le CerclePhysique passé en paramètre"""
        raise NotImplementedError

    def __repr__(self):
        return f"<{type(self).__name__} en {self.coords}>"