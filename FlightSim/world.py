import numpy as np

RWY_LENGTH = 1000 # m
RWY_WIDTH = 30 #m # RWY_LENGTH / 30

RWY_MARK_X_RATIO = 0.3
RWY_MARK_Y_RATIO = 0.3
CENTRAL_MARKS = 8

THR_MARK_LEN_RATIO = 0.05
THR_MARK_WIDTH_RATIO = 0.1
THR_MARKS = 4

# colors
RWY_COLOR = '#5A5348'
MARK_COLOR = "white"
GRASS_COLOR = '#608038'
SKY_COLOR = '#87CEEB'


class Polygon:

    def __init__(self, coords, color):
        self.coords = np.array(coords)
        self.color = color


class Rectangle(Polygon):

    def __init__(self, x, y, length, width, color):
        dx, dy = length / 2, width / 2
        x1, x2 = x - dx, x + dx
        y1, y2 = y - dy, y + dy
        super().__init__(((x1, y1, 0), (x2, y1, 0), (x2, y2, 0), (x1, y2, 0)), color)


class Runway(list):

    def __init__(self, width=RWY_WIDTH, length=RWY_LENGTH):
        super().__init__()
        self.width = width
        self.length = length
        self.mark = RWY_MARK_X_RATIO * length
        # Piste
        self.append(Rectangle(0, 0, length, width, RWY_COLOR))
        # Peignes
        dx, dy = length / 20, width / 10
        lx, ly = 0.8 * dx, 0.8 * dy
        for x in (-0.47 * length, 0.47 * length):
            for i in range(-THR_MARKS, THR_MARKS + 1):
                if i != 0:
                    self.append(Rectangle(x, i * dy, lx, ly, MARK_COLOR))
        # Traits centraux
        lx, ly = 0.6 * dx, 0.3 * dy
        for i in range(-CENTRAL_MARKS, CENTRAL_MARKS + 1):
            self.append(Rectangle(i * dx, 0, lx, ly, MARK_COLOR))
        # Plots
        mark_y = RWY_MARK_Y_RATIO * width
        for x in (-self.mark, self.mark):
            for y in (-mark_y, mark_y):
                self.append(Rectangle(x, y, dx, 2 * dy, MARK_COLOR))


class World:

    def __init__(self, runway, buildings=None):
        self.runway = runway
        self.buildings = [] if buildings is None else buildings

    def all(self):
        return self.buildings + self.runway
