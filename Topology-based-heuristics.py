

#!/usr/bin/env python3

import copy
import networkx as nx
import numpy as np

'''
    Implements the Louvain method.
    Input: a weighted undirected graph
    Ouput: a (partition, modularity) pair where modularity is maximum
'''
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
        nodes_, edges_ = in_order(nodes, edges)
        print("%d nodes, %d edges" % (len(nodes_), len(edges_)))
        return cls(nodes_, edges_)

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
                edges.append(((int(current_edge[0]), int(current_edge[1])), 1))
                current_edge = (-1, -1, 1)
                in_edge = 0
        nodes, edges = in_order(nodes, edges)
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
        self.k_i.append(0)
        self.edges_of_node = {}
        self.w = [0 for n in nodes]
        for e in edges:
            self.m += e[1]
            self.k_i[e[0][0]] += e[1]
            self.k_i[e[0][1]] += e[1] # there's no self-loop initially
            # save edges by node
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
        # access community of a node in O(1) time
        self.communities = [n for n in nodes]
        self.actual_partition = []
        # print(self.e_o_n)

    '''
        Applies the Louvain method.
    '''
    def apply_method(self,z):  #社区挖掘
        network = (self.nodes, self.edges)
        best_partition = [[node] for node in network[0]]
        best_q = -1
        i = 1
        k = len(self.nodes)*z  #参数为0.2
        # print(k)
        while 1: 
            #print("pass #%d" % i)
            i += 1
            partition = self.first_phase(network)
            q = self.compute_modularity(partition)
            partition = [c for c in partition if c]
            #print("%s (%.8f)" % (partition, q))
            # clustering initial nodes with partition
            if self.actual_partition:
                actual = []
                for p in partition:
                    part = []
                    for n in p:
                        part.extend(self.actual_partition[n])
                    actual.append(part)
                self.actual_partition = actual
            else:
                self.actual_partition = partition
            if q == best_q:
                break
            network = self.second_phase(network, partition)
            best_partition = partition
            best_q = q
        #得到actual_partition，为社区挖掘结果
        # print(best_q)
        # return 0
        #第二步 提取初始覆盖集
        S={}

        def nb1(node): # neighbors
            for e in self.e_o_n[node]:
                if e[0][0] == node and e[0][1] not in S:
                    yield e[0][1]
                if e[0][1] == node and e[0][1] not in S:
                    yield e[0][0]        
        
        nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}

        def f(S1,V): #计算V中除去S1后，的连通对数
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
                            if neighbour not in visited and neighbour not in S1 and neighbour in V: 
                                visited.append(neighbour) 
                                cp[id].append(neighbour) 
                                stack.append(neighbour)
                return len(cp[id])

            for v in V:
                if v not in visited and v not in S1:
                    id += 1 
                    cp[id]=[]
                    n = dfs(v)  
                    if n < 2:
                        continue
                    num += n*(n-1)/2
            return num


        def degree(i):  #适应性度数
            d = 0
            if i not in self.e_o_n:
                return 0
            for a in self.e_o_n[i]:
                if a[0][0] in S or a[0][1] in S:
                    continue
                d+=1
            return d

        for i in self.e_o_n: #find bridge
            if i not in S:
                for p in self.actual_partition:
                    if i in p and self.e_o_n[i]:
                        for e in self.e_o_n[i]:
                            a,b = e[0]
                        # print(self.e_o_n[i])
                        # print(a,b)
                            if a not in p and b not in S:
                                S[b] = 1 
                                S[a]=1
                            if b not in p and a not in S:
                                S[a] = 1  
                                S[b] = 1 
        
        # print(S)
        # print(k,len(S))
        np=len(self.actual_partition) #社区数量

        def degree(i):  #适应性度数
            d = 0
            if i not in self.e_o_n:
                return 0
            for a in self.e_o_n[i]:
                if a[0][0] in S or a[0][1] in S:
                    continue
                d+=1
            return d

        for p in self.actual_partition: #每个社区一定百分比 添加入S
            while 1:
                nump= len(p-S.keys())                
                if nump<len(p)*0.8:
                    break                
                max1 = max([degree(i) for i in p-S.keys()])


                if max1 == 0: #所有边都没有了
                    break
                for i in p:
                    if degree(i) == max1 and i not in S:
                        S[i]=1

        S2 = copy.deepcopy(S)
        # print(S2)
        k1=k/2

        best={i:(-1,-1) for i in range(np)}  #存储每个社区最优解
        # print(k,len(S2),nk)
        while len(S) < k:  #继续添加，每次添加一个点
            for p in range(np):  #更新最优解
                # print(1)
                id=-1
                min=100000
                if best[p][1] != -1:  #非空，则下一个
                    continue
                for a in self.actual_partition[p]: 
                    if a not in S:
                        b=f(S.keys()&{a},self.actual_partition[p]) 
                        if b<min:
                            id,min=a,b
                best[p]=(id,  f(S,self.actual_partition[p])-min ) #存储id和最大收益
                # print(best[p])

            id=-1
            max2=-1
            id1=-1                    
            for p in range(np): #筛选最优解
                if best[p][1]>max2:
                    id=best[p][0]
                    max2=best[p][1]
                    id1=p
            
            S[id]=1
            best[id1]=(-1,-1) #变成空，好更新

        while len(S) > k:  #每次删除一个点
            for n in range(np):
                npc=f(S,self.actual_partition[n]) #社区的连通对
                # print(S2)
                for i in self.actual_partition[n]:
                    if i in S:
                        #计算它的连通性增长量
                        j=f(S.keys()-{i},self.actual_partition[n]) 
                        best[i]=j-npc
                        # print(j-npc)
            id=-1
            min=100000
            # input()
            for k5,v in best.items():
                if k5 in S:
                    if v<min   :
                        min=v
                        id=k5
            if id !=-1:
                S.pop(id)


        Nk=30#迭代次数
        nk=0
        while nk<Nk:
            # print(str(nk)+'#')
            # print(k,len(S2))
            best={i:(-1,-1) for i in range(np)}  #存储每个社区最优解
            # print(k,len(S2),nk)
            while len(S2) < k:  #继续添加，每次添加一个点
                for p in range(np):  #更新最优解
                    # print(1)
                    id=-1
                    min=100000
                    if best[p][1] != -1:  #非空，则下一个
                        continue
                    for a in self.actual_partition[p]: 
                        if a not in S2:
                            b=f(S2.keys()&{a},self.actual_partition[p]) 
                            if b<min:
                                id,min=a,b
                    best[p]=(id,  f(S2,self.actual_partition[p])-min ) #存储id和最大收益
                    # print(best[p])

                id=-1
                max2=-1
                id1=-1                    
                for p in range(np): #筛选最优解

                    if best[p][1]>max2:
                        id=best[p][0]
                        max2=best[p][1]
                        id1=p
                
                S2[id]=1
                best[id1]=(-1,-1) #变成空，好更新

            if f(S2,self.e_o_n)<f(S,self.e_o_n):
                S=S2
                nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}
            nk+=1

            best={i:(-1,-1) for i in range(np)}
            while len(S2) < k+k1:  #继续添加，每次添加一个点
                for p in range(np):  #更新最优解
                    id=-1
                    min=100000
                    if best[p][1] != -1:  #非空，则下一个
                        continue
                    for a in self.actual_partition[p]: 
                        if a not in S2:
                            b=f(S2.keys()&{a},self.actual_partition[p]) 
                            if b<min:
                                id,min=a,b
                    best[p]=(id,  f(S2,self.actual_partition[p]) - min ) #存储id和最大收益
                id=-1
                max2=-1
                id1=-1
                # print(self.actual_partition)

                for p in range(np): #筛选最优解
                    if best[p][1]>max2:
                        id=best[p][0]
                        max2=best[p][1]
                        id1=p

                S2[id]=1
                best[id1]=(-1,-1) #变成空，好更新

            best={}

            while len(S2) > k:  #每次删除一个点

                for n in range(np):
                    npc=f(S2,self.actual_partition[n]) #社区的连通对
                    # print(S2)
                    for i in self.actual_partition[n]:
                        if i in S2:
                            #计算它的连通性增长量
                            j=f(S2.keys()-{i},self.actual_partition[n]) 
                            best[i]=j-npc
                            # print(j-npc)
                id=-1
                min=100000

                # input()
                for k5,v in best.items():
                    if k5 in S2:
                        if v<min   :
                            min=v
                            id=k5
                if id !=-1:
                    S2.pop(id)
                # print(id,best,S2,(id in S))
                # input()


            if f(S2,self.e_o_n)<f(S,self.e_o_n):
                S=S2

                nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}
            nk+=1  #n=2

            best={}
            while len(S2) > k-k1:  #每次删一个点
                for n in range(np):
                    npc=f(S2,self.actual_partition[n]) #社区的连通对
                    for i in self.actual_partition[n]:
                        if i in S2:
                            #计算它的连通性增长量
                            j=f(S2.keys()-{i},self.actual_partition[n]) 
                            best[i]=j-npc
                id=-1
                min=100000
                # print(best)
                for k5,v in best.items():
                    if k5 in S2:
                        if v<min   :
                            min=v
                            id=k5
                if id !=-1:
                    S2.pop(id)

        nb={i:nb1(i) for i in self.e_o_n.keys()-S.keys()}
        print(len(S))
        return f(S,self.e_o_n)



    '''
        Computes the modularity of the current network.
        _partition: a list of lists of nodes
    '''
    def compute_modularity(self, partition):
        q = 0
        m2 = self.m * 2
        for i in range(len(partition)):
            q += self.s_in[i] / m2 - (self.s_tot[i] / m2) ** 2
        return q

    '''
        Computes the modularity gain of having node in community _c.
        _node: an int
        _c: an int
        _k_i_in: the sum of the weights of the links from _node to nodes in _c
    '''
    def compute_modularity_gain(self, node, c, k_i_in):
        return 2 * k_i_in - self.s_tot[c] * self.k_i[node] / self.m

    '''
        Performs the first phase of the method.
        _network: a (nodes, edges) pair
    '''
    def first_phase(self, network):
        # make initial partition
        best_partition = self.make_initial_partition(network)
        while 1:
            improvement = 0
            for node in network[0]:
                if node not in self.edges_of_node:
                    continue
                node_community = self.communities[node]
                # default best community is its own
                best_community = node_community
                best_gain = 0
                # remove _node from its community
                if node in best_partition[node_community]:
                    best_partition[node_community].remove(node)
                best_shared_links = 0
                
                for e in self.edges_of_node[node]:
                    if e[0][0] == e[0][1]:
                        continue
                    if e[0][0] == node and self.communities[e[0][1]] == node_community or e[0][1] == node and self.communities[e[0][0]] == node_community:
                        best_shared_links += e[1]
                self.s_in[node_community] -= 2 * (best_shared_links + self.w[node])
                self.s_tot[node_community] -= self.k_i[node]
                self.communities[node] = -1
                communities = {} # only consider neighbors of different communities
                for neighbor in self.get_neighbors(node):
                    community = self.communities[neighbor]
                    if community in communities:
                        continue
                    communities[community] = 1
                    shared_links = 0
                    for e in self.edges_of_node[node]:
                        if e[0][0] == e[0][1]:
                            continue
                        if e[0][0] == node and self.communities[e[0][1]] == community or e[0][1] == node and self.communities[e[0][0]] == community:
                            shared_links += e[1]
                    # compute modular
                    # ity gain obtained by moving _node to the community of _neighbor
                    gain = self.compute_modularity_gain(node, community, shared_links)
                    if gain > best_gain:
                        best_community = community
                        best_gain = gain
                        best_shared_links = shared_links
                # insert _node into the community maximizing the modularity gain
                best_partition[best_community].append(node)
                self.communities[node] = best_community
                self.s_in[best_community] += 2 * (best_shared_links + self.w[node])
                self.s_tot[best_community] += self.k_i[node]
                if node_community != best_community:
                    improvement = 1
            if not improvement:
                break
        return best_partition

    '''
        Yields the nodes adjacent to _node.
        _node: an int
    '''
    def get_neighbors(self, node):
        for e in self.edges_of_node[node]:
            if e[0][0] == e[0][1]: # a node is not neighbor with itself
                continue
            if e[0][0] == node:
                yield e[0][1]
            if e[0][1] == node:
                yield e[0][0]

    def get_neighbor(self, node):
        for e in self.e_o_n[node]:
            if e[0][0] == e[0][1]: # a node is not neighbor with itself
                continue
            if e[0][0] == node:
                yield e[0][1]
            if e[0][1] == node:
                yield e[0][0]

    '''
        Builds the initial partition from _network.
        _network: a (nodes, edges) pair
    '''
    def make_initial_partition(self, network):
        partition = [[node] for node in network[0]]
        self.s_in = [0 for node in network[0]]
        self.s_in.append(0)
        self.s_tot = [self.k_i[int(node)] for node in network[0]]
        self.s_tot.append(0)
        for e in network[1]:
            if e[0][0] == e[0][1]: # only self-loops
                self.s_in[e[0][0]] += e[1]
                self.s_in[e[0][1]] += e[1]
        return partition

    '''
        Performs the second phase of the method.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def second_phase(self, network, partition):
        nodes_ = [i for i in range(len(partition))]
        # relabelling communities
        communities_ = []
        d = {}
        i = 0
        for community in self.communities:
            if community in d:
                communities_.append(d[community])
            else:
                d[community] = i
                communities_.append(i)
                i += 1
        self.communities = communities_
        # building relabelled edges
        edges_ = {}
        for e in network[1]:
            ci = self.communities[e[0][0]]
            cj = self.communities[e[0][1]]
            try:
                edges_[(ci, cj)] += e[1]
            except KeyError:
                edges_[(ci, cj)] = e[1]
        edges_ = [(k, v) for k, v in edges_.items()]
        # recomputing k_i vector and storing edges by node
        self.k_i = [0 for n in nodes_]
        self.edges_of_node = {}
        self.w = [0 for n in nodes_]
        for e in edges_:
            self.k_i[e[0][0]] += e[1]
            self.k_i[e[0][1]] += e[1]
            if e[0][0] == e[0][1]:
                self.w[e[0][0]] += e[1]
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
                self.edges_of_node[e[0][1]].append(e)
        # resetting communities
        self.communities = [n for n in nodes_]
        return (nodes_, edges_)

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
