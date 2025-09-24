#slide6


from math import pi
r=170/2
h=30
V=h*pi*r**2
M=V/1000

print(M)


l=[i%2 for i in range(10)]
print(l)


def masse_piscine(diam,h):
    return (diam/2)**2*pi*h/1000

print(masse_piscine(170,30))
print(masse_piscine(190,30))

def sgn(i):
    '''
    signe de i
    '''
    return 1 if i>0 else (-1 if i<0 else 0)

print(sgn(0))


def surface(rayon):
    return pi*rayon**2

def volumme(diametre=170,hauteur=30):
    '''
    si oublie de variable pas grave
    '''
    return surface(diametre/2)*h

print(volumme())

def factocode(n,i):
    while i<9:
        print(i, 'x', n, '=', i*n)
        i+=1
    return None

factocode(7,2)
