class UnionFind:
    def __init__(self,n):
        self.parent=list(range(n))
        self.rang=[0]*n
    def find(self,i):
        if self.parent[i]!=i:
            self.parent[i]= self.find(self.parent[i])
        return self.parent[i]
    def unir(self,i,j):
        repi=self.find(i)
        repj=self.find(j)
        
        if repi==repj:
            return False
        if self.rank[repi]>self.rank[repj]:
            self.parent[repj]=repi
        elif self.rank[repj]>self.rank[repi]:
            self.parent[repi]=repj
        else:
            self.parent[repj]=repi
            self.rank[repi]+=1
        return True