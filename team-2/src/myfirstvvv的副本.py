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
    #def num(self):
        #return self.num
    #def den(self):
        #return self.den
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
        return r(self.num*another.den,self.den*another.num)
    def printf(self):
        if self.den==1:
            print(str(self.num))
        elif self.num==0:
            print('0')
        if self.den!=1 and self.num!=0:
            print(str(self.num)+'/'+str(self.den))

def inverse(a,c):
    b=[[0 for j in range(len(a)+1)]for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a)):
            b[i][j]=a[i][j]
    for i in range(len(a)):
        b[i][len(a)]=c[i]
    def trans(i):
        for j in range(len(b)+1):
            temp=b[0][j]
            b[0][j]=b[i][j]
            b[i][j]=temp
    if b[0][0]==0:
        n=1
        for i in range(1,len(b)):
            if b[i][0]==1:
                trans(i)
                break
            else:
                n+=1
        if n==len(b):
            trans(1)
    for i in range(len(b)):
        for j in range(len(b)+1):
            b[i][j]=r(b[i][j])
    for k in range(1,len(b)):
        for i in range(k,len(b)):
            m=b[i][k-1]/b[k-1][k-1]
            for j in range(k-1,len(b)+1):
                b[i][j]=b[i][j]-b[k-1][j]*m
    c=list(range(len(b)))
    c.reverse()
    n=0
    for k in c[:len(b)-1]:
        n+=1
        for i in c[n:]:
            m=b[i][k]/b[k][k]
            for j in range(k,len(b)+1):
                b[i][j]=b[i][j]-(b[k][j]*m)
    for i in range(len(b)):
        p=b[i][i]
        for j in range(i,len(b)+1):
            b[i][j]=b[i][j]/p
    for i in range(len(b)):
        for j in range(len(b),len(b)+1):
            b[i][j].printf()
b=[[4,1,-1,0],[1,3,-1,0],[-1,-1,5,2],[0,0,2,4]]
c=[7,8,-4,6]
inverse(b,c)

                                               


            
                    


        
        


