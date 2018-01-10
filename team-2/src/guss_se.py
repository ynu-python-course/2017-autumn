import copy
def mymax(a):
    tmp=a[0]
    ans=tmp
    for i in a:
        if(tmp<i):
            ans=i
    return ans
def maxid(a):
    tmp=a[0]
    ans=tmp
    for i in a:
        if(tmp<i):
            ans=i
    for i in range(len(a)):
        if(ans==a[i]):
            return i
def guss_se(a,b,p,tme):
    x=[1]*len(a[0])
    m=[]
    w=1.25
    myid=[]
    xn=1
    xp1=1
    c=[[0 for j in range(len(a[0]))]for i in range(len(a))]
    for i in range(len(a)):
        m=m+[max(a[i])]
        myid=myid+[maxid(a[i])]
    for i in range(len(a)):
        temp=0
        for j in range(len(a[0])):
            if(a[i][j]!=m[i]):
                c[i][j-temp]=-a[i][j]
            else:
                temp=1
        c[i][j]=b[i]
    print(m)
    while(xn<tme or xp1>p):
        xp=copy.deepcopy(x)
        for i in range(len(x)):
            k=0
            temp=0
            temp1=x[i]
            for j in range(len(a[0])-1):
                if(j!=i):
                    temp=temp+c[i][j]*x[k]
                    k=k+1
                else:
                    k=k+1
                    temp=temp+c[i][j]*x[k]
                    k=k+1
            temp=temp+c[i][j+1]
            temp2=temp/m[i]
            #temp2=temp2*w
            #temp=1-w
            x[i]=temp2
            #x[i]=temp2+temp1*temp
        xp1=xp[0]-x[0]
        for i in range(len(x)):
            tmp=xp[i]-x[i]
            if(tmp>xp1):
                xp1=tmp
        xp1=abs(xp1)
        xn=xn+1
        print(x)
    print(x)
    print('times')
    print(xn-1)
    print(xp1)
a=[[8,-3,2],[4,11,-1],[6,3,12]]
b=[20,33,36]
oip'poa=[[-3,8,5],[2,-7,4],[1,9,-6]]
b=[6,9,1]
a=[[4,3,0],[3,4,-1],[0,-1,4]]
b=[24,30,-24]
a=[[4,-1,0,-1,0,0],[-1,4,-1,0,-1,0],[0,-1,4,0,0,-1],[-1,0,0,4,-1,0],[0,-1,0,-1,4,-1],[0,0,-1,0,-1,4]]
b=[0,5,0,6,-2,6]
p=0.00001
tme=8
guss_se(a,b,p,tme)                      
