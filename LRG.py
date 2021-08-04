#!/usr/bin/env python3
import copy
import networkx as nx
import numpy as np
import gc

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
        # print(nodes, edges)
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
        # print("%d nodes, %d edges" % (len(nodes), len(edges)))
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
        # print("%d nodes, %d edges" % (len(nodes), len(edges)))
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
        self.edges_of_node = {}
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
        print(len(self.nodes),len(self.edges))

    def apply_method(self,z):
        #1 建立覆盖集
        S = {}
        k = len(self.nodes)*z
        num = 1  
        # print(k)
        # return 0

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

        def nb2(node): # neighbors
            nb1={}
            for e in self.e_o_n[node]:
                if e[0][0] == node and e[0][1] not in S:
                    nb1[e[0][1]]=1
                if e[0][1] == node and e[0][1] not in S:
                    nb1[e[0][0]]=1
            # print(len(nb1))
            return nb1
        
        NB={i:nb2(i) for i in self.e_o_n.keys()-S.keys()}

        def LR(i):
            num=0   #邻居个数
            if i not in self.e_o_n:
                return 0
            num+=len(NB[i]) #i的邻居
            for n1 in NB[i]:
                num+=len(NB[n1]) #邻居的邻居
                for n2 in NB[n1]:
                    num+=len(NB[n2]) #邻邻邻
                    for n3 in NB[n2]:
                        num+=len(NB[n3]) #四阶
                        # print(len(nb(n3)))
            # print(num)
            return num
        
        L = sorted(self.nodes,key= LR,reverse=True)
        while len(S) < k: # num相当于flag
            i=L.pop(0)
            S[L.pop(0)]=1 #选出最大的，加入S
            # print(i)

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




    # def nb(self, node):  #neighbor
    #     for e in self.edges_of_node[node]:
    #         if e[0][0] == e[0][1]: # a node is not neighbor with itself
    #             continue
    #         if e[0][0] == node:
    #             yield e[0][1]
    #         if e[0][1] == node:
    #             yield e[0][0]
