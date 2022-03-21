import dearpygui.dearpygui as dpg


class Rectangle:
    """A rectangle: a point and dimensions"""
    __slots__ = ["x", "y", "width", "height"]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{type(self).__name__}, {self.x, self.y, self.width, self.height}"

    def __iter__(self):
        """Used to easily cast a Rectangle to a tuple"""
        return iter((self.x, self.y, self.width, self.height))


class DebugRectangle(Rectangle):
    """A debug rectangle, drawn on the screen"""
    __slots__ = ["tag"]

    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height)

        self.tag = dpg.draw_rectangle(
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            **kwargs
        )


    def delete(self):
        """Graphically deletes the DebugRectangle"""
        try:
            dpg.delete_item(self.tag)
        # Raised when dpg reassigns the tag
        except SystemError:
            pass