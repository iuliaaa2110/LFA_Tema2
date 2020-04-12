f=open("date.in")
g=open("date.out","w")
n=int(f.readline())     #starile sunt de la 0 la n-1
m=int(f.readline())
a=f.readline().split()  #alfabetul
d={}
for i in range(m):
    d[a[i]]=i
d['$']=m    #lambda
qz=int(f.readline())    #stare initiala
k=int(f.readline() )         #nr stari finale
qf=f.readline().split()  #stari finale
for i in range(k):
    qf[i]=int(qf[i])
t=int(f.readline())     #nr de tranzitii

M=[ [ [] for i in range(m+1) ] for j in range(n) ]

for i in range(t):
    xyz=f.readline().split()
    print(xyz)
    x=int(xyz[0])
    y=xyz[1]
    z=int(xyz[2])
    M[x][d[y]].append(z)
print(M)
