def apartine(y, lista):
    for i in range(len(lista)):
        if lista[i] == y:
            return True
    return False


def Lambda_inchidere(k, s):
    for j in range(len(M[k][m])):
        if not (apartine(M[k][m][j], s)):
            s.append(M[k][m][j])
            Lambda_inchidere(M[k][m][j], s)


def reuniune(lista1, k, lista2):
    for j in range(len(lista1)):
        for p in range(len(M[lista1[j]][k])):
            if not apartine(M[lista1[j]][k][p], lista2):
                lista2.append(M[lista1[j]][k][p])


def egale(lista1, lista2):  # liste de m liste
    for i in range(m):
        if set(lista1[i]) != set(lista2[i]):
            return False
    return True


def inlocuiesc(y, x):
    for i in range(n2):
        for j in range(m):
            for l in range(len(M2[i][j])):
                if M2[i][j][l] == y:
                    M2[i][j][l] = x


def elimin(l):
    global n2
    for i in range(n2):
        if M2[i][m] == l:
            l = i
    for i in range(l, n2 - 1):
        M2[i] = M2[i + 1]
    n2 -= 1


def pas1():
    for i in range(n):
        M[i][m + 1] = [i]  # M[i][m+1]=coloana lui lambda*
        Lambda_inchidere(i, M[i][m + 1])


def pas2():
    for k in range(m):
        for i in range(n):
            lista = []
            reuniune(M[i][m + 1], k, lista)
            for ii in range(n):
                listaf = []
                reuniune(lista, m + 1, listaf)
            M2[i][k] = listaf


def pas3():  # ma uit in M[][m+1] acolo este lambda*
    global qf
    for i in range(n):
        for l in range(len(M[i][m + 1])):
            if apartine(M[i][m + 1][l], qf) and not apartine(i, qf2):
                qf2.append(i)


def pas4():
    for i in range(n2 - 1):
        for j in range(i + 1, n2):
            if egale(M2[i], M2[j]) and ( (apartine(M2[i][m], qf2) and apartine(M2[j][m], qf2)) or (not apartine(M2[i][m], qf2) and not apartine(M2[j][m], qf2)) ):
                inlocuiesc(M2[j][m], M2[i][m])  # M2[][m]= indicele liniei
                elimin(M2[j][m])  # elimin linia
    for i in range(n2):
        for j in range(m):
            if M2[i][j] == []:
                M2[i][j] = []
            else:
                M2[i][j] = list(set(M2[i][j]))


def afisare1():
    global a
    print()
    print("Starile sunt:")
    for i in range(n2):
        print(M2[i][m],end=" ")
    print()
    print()
    print("Alfabetul este acelasi:")
    print(a)
    print()
    print("Starea initiala este aceeasi:")
    print(qz)
    print()
    print("Starile finale:")
    print(qf2)
    print()
    print("Tranzitiile NFA ului obtinut:")
    for i in range(n2):
        for j in range(m):
            for l in range(len(M2[i][j])):
                print(i, " ", a[j] , " ", M2[i][j][l])
    print()
    print("Matricea NFA ului obtinut:")
    for i in range(n2):
        print(M2[i][m], ": ", end=" ")
        for j in range(m):
            print(M2[i][j], end=" ")
        print()
    print()


def LambdaNFA_to_NFA():
    pas1()  # calcularea lambda-inchiderii
    pas2()  # calcularea functiei de tranzitie
    pas3()  # stari finale
    pas4()  # elimin dublurile
    afisare1()


# main:
f = open("date.in")
g = open("date.out", "w")

n = int(f.readline())  # starile sunt de la 0 la n-1
m = int(f.readline())
a = f.readline().split()  # alfabetul
d = {}
for i in range(m):
    d[a[i]] = i
d['$'] = m  # lambda
qz = int(f.readline())  # stare initiala
k = int(f.readline())  # nr stari finale
qf = f.readline().split()  # stari finale
for i in range(k):
    qf[i] = int(qf[i])
t = int(f.readline())  # nr de tranzitii

M = [[[] for i in range(m + 2)] for j in range(n)]  # m+2 pt coloana lui lambda si coloana lui lambda*

for i in range(t):
    xyz = f.readline().split()
    x = int(xyz[0])
    y = xyz[1]
    z = int(xyz[2])
    M[x][d[y]].append(z)

M2 = [[[] for i in range(m + 1)] for j in range(n)]
for i in range(n):
    M2[i][m] = i  # retin indicii liniilor deoarece o sa elimin din ele si va trebui sa stiu pe care
n2 = n  # n2 ul matricei2 se va micsora, nu va fi tot n
qf2 = []  # M2 va avea o alta multime de stari finale

LambdaNFA_to_NFA()
