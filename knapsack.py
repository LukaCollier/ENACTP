class Item:
    def __init__(self,id,w,v):
        self.id=id
        self.w=w
        self.v=v
    def __repr__(self):
        return f"{self.w},{self.v}"

    
def rec_knap(items,c):
    '''
    O(2^|items|) temporelle
    O(|items|) spatiale

    '''
    if len(items)==0:
        return 0
    else:
        if items[0].w>c:
            return rec_knap(items[1::],c)
        else:
            return max(rec_knap(items[1::],c),rec_knap(items[1::],c-items[0].w)+items[0].v)



def dyn_knap(items,c):
    '''
    O(|items|*c) en spatiale (matrice)
    O(|items|*c) en temporelle
    '''
    n=len(items)
    mat= [[0]*(c+1) for _ in range(n+1) ]
    for i in range(1,n+1):
        for j in range(1,c+1):
            if items[i-1].w>j:
                mat[i][j]=mat[i-1][j-1]
            else:
                mat[i][j]=max(mat[i-1][j],mat[i-1][j-items[i-1].w]+items[i-1].v)
    return mat


def knap_greedy(items,c):
    '''
    O(|items|log|items|)
    '''
    items=sorted(items, key=lambda x : x.v/x.w,reverse=True)
    res=0
    resl=[]
    pres=c
    for obj in items:
        if obj.w<=pres:
            pres-=obj.w
            res+=obj.v
            resl.append(obj.id)
    return res,resl

def rec_knapv2(items,c):
    '''
    O(2^|items|) temporelle
    O(|items|) spatiale

    '''
    if len(items)==0:
        return (0,[])
    else:
        if items[0].w>c:
            return rec_knap(items[1::],c)
        else:
            a=rec_knap(items[1::],c)
            b=rec_knap(items[1::],c-items[0].w)
            if a>b+items[0].v:
                return a
            else:
                l=b[1].append(items[0].id)
                return (b[0],l)

def dyn_knapv2(items,c):
    '''
    O(|items|*c) en spatiale (matrice)
    O(|items|*c) en temporelle
    '''
    n=len(items)
    mat= [[0]*(c+1) for _ in range(n+1) ]
    for i in range(1,n+1):
        for j in range(1,c+1):
            if items[i-1].w>j:
                mat[i][j]=mat[i-1][j-1]
            else:
                mat[i][j]=max(mat[i-1][j],mat[i-1][j-items[i-1].w]+items[i-1].v)
    l=[]
    j=c
    for i in  range(0,n):
        if mat[n-i][j]!=mat[n-i-1][j]:
            l.append(items[n-i-1].id)
            j=c-items[i-1].w
    return l
