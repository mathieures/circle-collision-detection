from collections import namedtuple
import dearpygui.dearpygui as dpg


Rectangle = namedtuple("Rectangle", ["x", "y", "width", "height"])


# class Rectangle:
#     """Un rectangle, constitué d'un point et de dimensions"""
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height

#     def __repr__(self):
#         return f"{type(self).__name__}, {self.x, self.y, self.width, self.height}"

#     def __iter__(self):
#         """Sert à transformer un Rectangle en tuple plus facilement"""
#         return iter((self.x, self.y, self.width, self.height))


class DebugRectangle(Rectangle):
    """Un Rectangle mais qui est affiché graphiquement"""
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height)

        self.tag = dpg.draw_rectangle(
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            **kwargs
        )

    # def __eq__(self, other):
    #     """
    #     Permet de déterminer si deux DebugRectangle sont identiques.
    #     Utilisé avec self.__hash__ par Quadtree pour ne pas en redessiner
    #     """
    #     if isinstance(other, type(self)):
    #         return (self.x == other.x) and (
    #                 self.y == other.y) and (
    #                 self.width == other.width) and (
    #                 self.height == other.height)
    #     return NotImplemented

    # def __hash__(self):
    #     return hash((self.x, self.y, self.width, self.height))


    def delete(self):
        """Supprime le rectangle graphiquement"""
        try:
            dpg.delete_item(self.tag)
        # Levée quand le tag a été réassigné je crois
        except SystemError:
            pass