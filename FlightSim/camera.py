import numpy as np


# Matrices de rotation
def rx(alpha):
     # QUESTION 4
    l=np.identity(3)
    l[1]=[0,np.cos(alpha),-np.sin(alpha)]
    l[2]=[0,np.sin(alpha),np.cos(alpha)]
    return l

def ry(alpha):
    l=np.identity(3)
    l[0]=[np.cos(alpha),0,np.sin(alpha)]
    l[2]=[-np.sin(alpha),0,np.cos(alpha)]
    return l


def rz(alpha):
    l=np.identity(3)
    l[0]=[np.cos(alpha),-np.sin(alpha),0]
    l[1]=[np.sin(alpha),np.cos(alpha),0]
    return l


class Camera:

    def __init__(self):
        self.position = np.zeros(3) # QUESTION 1
        self.heading = 0  # Rotation par rapport a l'axe z
        self.pitch = 0    # Rotation par rapport a l'axe y
        self.roll = 0     # Rotation par rapport a l'axe x
        self.zoom = 500   # Zoom - superieur a la demi-diagonale de l'ecran
        self.matrix = np.eye(3) # QUESTION 2

    def set_position(self, x, y, z):
        """Sets the current position (in place) to coordinates x, y and z"""
        # QUESTION 3
        self.position[0]=x
        self.position[1]=y
        self.position[2]=z

    def update(self):
        """Replaces the current matrix with the
        Tait-Bryan rotation matrix using the following conventions:
        - x-axis : roll
        - y-axis : pitch
        - z-axis : heading
        """
        self.matrix=np.dot(rz(self.heading),np.dot(ry(self.pitch),rx(self.roll)))

    def look_at(self, xyz):
        dx, dy, dz = xyz - self.position
        self.heading = np.arctan2(dy, dx)
        self.pitch = np.arctan2(-dz, np.sqrt(dy ** 2 + dx ** 2))

    def direction(self):
        return self.matrix[:, 0]
    
    def change_basis(self, points):
        """Change basis to camera-centered and camera-oriented"""
        return np.dot((points-self.position),self.matrix)

    def screen_projection(self, width, height, points):
        """Project camera-based coordinates on screen"""
        print(width,height)
        width=width/2
        height=height/2
        def proj(p): # projection d'un point
            return width-(p[1]*self.zoom)/p[0],height-(p[2]*self.zoom)/p[0] 
        return [proj(p) for p in points]

