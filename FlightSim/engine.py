from world import Runway, World
import random
import math
import aircraft


ANIM = 50  # Animation time step (milliseconds)
DT = ANIM / 1000


class SimEngine:

    def __init__(self, world, turbulence, aircraft):
        self.rwy = world.runway
        self.world = world
        self.turbulence = turbulence
        self.aircraft = aircraft
        self.aircraft.set_position(-2 * self.rwy.length, 0.0, 0.09 * self.rwy.length)
        self.landing_message = None

    def step(self):
        self.turbulence(self.aircraft)
        self.aircraft.fly(DT)
        self.aircraft.update()

    def reset(self):
        x = -(1.5 + random.random()) * self.rwy.length
        y = (2 * random.random() - 1) * self.rwy.length
        z = (0.1 + random.random() * 0.02) * self.rwy.length
        self.aircraft.reset()
        self.aircraft.set_position(x, y, z)
        self.aircraft.look_at((-self.rwy.mark-self.rwy.length, 0, 0.05 * self.rwy.length))

    def message(self):
        x, y, z = self.aircraft.position
        heading = math.degrees(self.aircraft.heading) % 360
        pitch = math.degrees(self.aircraft.pitch) % 360
        mark = -self.rwy.mark if x < 0 else self.rwy.mark
        slope = 100 * (z - self.aircraft.height) / math.sqrt((x - mark) ** 2 + y ** 2)
        lateral = math.degrees(math.atan2(y, abs(mark - x)))
        if 0 < x: lateral = -lateral
        message = ""
        if abs(x) < self.rwy.length / 2 and abs(y) < self.rwy.width / 2:
            if 1 < pitch and self.aircraft.height < z < aircraft.Z_CUTOFF:
                message = "Arrondissez"
            elif z <= self.aircraft.height:
                if self.landing_message is None:
                    roll = math.degrees(self.aircraft.roll) % 360
                    if 15 < roll < 345: message = "CRASH !"
                    elif 7 < roll < 353: message = "UNE AILE CASSEE !"
                    elif 357 < pitch: message = "OK"
                    elif 350 < pitch: message = "SUPER !"
                    elif pitch < 4: message = "DUR"
                    else: message = "TRAIN CASSE !"
                    self.landing_message = message
                else: message = self.landing_message
        elif z <= self.aircraft.height: message = "CRASH !"
        elif ((-1.7 * self.rwy.length < x < mark and (heading < 90 or 270 < heading))
              or (mark < x < 1.7 * self.rwy.length and (90 < heading < 270))):
            if lateral < -0.7: message = "A droite de l'axe\n"
            elif 0.7 < lateral: message = "A gauche de l'axe\n"
            if slope < 5: message += "En dessous du plan\n"
            elif 6 < slope: message += "Au dessus du plan\n"
            elif pitch < 2 or 4 < pitch: message += "Restez sur le plan"
            if message == "": message = "Super, continuez"
        else: message = "Essayez de vous poser..."
        return message
