class Inode:
    def __init__(self,name,path=''):
        self.name =name
        self.path = path
        
    def full_path(self):
        return f"{self.path}/{self.name}"
    
    def get_size(self):
        return 0
    
    def set_path(self,path):
        self.path=path
        
class File(Inode):
    def __init__(self,name,size,path=''):
        super().__init__(name,path)
        self.size=size
        
    def get_size(self):
        return self.size
    def __repr__(self):
        return f'{super().full_path()}, {self.size} octets'
'''
f=File("cute_cat.jpg",1000000)
print(f)
print(f.get_size())
'''

class Directory(Inode):
    def __init__(self,name,path=''):
        super().__init__(name,path)
        self.contents=[]
    def add_inode(self,file):
        file.set_path(self.full_path())
        self.contents.append(file)
    def get_size(self):
        return sum(f.get_size() for f in self.contents)
    
    def set_path(self,path):
        super().set_path(path)
        for f in self.contents:
                f.set_path(self.full_path())
                
                
home = Directory("home")
alice = Directory("alice")
images = Directory("images")
musique = Directory("musique")
vac1 = File("vacances_1.jpg", 3000000)
vac2 = File("vacances_2.jpg", 4000000)
cat  = File("cute_cat.jpg", 1000000)
home.add_inode(alice)
alice.add_inode(images)
alice.add_inode(musique)
images.add_inode(vac1)
images.add_inode(vac2)
images.add_inode(cat)
home.set_path("")  

for inode in [home, alice, images, vac1, vac2, cat, musique]:
    size = inode.get_size() // 1000000
    print(f"{inode.full_path()} ({size}Mo)")

    