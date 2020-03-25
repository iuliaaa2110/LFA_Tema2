f = open("NFAtoDFA_Date.in")
g = open("date.out", "w")

n = int(f.readline())  # starile sunt de la 0 la n-1
m = int(f.readline())
a = f.readline().split()  # alfabetul
d = {}
for i in range(m):
    d[a[i]] = i
qz = int(f.readline())  # stare initiala
nqf = int(f.readline())  # nr stari finale
qf = f.readline().split()  # stari finale
for i in range(nqf):
    qf[i] = int(qf[i])
qf=set(qf)
t = int(f.readline())  # nr de tranzitii

M = [[[] for i in range(m)] for j in range(n)]

for i in range(t):
    xyz = f.readline().split()
    x = int(xyz[0])
    y = xyz[1]
    z = int(xyz[2])
    M[x][d[y]].append(z)

def apartine(s, v):  # s este setul, v este vectorul de seturi
    for i in v:
        if s == i:
            return True
    return False

def stare_finala(s):
    global qf
    if s&qf:
        return True
    return False


v = []
M2 = []
k = 0
v.append({qz})
M2.append([[] for i in range(m)])
for j in range(m):
    k += 1
    v.append(set(M[qz][j]))
    M2[0][j] = set(M[qz][j])

y = 1
while y <= k:
    M2.append([[] for i in range(m)])
    for j in range(m):
        reuniune = []
        for i in v[y]:
            reuniune += M[i][j]
        if reuniune:
            M2[y][j] = reuniune
            if not apartine(set(reuniune), v):
                k += 1
                v.append(set(reuniune))
    y += 1

#stari finale:
qf2 = []
for i in range(k + 1):
    if stare_finala(v[i]):
        qf2.append(i)

#afisare:
print()
print("Indicii liniilor matricei:")
print(v)
print()
print()
print("Matricea DFA ului:")
print()
for i in range(k):
    print("Linia pentru starea "+str(v[i])+" este : ",M2[i])
print()
print("Automatul este:")
for i in range(k):
    for j in range(m):
        print("Din starea "+str(v[i])+" ajung cu simbolul ",a[j]," in starea ",M2[i][j])
        print()
print("Stari finale:")
for i in range(len(qf2)):
    print(v[qf2[i]])