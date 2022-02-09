import dearpygui.dearpygui as dpg


class Rectangle:
    """Un rectangle, constitué d'un point et de dimensions"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{type(self).__name__}, {self.x, self.y, self.width, self.height}"


class DebugRectangle(Rectangle):
    """Un Rectangle mais qui est affiché graphiquement"""
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height)

        self.tag = dpg.draw_rectangle(
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            **kwargs
        )