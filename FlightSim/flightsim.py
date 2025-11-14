from tkinter import Tk
from aircraft import Aircraft
from atmosphere import Turbulence
from engine import ANIM, SimEngine
from view import View
from world import Runway, World

class FlightSimulator(Tk):

    def __init__(self):
        super().__init__()
        self.title("Python Flight Simulator")
        runway = Runway()
        world = World(runway)
        turbulence = Turbulence()
        aircraft = Aircraft()
        self.sim = SimEngine(world, turbulence, aircraft)
        self.view = View(self.sim, self, width=800, height=450)
        self.view.draw_all()

    def loop(self):
        self.sim.step()
        self.view.after(ANIM, self.loop)
        self.view.draw_all()
        self.view.set_text(self.sim.message())

    def start(self):
        self.after(100, self.loop)
        self.mainloop()


if __name__ == '__main__':
    flightsim = FlightSimulator()
    flightsim.start()
