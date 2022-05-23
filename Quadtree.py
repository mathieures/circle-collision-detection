# https://gamedevelopment.tutsplus.com/tutorials/quick-tip-use-quadtrees-to-detect-likely-collisions-in-2d-space--gamedev-374
from Rectangle import Rectangle, DebugRectangle
import colors


class Quadtree:
    """A quadtree"""
    # MAX_OBJECTS = 5
    MAX_OBJECTS = 5
    # MAX_LEVELS = 10
    MAX_LEVELS = 20

    def __init__(self, window, level, bounds):
        self.window = window
        self.level = level # 0 being the root
        self.bounds = bounds # The 2D space the node occupies, a Rectangle object
        self.objects = [] # List of objects, here Rectangle objects for the example
        self.nodes = [None] * 4 # The 4 child nodes

        self.debug_zones = []


    def clear(self):
        """Recursively clear the Quadtree"""
        for zone in self.debug_zones:
            zone.delete()

        self.objects.clear()
        for i, node in enumerate(self.nodes):
            if node is not None:
                node.clear() # Calls the clear() method of the Quadtree child
                self.nodes[i] = None

    def split(self):
        """Split the Quadtree into 4 child Quadtree nodes"""
        sub_width = self.bounds.width // 2
        sub_height = self.bounds.height // 2
        x, y = self.bounds.x, self.bounds.y

        next_level = self.level + 1

        # Top right
        self.nodes[0] = Quadtree(self.window, next_level,
                                 Rectangle(x + sub_width, y, sub_width, sub_height))
        # Top left
        self.nodes[1] = Quadtree(self.window, next_level,
                                 Rectangle(x, y, sub_width, sub_height))
        # Bottom left
        self.nodes[2] = Quadtree(self.window, next_level,
                                 Rectangle(x, y + sub_height, sub_width, sub_height))
        # Bottom right
        self.nodes[3] = Quadtree(self.window, next_level,
                                 Rectangle(x + sub_width, y + sub_height, sub_width, sub_height))

        # Draw the zones
        self.debug_zones.append(DebugRectangle(x + sub_width, y, sub_width, sub_height, color=colors.RED, parent=self.window))
        self.debug_zones.append(DebugRectangle(x, y, sub_width, sub_height, color=colors.RED, parent=self.window))
        self.debug_zones.append(DebugRectangle(x, y + sub_height, sub_width, sub_height, color=colors.RED, parent=self.window))
        self.debug_zones.append(DebugRectangle(x + sub_width, y + sub_height, sub_width, sub_height, color=colors.RED, parent=self.window))

    def get_index(self, other):
        """
        Returns the index of the child in which the object passed in
        parameter should go, or -1 if it should be in none of them
        """
        rect = other.bounding_box

        index = -1

        vertical_midpoint = self.bounds.x + self.bounds.width // 2
        horizontal_midpoint = self.bounds.y + self.bounds.height // 2

        # Can the object completely fit in the top half?
        in_top_half = rect.y < horizontal_midpoint and rect.y + rect.height < horizontal_midpoint

        # Can the object completely fit in the bottom half?
        in_bottom_half = rect.y > horizontal_midpoint # We only have to test the origin

        # If it can completely fit in the left half
        if rect.x < vertical_midpoint and rect.x + rect.width < vertical_midpoint:
            # If it can fit in the top half, then it's in the top left part
            if in_top_half:
                index = 1
            elif in_bottom_half:
                index = 2
        # If it can completely fit in the right half
        elif rect.x > vertical_midpoint:
            if in_top_half:
                index = 0
            elif in_bottom_half:
                index = 3

        return index

    def insert(self, obj):
        """
        Insert an object in the Quadtree (if it has a bounding box).
        If the target nde is full, it's split, and the
        objects are put in the right child nodes
        """
        # If the node has children, insert the object in one of them
        if self.nodes[0] is not None:
            index = self.get_index(obj)
            if index != -1:
                self.nodes[index].insert(obj)
                return

        # Else, either the object doesn't fit, or the node has no child
        # We add the object to the node
        self.objects.append(obj)

        if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if self.nodes[0] is None:
                self.split()

            # Dispatch the objects in the children
            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def insert_all(self, objects):
        """Insert a list of objects in the tree"""
        for obj in objects:
            self.insert(obj)

    def retrieve(self, obj, potential_collisions=None):
        """
        Return all the objects that could collide
        with the object given in parameter
        """
        # At the first call of the function
        if potential_collisions is None:
            potential_collisions = []

        index = self.get_index(obj)
        if index != -1 and self.nodes[0] is not None:
            self.nodes[index].retrieve(obj, potential_collisions)

        potential_collisions.extend(self.objects)

        # print(f"{potential_collisions=}")
        return potential_collisions