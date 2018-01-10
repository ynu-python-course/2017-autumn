class r:
    @staticmethod
    def _gcd(m,n):
        if m==0 or n==0:
            return 1
        if m==1 or n==1:
            return 1
        if m<n:
            c=m
            d=n
        else:
            c=n
            d=m
        a=list(range(1,c+1))
        a.reverse()
        global o
        o=1
        for o in a:
            if c%o==0 and d%o==0:
                break
        return o
    @staticmethod
    def _mcm(m,n):
        if m==0 or n==0:
            return 1
        if m<n:
            c=m
            d=n
        else:
            c=n
            d=m
        global q
        for q in range(1,m*n+1):
            if (c*q)%d==0:
                break
        return c*q 
    def __init__(self,num,den=1):
        if num<0:
            _num=-num
            n=-1
        else:
            _num=num
            n=1
        if den<0:
            _den=-den
            m=-1
        else:
            _den=den
            m=1
        if m==-1 and n==-1:
            m=1
            n=1
        c=r._gcd(_num,_den)
        self.num=(_num//c)*n*m
        self.den=(_den//c)
    def __add__(self,another):
        c=r._mcm(self.den,another.den)
        num=self.num*(c//self.den)+another.num*(c//another.den)
        den=c
        return r(num,den)
    def __sub__(self,another):
        c=r._mcm(self.den,another.den)
        num=self.num*(c//self.den)-another.num*(c//another.den)
        den=c
        return r(num,den)
    def __mul__(self,another):
        return r(self.num*another.num,self.den*another.den)
    def __truediv__(self,another):
        if(self.num==0 or another.num==0):
           return r(0,1)
        return r(self.num*another.den,self.den*another.num)
    def __eq__(self,another):
        if(self.num==0 and another.num==0):
            return True
        elif(self.num==another.num and self.den==another.den):
            return True
        else:
            return False
    def __lt__(self,another):
        c=r._mcm(self.den,another.den)
        a=self.num*(c//self.den)
        b=another.num*(c//another.den)
        if(a<b):
            return True
        elif(a!=b):
            return False
        else:
            return False
    def __gt__(self,another):
        c=r._mcm(self.den,another.den)
        a=self.num*(c//self.den)
        b=another.num*(c//another.den)
        if(a>b):
            return True
        elif(a!=b):
            return False
        else:
            return False
    def printf(self):
        if self.den==1:
            print(str(self.num))
        elif self.num==0:
            print('0')
        if self.den!=1 and self.num!=0:
            print(str(self.num)+'/'+str(self.den))
def LUdivide(a):
    for i in range(len(a)):
        for j in range(len(a)):
            a[i][j]=r(a[i][j])
    for i in range(1,len(a)):
        a[i][0]=a[i][0]/a[0][0]
    for i in range(1,len(a)):
        p=0
        for j in range(1,len(a)):
            tmp=r(0)
            if(p<i):
                p+=1
            for k in range(p):
                tmp=a[k][j]*a[i][k]+tmp
            if(j<i):
                tmp=a[i][j]-tmp
                a[i][j]=tmp/a[j][j]
            else:
                a[i][j]=a[i][j]-tmp
    for i in range(len(a)):
        for j in range(len(a)):
            r.printf(a[i][j])
        print("\n")
a=[[2,10,0,-3],[-3,-4,-12,13],[1,2,3,-4],[4,14,9,-13]]
b=[[4,1,-1,0],[1,3,-1,0],[-1,-1,5,2],[0,0,2,4]]
LUdivide(a)
    
