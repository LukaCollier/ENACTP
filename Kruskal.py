import UnionFind
class Graph:
    def __init__(self,vertex,edge):
        '''
        vertex : 'a list
        edge : ('a * int * 'a) list
        '''
        self.vertex=vertex
        self.edge=edge
    
def kruskal(g):
    edge=g.edge[:]
    edge.sort(key=lambda n : n[1])
    dic={i:j for (j,i) in enumerate(g.vertex)}
    uf=UnionFind.UnionFind(len(g.vertex))
    def rec_aux(edg,tree):
        if len(edg)==0:
            return tree
        else:
            e=edg[0]
            e1=dic[e[0]]
            e2=dic[e[2]]
            if uf.find(e1) == uf.find(e2):
                return rec_aux(edg[1:],tree)
            else:
                uf.unir(e1,e2)
                tree.append(e)
                return rec_aux(edg[1:],tree)
    return rec_aux(edge,[])
            