from math import *

def shrink_min(l):
    i = l.index(min(l))
    n= len(l)
    if i == n-1:
        return l[0:i]
    return l[0:i]+l[i+1:n]



def mean_geo(nb):
    nb_log=[log(i) for i in nb]
    return exp(sum(nb_log)/len(nb))




def sortedm(nb,m):
    return sorted(nb, key=lambda n: n%m)

def premier(n):
    erat=[True for i in range(n+1)]
    sn=floor(sqrt(n))
    for i in range(2,sn+1):
        if erat[i]:
            for j in range((i*i),n+1, i):
                erat[j]=False
    return [ (i+2) for (i,flag) in enumerate(erat[2:]) if flag]


def isalphanum(c):
    return '0' <= c <= '9' or 'a' <= c <= 'z' or 'A'<= c <= 'Z'



def words(s:str):
    '''
    Par principe isalnum() est en O(|s|) et isalphanum en O(|1|)
    words est en O(|s|)
    '''
    res =''
    j=0
    for i,c in enumerate(s):
        if not(isalphanum(c)):
            res = res +' '+ s[j:i]
            j=i+1
    return res.split()

def words(s):
    filt= "".join(c if c.isalnum() else ' ' for c in s )
    return filt.split()
     

def main():
    l=(-100,23,45,789,-1,45,-8)
    print(shrink_min(l))
    print(mean_geo([1,1,1,1,1]))
    print(sortedm((1,2,3,4,5,6,7,8,9,10),3))
    print(premier(1000))
    print(words("patatede ;cam; info/ truc nuche"))
main()


