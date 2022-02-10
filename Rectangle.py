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

    def __iter__(self):
        """Sert à transformer un Rectangle en tuple plus facilement"""
        return iter((self.x, self.y, self.width, self.height))


class DebugRectangle(Rectangle):
    """Un Rectangle mais qui est affiché graphiquement"""
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height)

        self.tag = dpg.draw_rectangle(
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            **kwargs
        )


    def delete(self):
        """Supprime le rectangle graphiquement"""
        try:
            dpg.delete_item(self.tag)
        # Levée quand le tag a été réassigné je crois
        except SystemError:
            pass