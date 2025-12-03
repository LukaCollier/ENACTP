import sys, UnionFind, random, time


class Vertex(object):
    def __init__(self):
        self.adj = {}

    def __repr__(self):
        return str(self.adj)

    def add(self, v, w):
        self.adj[v] = w

    def is_adj(self, v):
        return v in self.adj


class WGraph(object):
    def __init__(self):
        self.nodes = {}

    def __repr__(self):
        return str(self.nodes)

    def add_node(self, u):
        self.nodes[u] = Vertex()

    def add_edge(self, u, v, w):
        unode = self.nodes.setdefault(u, Vertex())
        if not unode.is_adj(v): unode.add(v, w)
        vnode = self.nodes.setdefault(v, Vertex())
        if not vnode.is_adj(u): vnode.add(u, w)

    def edges(self):
        return [(u, v, w) for (u, node) in self.nodes.items()
                for (v, w) in node.adj.items() if u < v]
                
    def size(self):
        return len(self.nodes)

    def rand(self, n, m, w):
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        edges = random.sample(edges, m)
        for (u, v) in edges:
            self.add_edge(u, v, random.randint(1, w))



def kruskal(g):
    '''
    UnionFind O(alpha(|S|)
    algo en O((|A|+|S|)*log(|A|))
    '''
    edge=g.edges()
    edge.sort(key=lambda n : n[2])
    dic={i:j for (j,i) in enumerate(g.nodes)}
    uf=UnionFind.UnionFind(len(g.nodes))
    n=g.size()
    def rec_aux(edg,tree):
        if len(edg)==0 or len(tree)==n-1:
            return tree
        else:
            e=edg[0]
            e1=dic[e[0]]
            e2=dic[e[1]]
            if uf.find(e1) == uf.find(e2):
                return rec_aux(edg[1:],tree)
            else:
                uf.unir(e1,e2)
                tree.append(e)
                return rec_aux(edg[1:],tree)
    return rec_aux(edge,[])
