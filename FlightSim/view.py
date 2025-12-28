from tkinter import Canvas
from world import SKY_COLOR, GRASS_COLOR
import math


WORLD = "world" # tag for the main scene


def interpol(p1, p2):
    x1, y1, z1 = p1
    x12, y12, z12 = p2 - p1
    dy = y12 * x1 - y1 * x12
    dz = z12 * x1 - z1 * x12
    if dy == 0 or dz == 0:
        return (1., y1 / x1, z1 / x1)
    else:
        k = max((y1 / x1 + 1.) / abs(dy), (z1 / x1 + 1.) / abs(dz))
        return (1., y1 / x1 + k * dy, z1 / x1 + k * dz)


def visible_objects(face):
    '''Extracts the visible part of a face'''
    front = []
    for i in range(len(face)):
        j = (i + 1) % len(face)
        if max(abs(face[i, 1]), abs(face[i, 2])) < face[i, 0]:
            front.append(face[i])
            if face[j, 0] <= max(abs(face[j, 1]), abs(face[j, 2])):
                front.append(interpol(face[i], face[j]))
        elif max(abs(face[j, 1]), abs(face[j, 2])) < face[j, 0]:
            front.append(interpol(face[j], face[i]))
    return front


class View(Canvas):

    def __init__(self, sim, parent, **kwargs):
        super().__init__(parent, bg=SKY_COLOR, **kwargs)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.sim = sim
        self.x, self.y = 0, 0
        self.create_text(400, 30, tag="comment")
        self.pack()
        self.focus_set()
        self.bind("<KeyPress>", self.key_handler)
        self.bind("<ButtonPress-1>", self.save_pos)
        self.bind("<Button1-Motion>", self.drag)
        self.bind("<ButtonRelease-3>", lambda _ev: self.sim.reset())

    def save_pos(self, event): self.x, self.y = event.x, event.y

    def drag(self, event):
        self.sim.aircraft.steer(event.x - self.x, event.y - self.y)
        self.save_pos(event)

    def key_handler(self, event):
        dx, dy = 20, 5
        if event.keysym == "q": self.winfo_toplevel().destroy()
        elif event.keysym == "r": self.sim.reset()
        elif event.keysym == "Up": self.sim.aircraft.steer(0, -dy)
        elif event.keysym == "Down": self.sim.aircraft.steer(0, dy)
        elif event.keysym == "Right": self.sim.aircraft.steer(dx, 0)
        elif event.keysym == "Left": self.sim.aircraft.steer(-dx, 0)

    def set_text(self, text): self.itemconfigure("comment", text=text)

    def draw(self, coords, fill, outline):
        try: self.create_polygon(coords, fill=fill, outline=outline, tag=WORLD)
        except IndexError: pass # not enought points in coords

    def draw_ground(self):
        ac = self.sim.aircraft
        dz = math.tan(ac.pitch) * ac.zoom
        if ac.zoom < dz:
            polygon = ((0, 0), (self.width, 0), (self.width, self.height), (0, self.height))
        else:
            s = math.sin(ac.roll)
            c = math.cos(ac.roll)
            x0, y0 = self.width / 2 - s * dz, self.height / 2 - c * dz
            dx, dy = self.width * c, self.width * s
            polygon = ((x0 - dx, y0 + dy), (x0 - dx + dy, y0 + dy + dx),
                       (x0 + dx + dy, y0 - dy + dx), (x0 + dx, y0 - dy))
        self.draw(polygon, GRASS_COLOR, "")

    def draw_face(self, face):
        ac = self.sim.aircraft
        visible = visible_objects(ac.change_basis(face.coords))
        to_draw = [(p[0], p[1]) for p in ac.screen_projection(self.width, self.height, visible)]
        self.draw(to_draw, face.color, "")

    def draw_all(self):
        self.delete(WORLD)
        self.draw_ground()
        for obj in self.sim.world.all():
            self.draw_face(obj)
        self.create_text(self.width / 2, self.height / 2, text="+", fill="yellow", tag=WORLD)
        self.tag_lower(WORLD)
