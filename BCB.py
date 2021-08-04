#!/usr/bin/env python3
import copy
import networkx as nx
import numpy as np
import gc
import operator
import random

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
            nodes[int(n[0])] = 1
            nodes[int(n[1])] = 1
            w = 1
            if len(n) == 3:
                w = int(n[2])
            edges.append(((int(n[0]), int(n[1])), w))
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
        self.edges_of_node = {}
        self.G = nx.Graph()
        self.G.add_nodes_from(range(len(self.nodes)))  
        for e in edges:
            self.G.add_edge(int(e[0][0]),int(e[0][1]))
            self.G.add_edge(int(e[0][1]),int(e[0][0]))
            # save edges by node
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
                self.edges_of_node[e[0][1]].append(e)
        self.bc= nx.centrality.betweenness_centrality(self.G,normalized=False)
        self.bcl = sorted(self.bc.items(), key=operator.itemgetter(1),reverse = True)
        self.e_o_n = copy.deepcopy(self.edges_of_node)
        # print(self.G.edges)

    def apply_method(self,z):
        #1 建立覆盖集
        S = []
        k = len(self.nodes)*z 
        for i in self.bcl:
            S.append(i[0])
            if len(S) >= k:
                    break

        S = {i:1 for i in S}

        
        def nb1(node): # neighbors
            for e in self.e_o_n[node]:
                if e[0][0] == node and e[0][1] not in S.keys()-{i}:
                    yield e[0][1]
                if e[0][1] == node and e[0][1] not in S.keys()-{i}:
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
                if v not in visited and v not in S:
                    id += 1 
                    cp[id]=[]
                    n = dfs(v)  
                    if n < 2:
                        continue
                    num += n*(n-1)/2

            return num

        print(len(S))

        nb={i:nb1(i) for i in self.e_o_n}
        return f(S)
        


