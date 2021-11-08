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

with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
    Rresult = pickle.load(f)
# Name=['Random','OCH','TBH','GCNP','BCB','HCH','KSBG','LRBG','SG']
Name=['Random' ,'TBH','GCNP','BCB','HCH','KSBG','LRBG','SG']
Y = ["celegan.gml","Electronic_circuits.txt","yeast.txt","email.txt","polbooks.gml","karate.txt","lesmis.gml"]
# Y = ["karate.txt","lesmis.gml"]
Y1=["celegan","Electronic_circuits","yeast","email","polbooks","karate","lesmis"]
# Y1=["karate","lesmis"]

#指定默认字体
matplotlib.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['font.family']='sans-serif'
Z = [0.01,0.05,0.1,0.15,0.2,0.25,0.3]
# Z = [0.01,0.05]


reslut={'OCH':{'celegan':(39060 ,35245 ,30382 ,25879 ,20709 ,16318 ,7003 ),
    'Electronic_circuits':(121304,38025,14885,5514,2498,1087,553),
    'yeast':(137791,30005,2294,332,46,15,7),
    'email':(605550,507535,405473,319629,231204,142172 ,72849 )},

'GCNP':{'email':(627760,578350,518671,463203,409965,359976,314028),
},

'TBH':{'email':(608856,505537,394765,309333,217559,128382,73583 ),
}

}


def real(name):
    for y in Y:
        for i in range(len(Y)):
            if y==Y[i]: Rresult[name][Y1[i]]=list(0 for z in range(len(Z)))
        for z in range(len(Z)):    #输入算法名称
            t0 = time.perf_counter()
            if name=='OCH' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = OCH.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = OCH.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='TBH' :
                if y=='email.txt': continue
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = TBH.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = TBH.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)   
                c = pyl.apply_method(Z[z])         
            if name=='GCNP' :
                if y=='email.txt': continue
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = GCNP.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = GCNP.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='BCB' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = BCB.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = BCB.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='KSBG' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = KSBG.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = KSBG.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='LRBG' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = LRBG.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = LRBG.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='SG' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = SG.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = SG.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='HCH' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = HCH.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = HCH.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y) 
                c = pyl.apply_method(Z[z])
            if name=='Random' :
                if y=="lesmis.gml" or y=="polbooks.gml" or y=="celegan.gml":pyl = Random.PyLouvain.from_gml_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)
                else: pyl = Random.PyLouvain.from_file("C:\\Users\\xqjwo\\Desktop\\dataset\\"+y)   
                c = pyl.apply_method(Z[z])             
            
            for i in range(len(Y)):
                if y==Y[i]: Rresult[name][Y1[i]][z]=c
            L = name+' '+y+'参数'+str(z)+' '+str(int(c))+' '+str(int(time.perf_counter() - t0))
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
    f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\real_connectivity.txt", "a+")
    f.write(L+'\n')
    f.close()
    
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
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
    f = open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\real_connectivity.txt", "a+")    #
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
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
        Rresult = pickle.load(f)
    M=[]
    N=[]
    r=[]   
    inum=0  #m跟i对标，n跟j对标
    # print(Rresult)
    for i in Rresult: #遍历算法 Rresult[i]代表一种算法random，Rresult[i][j]代表一个算法的结果
        if i !='Random':
            M+=[[]]
            inum+=1
        for j in Rresult[i]: # 遍历一算法的每个网络 Rresult[i]=random 表示random有多少个网络
            if i =='Random':
                r+=[Rresult[i][j][0], Rresult[i][j][1]]
                # r+=[Rresult[i][j][2], Rresult[i][j][6]]  #存储random的每个值，生成[1,2,3,4,5,6,] 取0.1 0.3
                continue
            M[inum-1]+= [Rresult[i][j][0], Rresult[i][j][1]]
            # M[inum-1]+= [Rresult[i][j][2], Rresult[i][j][6]] #M[m]表示第m个算法的所有值 [ [1,2,3,4,5], [1,2,3,4,5]]
        N=[i for i in M if len(i)!=0]
        if i =='Random':continue  #random不参与百分比计算
        for p in range(len(M[inum-1])):
            num=round(100*(r[p]-M[inum-1][p])/r[p] ,2 )
            N[inum-1][p]=num
            if num<0:N[inum-1][p]=  0
    
    K= [list(d) for d in np.transpose(N)]
    index1=[[i+'1',i+'2'] for i in Y1]
    Name1=[i for i in Name if i !='Random']
    index1=[i  for j in index1 for i in j  ]
    # print(K)
    matplotlib.rcParams['axes.unicode_minus'] = False
    df = pd.DataFrame(K,
                    index=index1,
                    columns=pd.Index(Name1),
                    )

    df.plot(kind='barh') #,figsize=(5,8)

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.legend(loc="best")
    plt.xlabel("The relative error")
    plt.ylabel("Networks")
    plt.savefig('C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\real_random.pdf',
                bbox_inches='tight',
                dpi=400,
                )
    plt.show()

def pp():   #性能概况
    M1=[]       
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
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
    
    plt.legend()#绘制图例
    plt.xlabel('n')
    plt.ylabel('P(n)')

    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    plt.xlim(0,n[-1])
    plt.ylim(0,1.0)

    plt.savefig('C:\\Users\\xqjwo\\Desktop\\real_pp.pdf',#'C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\real_pp.pdf'
                bbox_inches='tight',
                dpi=300,
                )
    plt.show()


def lines():
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
        Rresult = pickle.load(f)

    M1=[ [ [[] for z in range(len(Z))]   for j in range(len(Y))  ]    for i in range(len(Name)-1) ] 
    # M1=[ [ [[] for z in range(len(Z))]   for j in range(4)  ]    for i in range(len(Name)-1) ]   
    inum=0
    for i in Rresult: #遍历算法 i 代表算法，Rresult[i]代表算法对应的结果，Rresult[i][j]代表一个算法的结果
        if i =='Random':continue #不输入random
        inum+=1
        jnum=0
        for j in Rresult[i]: # 遍历一算法的每个网络
            M1[inum-1][jnum]=Rresult[i][j]  #[[[]][]] 三维。。
            jnum+=1
            if jnum==len(Y):break  #只选取前四个网络图像

    markers=['.','o' ,'+'  ,'^', '*','x' ,'' ,'' ]
    colors=['b','g','r','c','m','y','k','r','g']

    print(M1)
    #画图
    plt.figure(22,figsize=(10.0, 10.0)) #
    for i in range(len(Y)):
        if i >= 4:break
        plt.subplot(2,2,i+1)
        for d in range(len(Name)-1):
            plt.plot(Z,#x轴方向变量
                    M1[d][i],
                    # interpolate.interp1d(Z,M1[d][i],kind='cubic')(Z),#y轴方向变量
                    color=colors[d],#线和marker的颜色random.choice(colors)
                    marker=markers[d],#marker形状random.choice(markers)
                    label=Name[d+1],#图例
                    )
        plt.legend()#绘制图例
        plt.xlabel(Y1[i])
        plt.ylabel('The value of optical fuction')

    plt.savefig('C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\real_lines.pdf',
                    bbox_inches='tight',
                    dpi=600,
                    )
    plt.show()

def line():
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
        Rresult = pickle.load(f)


    
    for i in Rresult: #遍历算法 i 代表算法，Rresult[i]代表算法对应的结果，Rresult[i][j]代表一个算法的结果
        jnum=0
        if i =='Random':continue #不输入random
        for j in Rresult[i]: # 遍历一算法的每个网络
            print(i+str(jnum)+'='+str(Rresult[i][j]))
            jnum+=1


    

def experiment():
    Rresult={name:{Y1[0]:()}  for name in Name}#存储结果
    for name in Name:
        real(name)
    with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "wb") as f:
        pickle.dump(Rresult, f)    
    print(Rresult)

def draw():
    connectivity()
    # Rd()
    # pp()
    # lines()
    line()


if __name__ == "__main__":
    # experiment()#运行，写入文件
    draw()#读取文件，画图

#     Rresult={'Random': {'celegan': [43071.0, 39621.0, 35511.0, 29403.0, 27028.0, 24310.0, 19900.0], 'Electronic_circuits': [127765.0, 117370.0, 104653.0, 53785.0, 70160.0, 61449.0, 52023.0], 'yeast': [214210.0, 194399.0, 162772.0, 118858.0, 119835.0, 95716.0, 38950.0], 'email': [626640.0, 565516.0, 506521.0, 441331.0, 379758.0, 322005.0, 285391.0], 'polbooks': [5253.0, 4851.0, 4371.0, 3916.0, 3322.0, 3003.0, 2485.0], 'karate': [528.0, 496.0, 435.0, 378.0, 351.0, 300.0, 231.0], 'lesmis': [2850.0, 2628.0, 2346.0, 1892.0, 1596.0, 1378.0, 1275.0]}, 
# 'TBH': {'celegan': [39060.0, 34717.0, 29891.0, 25201.0, 21119.0, 17768.0, 10345.0], 'Electronic_circuits': [124254.0, 52573.0, 14169.0, 6034.0, 1808.0, 912.0, 530.0], 'yeast': [130366.0, 30268.0, 663.0, 211.0, 40.0, 20.0, 7.0], 'email': [608856,505537,394765,309333,217559,128382,73583], 'polbooks': [5253.0, 4851.0, 4186.0, 3181.0, 3003.0, 973.0, 413.0], 'karate': [361.0, 335.0, 200.0, 130.0, 21.0, 30.0, 3.0], 'lesmis': [1875.0, 1233.0, 661.0, 227.0, 100.0, 92.0, 35.0]}, 
# 'GCNP': {'celegan': [43071.0, 39621.0, 35511.0, 31626.0, 27966.0, 24531.0, 21321.0], 'Electronic_circuits': [127765.0, 117855.0, 105570.0, 94395.0, 83436.0, 73536.0, 63903.0], 'yeast': [218806.0, 212226.0, 190653.0, 169072.0, 149879.0, 131842.0, 114482.0], 'email': [627760,578350,518671,463203,409965,359976,314028], 'polbooks': [5253.0, 4851.0, 4371.0, 3916.0, 3486.0, 3003.0, 2628.0], 'karate': [528.0, 496.0, 435.0, 378.0, 351.0, 300.0, 253.0], 'lesmis': [2850.0, 2628.0, 2346.0, 2080.0, 1830.0, 1596.0, 1378.0]}, 
# 'BCB': {'celegan': [40186.0, 34981.0, 31126.0, 27262.0, 23654.0, 20101.0, 16657.0], 'Electronic_circuits': [127765.0, 115450.0, 91866.0, 29834.0, 7749.0, 5515.0, 1635.0], 'yeast': [137611.0, 33518.0, 3432.0, 599.0, 213.0, 111.0, 66.0], 'email': [619941.0, 528906.0, 427354.0, 343223.0, 261739.0, 191310.0, 121367.0], 'polbooks': [5253.0, 4851.0, 4371.0, 3409.0, 3009.0, 2287.0, 639.0], 'karate': [361.0, 335.0, 83.0, 61.0, 31.0, 28.0, 19.0], 'lesmis': [1875.0, 1488.0, 584.0, 195.0, 145.0, 66.0, 51.0]}, 
# 'HCH': {'celegan': [40186.0, 34981.0, 31126.0, 27262.0, 23654.0, 20101.0, 16657.0], 'Electronic_circuits': [127765.0, 115450.0, 91866.0, 29834.0, 7749.0, 5515.0, 1635.0], 'yeast': [137611.0, 33518.0, 3432.0, 599.0, 213.0, 111.0, 66.0], 'email': [619941.0, 528906.0, 427354.0, 343223.0, 261739.0, 191310.0, 121367.0], 'polbooks': [5253.0, 4851.0, 4371.0, 3409.0, 3009.0, 2287.0, 639.0], 'karate': [361.0, 335.0, 83.0, 61.0, 31.0, 28.0, 19.0], 'lesmis': [1875.0, 1488.0, 584.0, 195.0, 145.0, 66.0, 51.0]}, 
# 'KSBG': {'celegan': [43365.0, 39903.0, 35778.0, 29647.0, 26107.0, 22792.0, 19702.0], 'Electronic_circuits': [129286.0, 119316.0, 106030.0, 92235.0, 74336.0, 54049.0, 44346.0], 'yeast': [201530.0, 122674.0, 79275.0, 23368.0, 13703.0, 609.0, 2543.0], 'email': [634501.0, 582660.0, 501502.0, 415418.0, 336614.0, 269753.0, 198790.0], 'polbooks': [5356.0, 4950.0, 4465.0, 3916.0, 3004.0, 3003.0, 2556.0], 'karate': [561.0, 528.0, 496.0, 435.0, 435.0, 406.0, 351.0], 'lesmis': [2926.0, 2701.0, 2415.0, 2145.0, 1891.0, 1596.0, 1083.0]}, 
# 'LRBG': {'celegan': [43071.0, 39340.0, 35245.0, 31375.0, 27730.0, 24310.0, 21115.0], 'Electronic_circuits': [127765.0, 112595.0, 89788.0, 76324.0, 63266.0, 55999.0, 42292.0], 'yeast': [214210.0, 163933.0, 118884.0, 86792.0, 64730.0, 48318.0, 41463.0], 'email': [619941.0, 552826.0, 471907.0, 404553.0, 342381.0, 289184.0, 230208.0], 'polbooks': [5253.0, 4851.0, 4371.0, 3916.0, 3486.0, 3003.0, 2628.0], 'karate': [528.0, 351.0, 300.0, 253.0, 210.0, 190.0, 171.0], 'lesmis': [1875.0, 1641.0, 1423.0, 1221.0, 796.0, 643.0, 513.0]}, 
# 'SG': {'celegan': [40470.0, 37128.0, 30877.0, 27262.0, 23654.0, 19901.0, 16837.0], 'Electronic_circuits': [128271.0, 104256.0, 40718.0, 25501.0, 2070.0, 1001.0, 761.0], 'yeast': [125812.0, 14822.0, 376.0, 82.0, 47.0, 34.0, 25.0], 'email': [621055.0, 541320.0, 450778.0, 370235.0, 280147.0, 207724.0, 129919.0], 'polbooks': [5356.0, 4950.0, 4465.0, 3828.0, 3082.0, 841.0, 514.0], 'karate': [561.0, 361.0, 200.0, 45.0, 39.0, 15.0, 14.0], 'lesmis': [2926.0, 1532.0, 732.0, 594.0, 369.0, 121.0, 71.0]}
# }
#     with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "wb") as f:
#         pickle.dump(Rresult, f)    
    # with open("C:\\Users\\xqjwo\\Desktop\\dataset\\experiment_data1\\realresult.txt", "rb") as f:
    #     Rresult = pickle.load(f)
    # print(Rresult)


