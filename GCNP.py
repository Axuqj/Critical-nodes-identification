#!/usr/bin/env python3
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
        print("%d nodes, %d edges" % (len(nodes), len(edges)))
        return cls(nodes, edges)

    '''
        Builds a graph from _path.
        _path: a path to a file following the Graph Modeling Language specification
    '''
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
        print("%d nodes, %d edges" % (len(nodes), len(edges)))
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
        print("%d nodes, %d edges" % (len(Gnodes), len(Gedges)))
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
        print("%d nodes, %d edges" % (len(Gnodes), len(Gedges)))
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
        print("%d nodes, %d edges" % (len(Gnodes), len(Gedges)))
        return cls(Gnodes, Gedges)

    '''
        Initializes the method.
        _nodes: a list of ints
        _edges: a list of ((int, int), weight) pairs
    '''
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        # precompute m (sum of the weights of all links in network)
        #            k_i (sum of the weights of the links incident to node i)
        self.m = 0
        self.k_i = [0 for n in nodes]
        self.edges_of_node = {}
        self.w = [0 for n in nodes]
        for e in edges:
            # save edges by node
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
                self.edges_of_node[e[0][1]].append(e)
        self.e_o_n = copy.deepcopy(self.edges_of_node)
        # access community of a node in O(1) time
        self.communities = [n for n in nodes]
        self.actual_partition = []

    def apply_method(self,z):
        #1 建立覆盖集
        S = []
        k = len(self.nodes)*z

        num = 1  
        # print(self.nodes)
        L = sorted(self.nodes,key= self.LNC,reverse=True)
        # print(L)
        while num: # num相当于flag
            for i in L:
                if i not in S:
                    S.append(i) #选出最大的，加入S
                    L.remove(i)
                    break
            num = 0
            for n in self.nodes:
                if n not in S:
                    if n not in self.e_o_n:
                        continue
                    for e in self.e_o_n[n]: #计算节点对数
                        if e[0][0] not in S and e[0][1] not in S: #存在边
                            num =1
                            break
                    if num == 1:  #加速迭代
                        break

        S = {i:1 for i in S}

        def nb1(node): # neighbors
            for e in self.e_o_n[node]:
                if e[0][0] == node and e[0][1] not in S.keys()-{i}:
                    yield e[0][1]
                if e[0][1] == node and e[0][1] not in S.keys()-{i}:
                    yield e[0][0]        
        
        nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}

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
            y = lambda x: S.keys()-{i}
            L = sorted(S,key= y,reverse=True)
            if len(self.nodes)>=1000:
                for i in range(0,int(len(self.e_o_n)/5)):
                    S.pop(L[i]) 
                    if len(S) <= k:
                        break
            else:
                S.pop(L[0])        
            nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}
            print(len(S))
        print(len(S))

        nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}
        return f(S)


    def LNC(self,i):
        H = 0
        if i not in self.edges_of_node:
            return 0
        di = len(self.edges_of_node[i]) #度数
        for j in self.get_neighbors(i):
            dj=len(self.edges_of_node[j])
            if (di+dj)>2: 
                weigh = (1-(self.nb_union(i,j)+1)/min(di,dj)) #计算权重
                H += weigh * (di-1)/(di+dj-2)
        return H
    
    def nb_union(self,i,j):
        num=0   
        nb1=self.get_neighbors(i)
        nb2=self.get_neighbors(j)
        for v in nb1 :
            for w in nb2:
                 if v == w:
                    num+=1
        return  num
        
    def get_neighbors(self, node):
        for e in self.edges_of_node[node]:
            if e[0][0] == e[0][1]: # a node is not neighbor with itself
                continue
            if e[0][0] == node:
                yield e[0][1]
            if e[0][1] == node:
                yield e[0][0]

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
