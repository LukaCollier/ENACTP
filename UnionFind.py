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
        if self.rang[repi]>self.rang[repj]:
            self.parent[repj]=repi
        elif self.rang[repj]>self.rang[repi]:
            self.parent[repi]=repj
        else:
            self.parent[repj]=repi
            self.rang[repi]+=1
        return True