import random

def rand(): return random.random() - 0.5


class Turbulence:

    def __init__(self, roll=0.01, pitch=0.007, heading=0.003):
        self.roll = roll
        self.pitch = pitch
        self.heading = heading

    def __call__(self, aircraft):
        aircraft.roll += self.roll * rand()
        aircraft.pitch += self.pitch * rand()
        aircraft.heading += self.heading * rand()
