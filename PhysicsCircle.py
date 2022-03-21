import dearpygui.dearpygui as dpg
from Rectangle import Rectangle


class PhysicsCircle:
    """A physical circle, whose "node" (matrix) must be created by dpg"""
    __slots__ = ["node", "coords", "radius", "circle"]

    @property
    def bounding_box(self):
        """
        Get the bounding box of the PhysicsCircle, to insert easily
        in the quadtree in the form of a Rectangle
        """
        half_radius = self.radius // 2
        double_radius = self.radius * 2
        bb_x = self.coords[0] - half_radius
        bb_y = self.coords[1] - half_radius
        return Rectangle(bb_x, bb_y, double_radius, double_radius)


    def __init__(self, node, coords, radius, color):
        self.node = node
        self.coords = coords
        self.radius = radius

        # Draw the circle
        self.circle = dpg.draw_circle((0, 0), self.radius, fill=color)

    def __repr__(self):
        return f"{type(self).__name__} of radius {self.radius} at {self.coords}"


    def action_collision(self):
        """Called only when the object collides"""
        raise NotImplementedError

    def check_collision(self, objet):
        """Detects collision with the PhysicsCircle in parameter"""
        raise NotImplementedError