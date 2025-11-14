import random
import math
from camera import Camera

TURBULENCE = 0.01
AERO_FACTOR = 0.999
BRAKE_FACTOR = 0.99
Z_CUTOFF = 10 # engine cutoff altitude for landing
MAX_SPEED = 200  # km/h
HEIGHT = 2 # Aircraft height in m

TWO_PI = 2 * math.pi


def bound(lb, ub, v): return max(lb, min(ub, v))


class Aircraft(Camera):

    def __init__(self, height=HEIGHT):
        super().__init__()
        self.height = height
        self.speed = MAX_SPEED

    def reset(self):
        self.roll = 0
        self.speed = MAX_SPEED

    def fly(self, dt):
        z = self.position[2]
        d = self.direction()
        dz = d[2]
        if z <= Z_CUTOFF:  # Engines off
            if self.height < z:
                self.speed *= AERO_FACTOR
                dz = dz - 0.02 * (MAX_SPEED - self.speed)
            else:  # Brake
                self.speed *= BRAKE_FACTOR
                self.roll = 0
                self.pitch *= 0.7
                dz = 0
        else:
            self.speed = MAX_SPEED
        dist = dt * self.speed / 3.6
        self.position[:2] += dist * d[:2]
        self.position[2] = max(self.height, z + dist * dz)
        incl = bound(-2.5, 2.5, math.tan(self.roll))
        self.heading -= 0.01 * incl

    def steer(self, dx, dy):
        scale = 0.002
        self.roll += dx * scale
        self.pitch -= math.cos(self.roll) * dy * scale
        self.heading += math.tan(self.roll) * dy * scale
        if math.cos(self.pitch) < 0:
            self.roll = (self.roll + math.pi) % TWO_PI
            self.pitch = (math.pi - self.pitch) % TWO_PI
            if math.pi < self.pitch: self.pitch -= TWO_PI
            self.heading += math.pi
        # TODO : if roll > 90
