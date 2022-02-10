import dearpygui.dearpygui as dpg
from Rectangle import Rectangle


class PhysicsCircle:
    """Un objet physique, dont le node est donné par dpg dans le main"""
    @property
    def bounding_box(self):
        """
        La bounding box pour insérer plus facilement dans
        le quadtree, sous la forme x, y, width, height
        """
        bb_x = self.coords[0] - self.radius // 2
        bb_y = self.coords[1] - self.radius // 2
        return Rectangle(bb_x, bb_y, self.radius * 2, self.radius * 2)


    def __init__(self, node, coords, radius, color):
        self.node = node
        self.coords = coords
        self.radius = radius

        # On dessine
        self.circle = dpg.draw_circle((0, 0), self.radius, fill=color)

    def __repr__(self):
        return f"<{type(self).__name__} en {self.coords}>"


    def action_collision(self):
        """Méthode appelée quand l'objet est sujet à une collision"""
        raise NotImplementedError

    def check_collision(self, objet):
        """Détecte les collisions avec le PhysicsCircle passé en paramètre"""
        raise NotImplementedError