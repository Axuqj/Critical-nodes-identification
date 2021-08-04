#!/usr/bin/env python3

import math
import unittest
import time
from GCNP import PyLouvain
name='GCNP'
class PyGCNPTest(unittest.TestCase):
    
    # def test_RG(self):
    #     # WS
    #     Z=['250 1250 70','  500 1500 125',' 1000 5000 200',' 1500 4500 265']
    #     for z in Z:
    #         z=z.split()
    #         t0 = time.perf_counter()
    #         n = 2*int(z[1])/int(z[0])
    #         pyl = PyLouvain.from_WSgraph(int(z[0]),int(n),0.3)
    #         c = pyl.apply_method(int(z[2])/len(pyl.nodes))
    #         L = name+' '+'WS'+str(z[0])+str(z[2])+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
    #         f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data\\"+name+"2.txt", "a+")
    #         f.write(L+'\n')
    #         f.close()
    #         print(L)

        # # BA
        # Z=['500 499 50',' 1000 999 75']
        # # Z=['500 499 50',' 1000 999 75',' 2500 2499 100','5000 4999 150']
        # for z in Z:
        #     z=z.split()
        #     t0 = time.perf_counter()
        #     pyl = PyLouvain.from_BAgraph(int(z[0]),1)
        #     c = pyl.apply_method(int(z[2])/len(pyl.nodes))
        #     L = name+' '+'BA'+str(z[0])+str(z[2])+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
        #     f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data\\"+name+"2.txt", "a+")
        #     f.write(L+'\n')
        #     f.close()
        #     print(L)

        # # ER
        # Z=['235 349 50','465 699 80',' 940 1399 140']
        # # Z=['235 349 50','465 699 80',' 940 1399 140','2343 3499 200']
        # for z in Z:
        #     z=z.split()
        #     t0 = time.perf_counter()
        #     pyl = PyLouvain.from_ERgraph(int(z[0]),int(z[1]))
        #     c = pyl.apply_method(int(z[2])/len(pyl.nodes))
        #     L = name+' '+'ER'+str(z[0])+str(z[2])+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
        #     f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data\\"+name+"2.txt", "a+")
        #     f.write(L+'\n')
        #     f.close()
        #     print(L)

    def test_RN(self): 
        Z=[0.01,0.03,0.05,0.1,0.2]
        Y=[]
        for n in [0.4,0.8,1.2,1.6,2,2.4,2.8,3.2]:#八个
            Y.append(str(n/2)+'.dat')
            Y.append(str(n/2)+'_1.dat')
            Y.append(str(n/2)+'_2.dat')
            Y.append(str(n/2)+'_3.dat')
            Y.append(str(n/2)+'_4.dat')
        # Y = ["facebook.txt","social.txt","CA-GrQc.txt","p2p08.txt","p2p09.txt","arxiv.txt"]
        # Y = ["celegan.gml","Electronic_circuits.txt","yeast.txt","email.txt","karate.txt","lesmis.gml","polbooks.gml"]
        for y in Y:
            for z in Z:
                t0 = time.perf_counter()
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":
                    pyl = PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else:
                    pyl = PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                c = pyl.apply_method(z)
                f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data\\"+name+"4.txt", "a+")
                L = name+' '+y+'参数'+str(z)+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
                f.write(L+'\n')
                f.close()
                print(L)

    # def test_RN(self): 
    #     # Z=[0.1,0.2,0.01,0.3]
    #     # Z = [0.01,0.05,0.1,0.15,0.2,0.25,0.3]
    #     z=0.1
    #     Y=[]
    #     for n in [4,6,8]:
    #         Y.append(str(n)+'_.dat')
    #     # Y = ["facebook.txt","social.txt","CA-GrQc.txt","p2p08.txt","p2p09.txt","arxiv.txt"]
    #     # Y = ["celegan.gml","Electronic_circuits.txt","yeast.txt","email.txt","karate.txt","lesmis.gml","polbooks.gml"]
    #     for y in Y:
    #         t0 = time.perf_counter()
    #         if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":
    #             pyl = PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
    #         else:
    #             pyl = PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
    #         c = pyl.apply_method(z)
    #         f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data\\"+name+"5.txt", "a+")
    #         L = name+' '+y+'参数'+str(z)+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
    #         f.write(L+'\n')
    #         f.close()
    #         print(L)

    #  def test_SBM(self): 
    #     # Z=[0.1,0.2,0.01,0.3]
    #     # Z = [0.01,0.05,0.1,0.15,0.2,0.25,0.3]
    #     z=0.1
    #     Y=[]
    #     for n in [0.01,0.02,0.05,0.1]:
    #         Y.append(str(n)+'.dat')
    #     # Y = ["facebook.txt","social.txt","CA-GrQc.txt","p2p08.txt","p2p09.txt","arxiv.txt"]
    #     # Y = ["celegan.gml","Electronic_circuits.txt","yeast.txt","email.txt","karate.txt","lesmis.gml","polbooks.gml"]
    #     for y in Y:
    #         t0 = time.perf_counter()
    #         pyl = PyLouvain.from_file1("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
    #         c = pyl.apply_method(z)
    #         f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data\\"+name+"6.txt", "a+")
    #         L = name+' '+y+'参数'+str(z)+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
    #         f.write(L+'\n')
    #         f.close()
    #         print(L)

if __name__ == '__main__':
    unittest.main()

