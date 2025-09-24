def somme_i2(n):
    res = 0
    for i in range(1,n+1):
        res =res + i*i
    return res

def somme_i2_rec(n):
    if n==1:
        return 1
    else:
        return n*n +somme_i2_rec (n-1)

def somme_i2_rec_conditionnelle( n ):
    return 1 if n==1 else (n*n +somme_i2_rec_conditionnelle (n-1))

def somme_i2_gen( n):
    return sum(i*i for i in range(1,n+1))


def somme_i2_map (n):
    return sum(map(lambda i: i*i,(j for j in range(1,n+1))))

'''
print(somme_i2(3))
print(somme_i2_rec(3))
print(somme_i2_rec_conditionnelle(3))
print(somme_i2_gen(3))
print(somme_i2_map(3))
'''

class Point(object):
    def __init__(self, x=0,y=0):
        self.x=x
        self.y=y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy


class NamedPoint(Point): #tous les objets de la classe NamedPoint sont aussi des objets de la class Point
    def __init__(self,x,y,name):
        super().__init__(x,y)
        self.name=name

    def __repr__(self):
        return f"{self.name} = ({self.x},{self.y})" #f"{self.name} = {super().__repr__()}"



point=NamedPoint(5,4,"patate")
'''
print(point)

point.move(5,-3)

print(point)
'''

def letters(text):
    return [c for c in text if c.isalnum()]
def letterswset(text):
    '''
    si le caractère est present plusieurs fois alors il n'est sauvegardé qu'une fois
    '''
    return {c for c in text if c.isalnum()}
def occ(text):
    dic={}
    let= letters(text)
    for c in let:
        if c in dic:
            dic[c] +=1
        else:
            dic[c] = 1
    key = sorted(list(dic.keys()))
    for c in key:
        print(f"{c} -> {dic[c]}")
    return dic

#print(occ("patartyte hgeazertyuljhjgdgfgvqj,bh,azertjgd"))
def occwthin(text):
    dic={}
    let=letters(text)
    for c in let:
        dic.setdefault(c,0)
        dic[c]+=1
    key = sorted(list(dic.keys()))
    for c in key:
        print(f"{c} -> {dic[c]}")
    return dic



def inv_dic(dic):
    l=list(dic.keys())
    idic={}
    for k in l:
        idic[dic[k]]=k
    return idic

fr_en ={'avion':'aircraft', 'vol': 'flight', 'aile': 'wing'}

print(inv_dic(fr_en))

print(occwthin("patartyte hgeazertyuljhjgdgfgvqj,bh,azertjgdazeretryuyiulhqlydfbjffgncqfsvntjsqdfxbnkjsqdcvcnv,kgjsqqdvxcjkliuyteqzrqjklmoiuytfcserthjkiuygfrtyjkiuygfdertyuiopmljnbvcxqazsdfgtyhjl"))
