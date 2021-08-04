#基于Ks的简单贪心算法

import copy
import networkx as nx
import numpy as np

class PyLouvain:

    '''
        Builds a graph from _path.
        _path: a path to a file containing "node_from node_to" edges (one per line)
    '''
    @classmethod
    def from_file1(cls, path): #接收邻接矩阵
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        nodes = {}
        edges = []
        k=0 #记录当前行数
        for line in lines:
            nodes[k]=1 
            n = line.split()
            if not n:
                break
            m = len(n)  #一行有多少数
            for i in range(0,m):
                if int(n[i]) != 0:
                    nodes[i]=1
                    w=1  
                    if int(n[i]) != 1:
                        w = n[i]
                    edges.append(((k, i), w))
            k+=1
        # rebuild graph with successive identifiers
        # nodes_, edges_ = in_order(nodes, edges)
        print("%d nodes, %d edges" % (len(nodes), len(edges)))
        return cls(nodes, edges)
        

    @classmethod
    def from_file(cls, path):
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        nodes = {}
        edges = []
        for line in lines:
            n = line.split()
            if not n:
                break
            nodes[n[0]] = 1
            nodes[n[1]] = 1
            w = 1
            if len(n) == 3:
                w = int(n[2])
            edges.append(((n[0], n[1]), w))
        # rebuild graph with successive identifiers
        # nodes_, edges_ = in_order(nodes, edges)
        print("%d, %d" % (len(nodes), len(edges)))
        return cls(nodes, edges)

    @classmethod
    def from_gml_file(cls, path):
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        nodes = {}
        edges = []
        current_edge = (-1, -1, 1)
        in_edge = 0
        for line in lines:
            words = line.split()
            if not words:
                break
            if words[0] == 'id':
                nodes[int(words[1])] = 1
            elif words[0] == 'source':
                in_edge = 1
                current_edge = (int(words[1]), current_edge[1], current_edge[2])
            elif words[0] == 'target' and in_edge:
                current_edge = (current_edge[0], int(words[1]), current_edge[2])
            elif words[0] == 'value' and in_edge:
                current_edge = (current_edge[0], current_edge[1], int(words[1]))
            elif words[0] == ']' and in_edge:
                edges.append(((current_edge[0], current_edge[1]), 1))
                current_edge = (-1, -1, 1)
                in_edge = 0
        # nodes, edges = in_order(nodes, edges)
        # print("%d, %d" % (len(nodes), len(edges)))
        return cls(nodes, edges)

    @classmethod
    def from_ERgraph(cls, n,m): # n为点数，m为边
        p = 2*m/(n*(n-1))
        G = nx.random_graphs.erdos_renyi_graph(n,p)
        Gnodes = {}
        Gedges = []
        for nd in G.nodes:
            Gnodes[nd]=1
        for ed in G.edges:
            Gedges.append(((ed[0],ed[1]),1))
        # print("%d, %d" % (len(nodes), len(edges)))
        return cls(Gnodes, Gedges)

    @classmethod
    def from_WSgraph(cls, a,b,p): # a为点数，b为邻居数，p为重连概率
        G = nx.random_graphs.watts_strogatz_graph(a,b,p)
        Gnodes = {}
        Gedges = []

        for nd in G.nodes:
            Gnodes[nd]=1
        for ed in G.edges:
            Gedges.append(((ed[0],ed[1]),1))
        # print("%d, %d" % (len(nodes), len(edges)))
        return cls(Gnodes, Gedges)

    @classmethod
    def from_BAgraph(cls, n,m): # n为点数，m为每次加入数
        G = nx.random_graphs.barabasi_albert_graph(n,m)
        Gnodes = {}
        Gedges = []
        for nd in G.nodes:
            Gnodes[nd]=1
        for ed in G.edges:
            Gedges.append(((ed[0],ed[1]),1))
        # print("%d, %d" % (len(nodes), len(edges)))
        return cls(Gnodes, Gedges)

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.edges_of_node = {}
        # precompute m (sum of the weights of all links in network)
        #            k_i (sum of the weights of the links incident to node i)
        for e in edges:
            # save edges by node self.edges_of_node
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
                self.edges_of_node[e[0][1]].append(e)
        for n in nodes:
            if n not in self.edges_of_node:
                self.edges_of_node[n]=[]
        self.e_o_n = copy.deepcopy(self.edges_of_node)

    '''
        Applies the Louvain method.
    '''
    def apply_method(self,z): 


        #1 建立覆盖集
        k = len(self.nodes)*z
        node1=copy.deepcopy(self.nodes)
        # print(self.nodes)
        S={}
        data = {}
        data1={} #访问过的
        ks = 1
        
        def dg(i):
            return len(self.e_o_n[i])
            
        def degree(i):
            d = 0
            if i not in self.e_o_n or i in data1:
                return 0
            for a in self.e_o_n[i]:
                if a[0][0] in data1 or a[0][1] in data1:
                    continue                
                d+=1
            return d

        while node1:
            # 暂存度为ks的顶点
            temp = []
            m=10000
            id = 0

            dg1={i:degree(i) for i in node1}
            for i,n in dg1.items():
                if n == m:
                    temp.append(n)
                if n < m:
                    temp=[i]
                    m = n
            # print(temp)
            for i in temp:
                if i in node1:
                # S.append(i)
                    node1.pop(i)
                data1[i]=1
                # print(i)
            data[ks] = temp
            ks += 1
            # print(node1)

        while len(S) < k:  # num相当于flag
            ks -= 1
            if ks == 0:
                break
            for i in data[ks]:
                S[i]=1 #依次添加入S
                if len(S) >= k :
                    break

        def nb1(node): # neighbors
            for e in self.e_o_n[node]:
                if e[0][0] == node and e[0][1] not in S:
                    yield e[0][1]
                if e[0][1] == node and e[0][1] not in S:
                    yield e[0][0]        
        
        nb={i:nb1(i) for i in self.e_o_n}

        def f(S1):
            #cp:connection_partition
            cp = {}
            visited = []
            stack = []
            id = 0
            cp[0]=[]
            num=0

            def dfs(v):  #搜索连通分量
                cp[id].append(v)
                visited.append(v) 
                stack.append(v)
                while stack:
                    node = stack.pop()
                    if v in nb:
                        
                        for neighbour in nb[v]: 
                            if neighbour not in visited and neighbour not in S1: 
                                visited.append(neighbour) 
                                cp[id].append(neighbour) 
                                stack.append(neighbour)
                return len(cp[id])

            for v in self.nodes:
                if v not in visited and v not in S1:
                    id += 1 
                    cp[id]=[]
                    n = dfs(v)  
                    if n < 2:
                        continue
                    num += n*(n-1)/2

            return num



        #现在开始回添。选最终节点对最大的点，也就是f最大
        while len(S) > k :
            id = 0
            m = -1
            for i in S:
                o=f(S.keys()-{i})
                if o>m:
                    id = i
                    m=o
            print(id)
            S.pop(id)
            nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}
        # print(len(S))

        nb={i:nb1(i) for i in self.e_o_n}
        return f(S)



    '''
        Builds the initial partition from _network.
        _network: a (nodes, edges) pair
    '''

'''
    Rebuilds a graph with successive nodes' ids.
    _nodes: a dict of int
    _edges: a list of ((int, int), weight) pairs
'''
def in_order(nodes, edges):
        # rebuild graph with successive identifiers
        nodes = list(nodes.keys())
        nodes.sort()
        i = 0
        nodes_ = []
        d = {}
        for n in nodes:
            nodes_.append(i)
            d[n] = i
            i += 1
        edges_ = []
        for e in edges:
            edges_.append(((d[e[0][0]], d[e[0][1]]), e[1]))
        return (nodes_, edges_)









