function generate_SBM(Groups,P_adj)
% function [Adj,Z]=generate_SBM(Groups,P_adj)
% generate_SBM��[10 20 30],[0.5 0.01 0.01,0.02 0.5 0.01,0.01 0.01 0.5]��
% ���ݿ����Ӹ�������������ڽӾ���,ֻ����������;
% ���룺
% Groups��һ����ڵ��������飬Ԫ����ĿΪ����Ŀ�����ÿ��Ԫ�ص�ֵΪ��Ӧ��Ľڵ�����;
% P_adj�ǿ����Ӹ��ʾ���ָ��������������Ӹ���
% �����
% Adj������������ڽӾ���
% Z�ڵ�Ŀ�ָʾ����
%%%%%%%%%%%%%%%%%%%%%%%
c=4;
s=32;
%���ɿ����Ӹ��ʾ���
Groups=ones(c,1)*s;
pin=0.5;
pout=0.001;
P_adj=zeros(length(Groups),length(Groups));
for i=1:length(Groups);
    for j=1:length(Groups)
        if i==j
            P_adj(i,j)=pin;
        else
            P_adj(i,j)=pout;
        end
    end
end
P_adj(3,3)=pout;P_adj(4,4)=pout;
P_adj(4,3)=pin;P_adj(3,4)=pin;
%%��������ɽ���


% P_adj(6,6)=pout;P_adj(7,7)=pout;P_adj(8,8)=pout;
% P_adj(6,7)=pin;P_adj(7,6)=pin;
% P_adj(6,8)=pin;P_adj(8,6)=pin;
% P_adj(7,8)=pin;P_adj(8,7)=pin;

for h=1:1
    testf=strcat('E:\mprogram\graph\Generate_Graph\data\192_',num2str(pout),'.dat');%����ļ�strcat('data/test_',num2str(h),'.dat');
    testf1=strcat('E:\mprogram\graph\Generate_Graph\data\192_',num2str(pout),'_A.dat');%����ļ�strcat('data/test_',num2str(h),'.dat');
    testf3=strcat('E:\mprogram\graph\Generate_Graph\data\192_unorder',num2str(pout),'_A.dat');%����˳����ڽӾ���;
    testf2=strcat('E:\mprogram\graph\Generate_Graph\data\192_c.dat');%����ļ�
    num=sum(Groups);%�õ��ڵ�����Ŀ
    k=length(Groups);%�õ�����Ŀ���
    A=rand(num,num);%������Ӧ��С�����������
    A=speye(num,num);
    for i=1:k
        for j=i:k
            A1=rand(s,s);
            A1(A1<=P_adj(i,j))=-1;
            A1(A1>P_adj(i,j))=0;
            A1=-A1;
            A((i-1)*s+1:i*s,(j-1)*s+1:j*s)=A1;
        end
    end
%     pos=0;%����ʼλ��
%     pos2=0;
%     for i=1:k
%         if i-1==0
%             pos=pos+1;
%         else
%             pos=pos+Groups(i-1);
%         end
%         pos2=pos;
%         for j=i:k
%             if j==i
%                 pos2=pos2;
%             else
%                 pos2=pos2+Groups(j-1);
%             end
%             p=P_adj(i,j);%�õ�������Ӹ���        
%             if i==j
%                 for ii=pos:pos+Groups(i)-1
%                     for jj=ii:pos+Groups(i)-1
%                         if ii==jj
%                             A(ii,jj)=0;
%                         else
%                             if A(ii,jj)<p
%                                 A(ii,jj)=1;
%                             else
%                                 A(ii,jj)=0;
%                             end
%                         end
%                     end
%                 end
%             end
%             if i<j
%                 for ii=pos:pos+Groups(i)-1
%                     for jj=pos2:pos2+Groups(j)-1
%                         if A(ii,jj)<p
%                             A(ii,jj)=1;
%                         else
%                             A(ii,jj)=0;
%                         end
%                     end
%                 end
%             end        
%         end
%     end

%     for i=1:num
%         for j=i:num
%             if i==j
%                 A(i,j)=0;
%             else
%                 A(j,i)=A(i,j);
%             end
%         end
%     end
    Z=zeros(num,1);
    pos=0;
    dis=1
    for k1=1:k
        if k1==1
            pos=1;
        else
            pos=pos+Groups(k1-1);
        end        
        for i=pos:pos+Groups(k1)-1
            Z(i,:)=k1;        
        end
    end
    
%     B=A;
%         for i=1:length(B)
%         r1=ceil(rand()*length(B));
%         r2=ceil(rand()*length(B));
%         B_r1=B(r1,:);
%         B_r2=B(r2,:);
%         B(r1,:)=B_r2;
%         B(r2,:)=B_r1;
%         B_c1=B(:,r1);
%         B_c2=B(:,r2);        
%         B(:,r1)=B_c2;
%         B(:,r2)=B_c1;
%         end
        dis=2
         spy(A)
%         spy(B);
    dlmwrite(testf2,Z,'delimiter',' ');
    dis=3
%     dlmwrite(testf1,A,'delimiter',' ');
    dis=4
%     dlmwrite(testf3,B,'delimiter',' ');
%     dis=5
%     outfile(A,testf);
%     dis=6
end

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
sum(sum(g_A));
%  �����ļ�ת�����ڽӾ���������ļ� 
dlmwrite(filename,edges,'delimiter',' ');


