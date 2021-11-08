import random
import OCH
import TBH
import numpy as np
import sys
import GCNP
import math
import Random
import matplotlib.pyplot as plt 
import BCB
import KSBG
import LRBG
import SG
import HCH
from scipy import interpolate
import time
import pickle
import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['font.family']='sans-serif'
#Name=['Random','OCH','TBH','GCNP','BCB','HCH','KSBG','LRBG','SG']
Name=['Random','TBH','GCNP','BCB','HCH','KSBG','LRBG','SG']
# Name=['Random','LRBG','SG']
Rresult={name:{'WS':[]}  for name in Name}#存储结果
# Y = {'WS':['250 1250 70','  500 1500 125'],
#     'BA':['500 499 50',' 1000 999 75'],
#     'ER':['235 349 50','465 699 80']}
Y = {'WS':['250 1250 70','500 1500 125','1000 5000 200'],
    'BA':['500 499 50','1000 999 75','1500 1499 100'],
    'ER':['235 349 50','465 699 80','940 1399 140']}

result={'OCH':{'WS':(15579,58083,319600,), 'BA':(302,958,2012), 'ER':(3230,30419,142082)} ,
 'TBH':{'WS':(16110,63204,319600), 'BA':(293,909,1568), 'ER':(1035,22165,123268)} }

def BA_ER(name):
    for y1 in Y:
        Rresult[name][y1]=list(0 for n in range(len(Y[y1])))  #生成 result={'TBH':{'WS':(), '':()}}
        for y2 in range(len(Y[y1])):  #y2是序号0123； y3是点边如'250 1250 70'
            y3= Y[y1][y2].split()   
            t0 = time.perf_counter()
            if name=='OCH' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = OCH.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = OCH.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = OCH.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='TBH' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = TBH.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = TBH.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = TBH.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))      
            if name=='GCNP' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = GCNP.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = GCNP.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = GCNP.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='BCB' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = BCB.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = BCB.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = BCB.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='KSBG' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = KSBG.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = KSBG.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = KSBG.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='LRBG' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = LRBG.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = LRBG.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = LRBG.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='SG' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = SG.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = SG.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = SG.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='HCH' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = HCH.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = HCH.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = HCH.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
            if name=='Random' :
                if y1=='WS':
                    n = 2*int(y3[1])/int(y3[0])  #连边概率
                    pyl = Random.PyLouvain.from_WSgraph(int(y3[0]),int(n),0.3)
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='BA': 
                    pyl = Random.PyLouvain.from_BAgraph(int(y3[0]),1) 
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))
                if y1=='ER':
                    pyl = Random.PyLouvain.from_ERgraph(int(y3[0]),int(y3[1]))
                    c = pyl.apply_method(int(y3[2])/len(pyl.nodes))                                                        
            Rresult[name][y1][y2]=c #result={'TBH':{'WS':(), '':()}}

            L = name+' '+y1+str(y3[0])+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
            f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\test.txt", "a+")
            f.write(L+'\n')
            f.close()

def connectivity():        #连通节点对 表示算法name在网络y的第i个参数的结果是c：result={'CBG':{'network1': (1,2,3), '':()}, ''   }
    L=''  
    for n in range(len(Name)):
        if Name[n] =='Random':continue
        L+=Name[n]
        if n!=len(Name)-1 : L+=' & ' 
        else: L+=' \\\\'
    f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BA_connectivity.txt", "a+")
    f.write(L+'\n')
    f.close()
    
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BAresult.txt", "rb") as f:
        Rresult = pickle.load(f)
    print(Rresult)
    M1=[]       
    inum=0
    for i in Rresult: #遍历算法 i 代表算法，Rresult[i]代表算法对应的结果，Rresult[i][j]代表一个算法的结果
        if i =='Random':continue #不输入random
        M1+=[[]] 
        inum+=1
        for j in Rresult[i]: # 遍历一算法的每个网络
            M1[inum-1]+=Rresult[i][j]
    K=np.transpose(M1) 
    f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BA_connectivity.txt", "a+")    #
    for i in K:
        L=''
        mini=min(i)
        for j in range(len(i)):
            if i[j]==mini: L+= '\\textbf{' + str(int(i[j]))+'}'
            else:L+=str(int(i[j]))
            if j!=len(i)-1 : L+=' & ' 
            else: L+=' \\\\'
        f.write(L+'\n')
    f.close()

def Rd():
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BAresult.txt", "rb") as f:
        Rresult = pickle.load(f)

    M=[]
    N=[]
    r=[]   
    inum=0  #m跟i对标，n跟j对标
    for i in Rresult: #遍历算法 Rresult[i]代表一种算法random，Rresult[i][j]代表一个算法的结果
        if i !='Random':
            M+=[[]]
            inum+=1
        for j in Rresult[i]: # 遍历一算法的每个网络 Rresult[i]=random 表示random有多少个网络
            if i =='Random'or j=='WS':
                r+=[Rresult[i][j][0], Rresult[i][j][1],Rresult[i][j][2]]  #存储random的每个值，生成[1,2,3,4,5,6,]
                continue
            M[inum-1]+= [Rresult[i][j][0], Rresult[i][j][1],Rresult[i][j][2]]
            # M[inum-1]+= [Rresult[i][j][2], Rresult[i][j][6]] #M[m]表示第m个算法的所有值 [ [1,2,3,4,5], [1,2,3,4,5]]
        N=[i for i in M if len(i)!=0]
        if i =='Random'or j=='WS':continue  #random不参与百分比计算
        for p in range(len(M[inum-1])):
            num=round(100*(r[p]-M[inum-1][p])/r[p] ,3 )
            N[inum-1][p]=num
            if num<0:N[inum-1][p]=  0
            # if num<100: num=num*100
    
    K= [list(d) for d in np.transpose(N)]
    index1=[[],[]]
    for i in Y:
        if i =='BA':
            for y in Y[i]:
                index1[0]+= [i+y.split()[0]]
        if i =='ER':
            for y in Y[i]:
                index1[1]+= [i+y.split()[0]]
    print(Rresult)
    
    Name1=[i for i in Name if i !='Random' ]
    # print(Name1)
    index1=[i  for j in index1 for i in j  ]
    # print(N)
    # sys.exit()
    matplotlib.rcParams['axes.unicode_minus'] = False
    df = pd.DataFrame(K,
                    index=index1,
                    columns=pd.Index(Name1),
                    )

    df.plot(kind='barh') #,figsize=(5,8)

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.legend(loc="upper left")
    plt.xlabel("The relative error")
    plt.ylabel("Networks")
    plt.savefig('C:\\Users\\xqjwo\\Desktop\\BA_random.pdf',#C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BA_random.pdf
                bbox_inches='tight',
                dpi=400,
                )
    plt.show()



def pp():   #性能概况
    M1=[]       
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BAresult.txt", "rb") as f:
        Rresult = pickle.load(f)
    m=0
    for i in Rresult: #遍历算法 i 代表算法，Rresult[i]代表算法对应的结果，Rresult[i][j]代表一个算法的结果
        if i =='Random':continue #不输入random
        M1+=[[]] 
        m+=1 
        for j in Rresult[i]: # 遍历一算法的每个网络
            M1[m-1]+=Rresult[i][j]
    
    # print(M1)
    best=[min(m) for m in np.transpose(M1)]   #最优值集合
    # print(best)
    
    inum=len(best) #案例个数 
    M2=M1.copy()
    for i in range(len(M1)):
        M2[i]=[round(math.log(M1[i][j]/best[j],2) , 2)  for j in range(len(M1[i])) ]  #转化成log2(T/best)，后面就很好算。。
    nmax=np.max(M2)

    M3=[[0 for i in range(100)] for j in range(len(M2))]  #M3[i]就是每个算法的p（n）
    for i in range(len(M2)): #m是算法如cbg的序号
        for j in range(0,100):
            M3[i][j]= round(np.sum(np.array(M2[i])<=j*nmax/100)/len(M2[i]),2) #大于当下n的多少，也就是p（n)!!!
    
    # lines=['-','--' , '-.']
    markers=['.','o' ,'+'  ,'^', '*','x' ,''  ]
    colors=['b','g','r','c','m','y','k','r']

    n=[i*nmax/100 for i in range(100) ]
    
    for d in range(len(Name)-1):
        plt.plot(n,#x轴方向变量
                interpolate.interp1d(n,M3[d],kind='cubic')(n),#y轴方向变量
                # linestyle=random.choice(lines),#线型
                color=colors[d],#线和marker的颜色random.choice(colors)
                # marker=markers[d],#marker形状random.choice(markers)
                label=Name[d+1],#图例
                )
    
    plt.legend(loc="best")#绘制图例
    plt.xlabel('n')
    plt.ylabel('P(n)')

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    plt.xlim(0,n[-1])

    plt.savefig('C:\\Users\\xqjwo\\Desktop\\BA_pp.pdf',#'C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BA_pp.pdf'
                bbox_inches='tight',
                dpi=300,
                )
    plt.show()

def experiment():
    for name in Name:
        BA_ER(name)
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BAresult.txt", "wb") as f:
        pickle.dump(Rresult, f)    
    print(Rresult)

def draw():
    # connectivity()
    # Rd()
    pp()

if __name__ == "__main__":
    # experiment()#运行，写入文件
    draw()#读取文件，画图

#     Rresult={'Random': {'WS': [16110.0, 70125.0, 319600.0], 'BA': [73177.0, 337550.0, 673191.0], 'ER': [12251.0, 57977.0, 256698.0]}, 
# 'TBH':{'WS':[16110,63204,319600], 'BA':[293,909,1568], 'ER': [1035,22165,123268 ] },
# 'GCNP': {'WS': [16110.0, 70125.0, 319600.0], 'BA': [83845.0, 369370.0, 887778.0], 'ER': [15931.0, 66430.0, 296835.0]}, 
# 'BCB': {'WS': [16110.0, 70125.0, 319600.0], 'BA': [269.0, 793.0, 1413.0], 'ER': [6018.0, 43426.0, 195094.0]}, 
# 'HCH': {'WS': [16110.0, 70125.0, 319600.0], 'BA': [259.0, 775.0, 1701.0], 'ER': [6832.0, 37757.0, 226156.0]}, 
# 'KSBG': {'WS': [15931.0, 70125.0, 319600.0], 'BA': [23260.0, 5359.0, 10716.0], 'ER': [10599.0, 56956.0, 237742.0]}, 
# 'LRBG': {'WS': [16110.0, 69751.0, 319600.0], 'BA': [11699.0, 37192.0, 69537.0], 'ER': [8691.0, 52683.0, 224831.0]}, 
# 'SG': {'WS': [16290.0, 70125.0, 320400.0], 'BA': [255.0, 773.0, 1713.0], 'ER': [1315.0, 23292.0, 137340.0]}}
#     with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BAresult.txt", "wb") as f:
#         pickle.dump(Rresult, f) 

    # with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\BAresult.txt", "rb") as f:
    #     Rresult = pickle.load(f)
    # print(Rresult)