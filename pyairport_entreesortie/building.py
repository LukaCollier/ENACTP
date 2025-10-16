import geometry as geo
class BuildingError(Exception):
    pass

class Building:
    def __init__(self,name):
        self.name=name
        self.coordinates=[]
    def add_point(self,point):
        self.coordinates.append(point)
    def __repr__(self):
        return f'{self.name} : {self.coordinates}'


def from_file(filename):
    res=[]
    try:
        with open(filename,'r') as f:
            for line in f:
                line=line.strip()
                if line[0]=='[':
                    #name=line.split()[-1].split(']')[0]
                    name=line.split('[')[-1].split(']')[0]
                    res.append(Building(name))
                else:
                    try: #possible de creer une erreur à cause d'un changement de type
                        coord=line.split()
                        res[-1].add_point(geo.Point(int(coord[0]),int(coord[1]))) 
                    except ValueError:
                        #raise BuildingError("problème dans l'importation du point impossible de changer de type")
                        raise BuildingError("Segmentation Fault (Core dumped)")
        return res
    except FileNotFoundError:
        return []

#print(from_file("DATA/LFPG/terminals.txt"))
