from tkinter import Canvas


class CustomCanvas(Canvas):
    """Un canvas qui peut dire si un point est à l'intérieur"""
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height)
        super().pack()

    def is_in_bounds(self, x, y):
        return (0 <= x <= int(self["width"])) and (
                0 <= y <= int(self["height"]))