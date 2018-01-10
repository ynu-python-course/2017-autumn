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

def inverse(a):
    b=[[0 for j in range(2*len(a))]for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a)):
            b[i][j]=a[i][j]
    for i in range(len(a)):
        for j in range(len(a),2*len(a)):
            if i==(j-len(a)):
                b[i][j]=1
    def resort(a,n):
        max=a[n][n]
        q=n
        p=n
        for i in range(n,(len(a))):
            for j in range(n,len(a)):
                if(a[i][j]>max):
                    max=a[i][j]
                    q=i
                    p=j
        def jh(a,n,q,p):
            if(p!=n):
                for i in range(n,(len(a))):
                    temp=a[i][n]
                    a[i][n]=a[i][p]
                    a[i][p]=temp
            if(q!=n):
                for j in range(n,(2*len(a))):
                    temp=a[n][j]
                    a[n][j]=a[q][j]
                    a[q][j]=temp
        if(q!=n and p!=n):
            jh(a,n,q,p)
        return(a)
    b=resort(b,0)

    #for i in range(len(b)):
        #for j in range(2*len(b)):
            #b[i][j]=r(b[i][j])
    for k in range(1,len(b)):
        b=resort(b,k-1)
        for i in range(k,len(b)):
            m=b[i][k-1]/b[k-1][k-1]
            for j in range(k-1,2*len(b)):
                b[i][j]=b[i][j]-b[k-1][j]*m
    c=list(range(len(b)))
    c.reverse()
    n=0
    for k in c[:len(b)-1]:
        n+=1
        for i in c[n:]:
            m=b[i][k]/b[k][k]
            for j in range(k,2*len(b)):
                b[i][j]=b[i][j]-(b[k][j]*m)
    for i in range(len(b)):
        p=b[i][i]
        for j in range(i,2*len(b)):
            b[i][j]=b[i][j]/p
    print(b)


a=[[-3,8,5],[2,-7,4],[1,9,-6]]
inverse(a)
                                               


            
                    


        
        


