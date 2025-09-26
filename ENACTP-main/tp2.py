class Fraction:
    
    def __init__(self,num,dem):
        pgcd=gcd(num,dem)
        self.numerator = num//pgcd
        self.denominator =dem//pgcd
    
    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"
    def approximate(self):
        return self.numerator/self.denominator
    def __add__(self,f2):
        num = self.numerator*f2.denominator+self.denominator*f2.numerator
        dem = self.denominator*f2.denominator
        return Fraction(num,dem)
def sum_r(l):
    res=Fraction(0,1)
    for i in l:
        res=res+i
    return res

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def leibniz(n):
    return [Fraction(8,((4*i+1)*(4*i+3))) for i in range(n)]

def sum_approximate(fractions):
    return sum(f.approximate() for f in fractions)


f=Fraction(104348,33215)
print(f)

f1=Fraction(15,45)
f3=f+f1

L=leibniz(1001)
fp=sum_r(L)

print(fp)
print(sum_approximate(L))
