class Node:
    def __init__(self):
        self.pred=None
        self.rang=0
    def __eq__(self,other):
        return self.pred==other.pred

class UnionFind:
    def __init__(self):
        self.nodes={}


    def add(self,i):
        self.nodes[i]=Node()

    def find(self,i):
        if self.nodes[i].pred==None:
            return i
        else:
            a=self.find(self.nodes[i].pred)
            self.nodes[i].pred=a
            return a

    def union(self,id1,id2):
        rep1=self.find(id1)
        rep2=self.find(id2)
        if rep1==rep2:
            return False
        if self.nodes[rep1].rang>self.nodes[rep2].rang:
            self.nodes[rep2].pred=rep1
        elif self.nodes[rep2].rang>self.nodes[rep1].rang:
            self.nodes[rep1].pred=rep2
        else:
            self.nodes[rep2].pred=rep1
            self.nodes[rep1].rang+=1
        return True
