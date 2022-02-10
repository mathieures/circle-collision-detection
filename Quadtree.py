# https://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374
from numba import jit

from Rectangle import Rectangle, DebugRectangle
import colors


class Quadtree:
    """Un quadtree, ou arbre quartique"""
    # MAX_OBJECTS = 5
    MAX_OBJECTS = 5
    # MAX_LEVELS = 10
    MAX_LEVELS = 20

    @staticmethod
    @jit(nopython=True)
    def get_index_from_bb(rect_1, rect2):
        """
        Retourne l'indice du node dans lequel
        doit aller rect2, à partir de rect_1.
        rect_1 et rect_2 sont des tuples de 4 entiers.
        """
        index = -1

        self_x, self_y, self_height, self_width = rect_1
        rect_x, rect_y, rect_height, rect_width = rect2

        vertical_midpoint = self_x + self_width // 2
        horizontal_midpoint = self_y + self_height // 2

        # Est-ce que l'objet peut complètement tenir dans la moitié haute ?
        in_top_half = rect_y < horizontal_midpoint and rect_y + rect_height < horizontal_midpoint

        # Est-ce que l'objet peut complètement tenir dans la moitié basse ?
        in_bottom_half = rect_y > horizontal_midpoint # On peut ne tester que l'origine

        # S'il peut complètement tenir dans la partie gauche
        if rect_x < vertical_midpoint and rect_x + rect_width < vertical_midpoint:
            # S'il tenait dans la partie haute, il est en haut à gauche
            if in_top_half:
                index = 1
            elif in_bottom_half:
                index = 2
        # S'il peut complètement tenir dans la partie droite
        elif rect_x > vertical_midpoint:
            if in_top_half:
                index = 0
            elif in_bottom_half:
                index = 3

        return index


    def __init__(self, window, level, bounds):
        self.window = window
        self.level = level # 0 étant la racine
        self.bounds = bounds # l'espace 2D que le node occupe, un Rectangle
        self.objects = [] # liste d'objets, ici pour l'exemple des objets Rectangle
        self.nodes = [None] * 4 # les 4 noeuds fils

        self.debug_zones = []


    def clear(self):
        """Efface récursivement le Quadtree"""
        for zone in self.debug_zones:
            zone.delete()

        self.objects.clear()
        for i, node in enumerate(self.nodes):
            if node is not None:
                node.clear() # appelle la méthode clear() du Quadtree fils
                self.nodes[i] = None

    def split(self):
        """Sépare le Quadtree en 4 noeuds Quadtree fils"""
        sub_width = self.bounds.width // 2
        sub_height = self.bounds.height // 2
        x, y = self.bounds.x, self.bounds.y

        next_level = self.level + 1

        # En haut à droite
        self.nodes[0] = Quadtree(self.window, next_level,
                                 Rectangle(x + sub_width, y, sub_width, sub_height))
        # En haut à gauche
        self.nodes[1] = Quadtree(self.window, next_level,
                                 Rectangle(x, y, sub_width, sub_height))
        # En bas à gauche
        self.nodes[2] = Quadtree(self.window, next_level,
                                 Rectangle(x, y + sub_height, sub_width, sub_height))
        # En bas à droite
        self.nodes[3] = Quadtree(self.window, next_level,
                                 Rectangle(x + sub_width, y + sub_height, sub_width, sub_height))

        # On dessine les zones
        self.debug_zones.append(DebugRectangle(x + sub_width, y, sub_width, sub_height, color=colors.RED, parent=self.window))
        self.debug_zones.append(DebugRectangle(x, y, sub_width, sub_height, color=colors.RED, parent=self.window))
        self.debug_zones.append(DebugRectangle(x, y + sub_height, sub_width, sub_height, color=colors.RED, parent=self.window))
        self.debug_zones.append(DebugRectangle(x + sub_width, y + sub_height, sub_width, sub_height, color=colors.RED, parent=self.window))

    def get_index(self, objet):
        """
        Retourne l'indice du fils dans lequel l'objet passé
        en paramètre devra aller, ou -1 s'il n'est dans aucun
        """
        self_rect = tuple(self.bounds)
        other_rect = tuple(objet.bounding_box)
        index = self.get_index_from_bb(self_rect, other_rect)

        return index

    def insert(self, objet):
        """
        Insère un objet dans le Quadtree (s'il a une bounding box).
        Si le noeud cible est rempli, il est séparé
        et on met ses noeuds fils dans les bons noeuds
        """
        # Si le node a des enfants, on l'insère dans un enfant
        if self.nodes[0] is not None:
            index = self.get_index(objet)
            if index != -1:
                self.nodes[index].insert(objet)
                return

        # Sinon soit l'objet ne rentre pas soit il n'y a pas d'enfant
        # On ajoute l'objet au node
        self.objects.append(objet)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if self.nodes[0] is None:
                self.split()

            # On répartit les objets dans les enfants
            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def insert_all(self, objets):
        """Insère une liste d'objets dans l'arbre"""
        for objet in objets:
            self.insert(objet)

    def retrieve(self, objet, potential_collisions=None):
        """
        Retourne tous les objets qui pourraient
        collide avec l'objet donné en paramètre
        """
        # Au premier appel de la fonction
        if potential_collisions is None:
            potential_collisions = []

        index = self.get_index(objet)
        if index != -1 and self.nodes[0] is not None:
            self.nodes[index].retrieve(objet, potential_collisions)

        potential_collisions.extend(self.objects)

        # print(f"{potential_collisions=}")
        return potential_collisions