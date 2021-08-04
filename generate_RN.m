function generate_RN(zout)
% function [M]=generate_RN(zout)
% clear,clc;
% close all;
%%%%%%%%%%%%%%%%%%%%%%%
C=4;  社区
s=32; 节点
d=16; 平均度数
zout=8;
testf=strcat('D:\mprogram\EM\vbmod\data\128_16_8_5.dat');%输出文件
%%%%%%%%%%%%%%%%%%%%%%%
pout=zout/d;
pin=1-pout;
p1=d*pin/(s-1);
p2=d*pout/(C-1)/s;
n=C*s;
% M=zeros(n,n);
M=sparse(n,n);
for i=1:n
    for j=i+1:n
        if just(i,j,s)==1
            if rand()<=p1
                M(i,j)=1;
                M(j,i)=1;
            end
        else
           if rand()<=p2
                M(i,j)=1;
                M(j,i)=1;
           end 
        end
    end
end
 show_matrix(M,'hehe');
 outfile(M,testf);
function outfile(g_A,filename)
edges=0;
n=0;
for i=1:length(g_A)
    for j=i+1:length(g_A)
        if g_A(i,j)==1
            n=n+1;
            edges(n,1)=i;
            edges(n,2)=j;
        end
    end
end
sum(sum(g_A))
%  网络文件转换的邻接矩阵输出到文件 
dlmwrite(filename,edges,'delimiter',' ','-append');
 
function r=just(i,j,s)
a=floor((i-1)/s);
b=floor((j-1)/s);
if abs(a-b)<1.0e-6
    r=1;
else
    r=0;
end
    
function show_matrix(A,str) 
  figure(...
  'Color',[1 1 1],...
  'Name',str); 
  clf;
%   imagesc(A);
  spy(A);
  colorbar;  
  set(gca,'fontsize',20);
  xlabel('Nodes','fontsize',20);
  ylabel('Nodes','fontsize',20);
