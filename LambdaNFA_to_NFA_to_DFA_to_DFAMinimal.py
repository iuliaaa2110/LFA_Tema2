def afisare(automat):
    print("Automatul rezultat:")
    print()

    print("Numar de stari:")
    print(automat[0])
    print()

    print("Starile sunt:")
    for i in range(automat[0]):
        print(automat[1][i])
    print()

    print("Numarul de simboluri:")
    print(automat[2])
    print()

    print("Alfabetul:")
    for i in range(automat[2]):
        print(automat[3][i])
    print()

    print("Starea initiala:")
    print(automat[4])
    print()

    print("Numarul de stari finale:")
    print(automat[5])
    print()

    print("Starile finale:")
    for i in range(automat[5]):
        print(automat[6][i])
    print()

    print("Numarul de tranzitii:")
    print(automat[7])
    print()

    print("Tranzitiile")
    for i in range(automat[7]):
        for j in range(3):
            print(automat[8][i][j],end="  ")
        print()


def LambdaNFA_to_NFA(automat):

    def Lambda_inchidere(k, s):
        for j in range(len(M[k][m])):
            if M[k][m][j] not in s:
                s.append(M[k][m][j])
                Lambda_inchidere(M[k][m][j], s)


    def reuniune(lista1, k, lista2):
        for j in range(len(lista1)):
            for p in range(len(M[lista1[j]][k])):
                if M[lista1[j]][k][p] not in lista2:
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
        nonlocal qf2
        if l in qf2:            #daca era stare finala, trebuie sa o elimin si de acolo
            qf2.remove(l)

        for i in range(n2):     #pe coloana m mi am pus eu indicii liniilor, ca atunci cand tai din ele sa stiu ce stari raman. Asadar acum caut linia corespunzatoare starii l, si pe aceea o voi elimina
            if M2[i][m] == l:
                l = i

        for i in range(l, n2 - 1):
            M2[i] = M2[i + 1]   #o sa dezaloc liniile ramase in plus mai tarziu



    def pas1():
        nonlocal m
        for i in range(n):
            M[i][m + 1] = [i]  # M[i][m+1]=coloana lui lambda*
            Lambda_inchidere(i, M[i][m + 1])


    def pas2():
        nonlocal m
        for k in range(m):
            for i in range(n):
                lista = []
                reuniune(M[i][m + 1], k, lista)
                for ii in range(n):
                    listaf = []
                    reuniune(lista, m + 1, listaf)
                M2[i][k] = listaf


    def pas3():  # ma uit in M[][m+1] acolo este lambda*
        nonlocal qf,m
        for i in range(n):
            for l in range(len(M[i][m + 1])):
                if M[i][m+1][l] in qf and i not in qf2:
                    qf2.append(i)


    def pas4():
        nonlocal n2
        for i in range(n2-1):
            for j in range(i + 1, n2):
                if egale(M2[i], M2[j]) and ( (M2[i][m] in qf2 and M2[j][m] in qf2) or (M2[i][m] not in qf2 and M2[j][m] not in qf2)):
                    inlocuiesc(M2[j][m], M2[i][m])  # M2[][m]= indicele liniei
                    elimin(M2[j][m])  # elimin linia
                    n2-=1
        for i in range(n2):
            for j in range(m):
                if M2[i][j] == []:
                    M2[i][j] = []
                else:
                    M2[i][j] = list(set(M2[i][j]))


    #1)explicitez automatul:
    # (extrag doar ce am de gand sa folosesc:)

    n=automat[0]        # nr de stari=nr de linii
    m=automat[2]        # nr de simboluri=nr de coloane
    qf=automat[6]       # vectorul de stari finale
    M=automat[9]        # Matricea automatului
    tranzitii=automat[8]

    d = {}
    for i in range(m):
        d[a[i]] = i
    d['$'] = m  # lambda

    M = [[[] for i in range(m + 2)] for j in range(n)]  # m+2 pt coloana lui lambda si coloana lui lambda*
    for i in range(t):
        xyz = tranzitii[i]
        x = int(xyz[0])
        y = xyz[1]
        z = int(xyz[2])
        M[x][d[y]].append(z)


    M2 = [[[] for i in range(m + 1)] for j in range(n)]
    for i in range(n):
        M2[i][m] = i    # in M2[i][m] retin indicii liniilor deoarece o sa elimin din ele si va trebui sa stiu pe care
    n2 = n              # n2 ul matricei2 se va micsora, nu va fi tot n
    qf2 = []            # M2 va avea o alta multime de stari finale


    #2)Rezolvarea propriu-zisa

    pas1()  # calcularea lambda-inchiderii
    pas2()  # calcularea functiei de tranzitie
    pas3()  # stari finale
    pas4()  # elimin dublurile


    #3)imi construiesc noul automat:

    automat2 = [0] * 10
    automat2[0] = n2  # nr de stari=nr de linii
    stari2=[]
    for i in range(n2):
        stari2.append(M2[i][m])
    automat2[1] = stari2  # vectorul de stari
    automat2[2] = m  # nr de simboluri=nr de coloane
    automat2[3] = automat[3]  # alfabetul
    automat2[4] = automat[4]  # starea initiala
    automat2[5] = len(qf2)  # numarul de stari finale
    automat2[6] = qf2  # vectorul de stari finale
    tranzitii2=[]
    for i in range(n2):
        for j in range(m):
            for l in range(len(M2[i][j])):
                tranzitii2.append([i,a[j],M2[i][j][l]])
    automat2[7] =len(tranzitii2)# numarul de tranzitii
    automat2[8] =tranzitii2     #tranzitii
    for i in range(n2):
        M2[i].pop(m)        #imi retinusem eu pe coloana m numele starii liniei i, dar acum nu mai am nevoie, e totul in stari2.
    for i in range(n2,n):   #pe asta as fi putut sa o fac si in subprogramul elimina
        M2.pop(n2)
    automat2[9] = M2  # Matricea automatului

    return automat2


def NFA_to_DFA(automat):

    def stare_finala(s):
        nonlocal qf
        if s.intersection(s,set(qf)) != set():
            return True
        return False


    def stari_finale():
        nonlocal qf2,k,v
        for i in range(k + 1):
            if stare_finala(v[i]):
                qf2.append(v[i])

    def rezolvare():
        nonlocal y,k,M2,v,ds
        while y <= k:
            M2.append([[] for i in range(m)])
            for j in range(m):
                reuniune = []
                for i in v[y]:
                    reuniune += M[ds[i]][j]
                if reuniune:
                    M2[y][j] = set(reuniune)
                    if set(reuniune) not in v:
                        k += 1
                        v.append(set(reuniune))
            y += 1


    # 1)explicitez automatul:
    # (extrag doar ce am de gand sa folosesc:)

    n = automat[0]  # nr de stari=nr de linii
    qz = automat[4] #stare initiala
    m = automat[2]  # nr de simboluri=nr de coloane
    qf = automat[6]  # vectorul de stari finale
    stari=automat[1]
    t=automat[7]
    tranzitii=automat[8]

    d = {}
    for i in range(m):
        d[a[i]] = i

    M = [[[] for i in range(m)] for j in range(n)]

    for i in range(t):
        xyz = tranzitii[i]
        x = int(xyz[0])
        y = xyz[1]
        z = int(xyz[2])
        M[x][d[y]].append(z)

    #initializez noi variabile:

    ds={}   #voi avea un dictionar de stari.Exemplu starea care se numeste 3 dar se afla pe linia 2: voia avea d[3]=2
    for i in range(n):
        ds[stari[i]]=i
    v = []
    M2 = []
    k = 0
    v.append({qz})  #vector de stari
    M2.append([[] for i in range(m)])
    for j in range(m):
        k += 1
        v.append(set(M[qz][j]))
        M2[0][j] = set(M[qz][j])
    qf2 = []  # vector de stari finale
    y = 1


    #2)rezolvarea propriu-zisa

    rezolvare()
    stari_finale()


    #3)Imi construiesc noul automat:

    automat2=[0]*10
    automat2[0]=k+1
    automat2[1]=v
    automat2[2]=m
    automat2[3]=automat[3]
    automat2[4]={qz}
    automat2[5]=len(qf2)
    automat2[6]=qf2
    tranzitii2=[]
    for i in range(k + 1):
        for j in range(m):
            if M2[i][j]:
                tranzitii2.append([v[i],a[j],M2[i][j]])
            if M2[i][j]==[]:
                M2[i][j]={}
    automat2[7]=len(tranzitii2)
    automat2[8]=tranzitii2
    automat2[9]=M2
    return automat2


def DFA_to_DFAMinimal(automat):
    global d

    def noua_stare(x):  #noua_stare(x) imi returneaza acea stare din automatul nou care contine starea x din automatul vechi
        nonlocal v
        for i in range(n2):
            if x in list(v[i]):
                return v[i] #exp pt starea 2 din automatul initial noua stare va fi cea care il contine, gen {2,3,4} si o returnez pe asta.


    def dead_end(i,ap):       #i este indicele starii, nu puteam sa apelez pt stare, deoarece nu exista M[{1,2,3}][j], dar pot sa fac M[i][j] iar v[i]=starea {1,2,3}.
        nonlocal M2,v,qf2,m,ok
        for j in range(m):
            if M2[i][j]:
                if nu[v.index(M2[i][j])]==1:    #starea atsa nu este de tip dead_end.
                    ok=0
                    break

                elif M2[i][j] in qf2:         #daca e stare finala.
                    ok=0                    #inseamna ca NU este o stare de tip dead_end
                    for i in range(n2):         #=> toate starile marcate in  ap acum NU sunt, la randul lor stari de tip dead_end => nu vreau sa le mai testez odata=> o sa le marchez in nu[]
                        nu[i]=nu[i] or ap[i]
                    break

                elif M2[i][j] in v and ap[v.index(M2[i][j])]==0:        #Daca starea in care ma duc este diferita de cele prin care am trecut pana acum ( daca sunt egale subprogramul se opreste pt a nu intra in ciclu infinit )
                        ap[v.index(M2[i][j])]=1
                        dead_end(v.index(M2[i][j]), ap) #pozitia starii M[i][j] in vectorul de stari


    def elimin(stare):
        nonlocal M2,v
        for i in range(n2):
            for j in range(m):
                if M2[i][j]==stare:
                    M2[i][j]={}
        v.remove(stare)


    def sterge_stare(i):
        nonlocal M2,n2,v,qf2
        M2.pop(i)
        n2 -= 1
        if v[i] in qf2:
            qf2.remove(v[i])
        elimin(v[i])  # rup toate legaturile cu starea v[i]


    def parcurg(i): #e foarte asemanator cu dead_end
        nonlocal M2,v,app
        for j in range(m):
            if M2[i][j] in v and app[v.index(M2[i][j])] == 0:  # Daca starea in care ma duc este diferita de cele prin care am trecut pana acum ( daca sunt egale subprogramul se opreste pt a nu intra in ciclu infinit )
                app[v.index(M2[i][j])] = 1
                parcurg(v.index(M2[i][j]))  # pozitia starii M[i][j] in vectorul de stari

    def pas1_a():
        nonlocal A
        for i in range(n):
            A.append([True] * i)


    def pas1_b():
        nonlocal A,n,qf
        for i in range(n - 1, -1, -1):  # parcurg liniile descrescator ca sa ma asigur ca exista A[i][l]
            for l in range(i):
                if (i in qf and l not in qf) or (i not in qf and l in qf):  # daca una e stare finala si cealalta nu e
                    A[i][l] = False

    def pas1_c():
        nonlocal A,M,n
        k=1     #k este ca sa repet pasul c pana nu mai apar modificari
        while k==1:
            k=0
            for j in range(m):
                for i in range(n - 1, -1, -1):
                    for l in range(i):
                        if (M[i][j]==-1 and M[l][j]!=-1) or (M[i][j]!=-1 and M[l][j]==-1):
                            A[i][j]=False
                        else:
                            #i mereu > l
                            if M[i][j] != -1 and M[l][j] != -1:
                                a=max(M[i][j],M[l][j])
                                b=min(M[i][j],M[l][j])
                                if a!=b and A[a][b] == False and A[i][l] != False: # j este simbolul. Daca ( ~(i,j),~(l,j) ), atunci marchez (i,l)
                                    A[i][l] = False                                                         #M[i][j]= ~(i,j)
                                    k=1                                                                     #A [M[[i][j]]] [M[[l][j]]]= (i,j)


    def pas2():
        nonlocal M2,v,n2
        marchez=[0]*n
        for i in range(n-1,-1,-1):
            if marchez[i]==0:
                s=[i]
                marchez[i]=1
                for j in range(i):
                    if A[i][j]==True and marchez[j]==0:
                        s.append(j)
                        marchez[j]=1
                v.append(set(s))    #eu oricum am avut grija sa nu pun acelasi element de doua ori, dar il fac set ca sa nu conteze ordinea elementelor. Sa nu patesc ceva de genul [1,2,3] != [3,2,1]
                n2+=1
                M2.append([[] for i in range(m)])   #aloc o linie in matrice pentru starea v[k]=s
        for i in range(n2):
            for j in range(m):
                M2[i][j]=noua_stare(M[list(v[i])[0]][j])      #e de ajuns sa verific pt o singura componenta din starea v[i] ca sa aflu unde se duce, de aceea fac v[i][0].


    def pas3():
        nonlocal qz,qz2,qf,qf2

        #stare initiala:

        qz2=noua_stare(qz)  #noua_stare(x) imi returneaza acea stare din automatul nou care contine starea x din automatul vechi

        #stari finale:

        while qf!=[]:
            qf2.append(noua_stare(qf[0]))
            for j in (noua_stare(qf[0])):
                qf.remove(j)        #distrug multimea initiala de stari finale


    def pas4():
        nonlocal n2,M2,v,ok,nu,qz2
        i=0
        nu=[0]*n2
        while i < n2:
            ap=[0]*n2
            ap[i]=1
            ok=1    #presupun ca i este o stare de tip dead_end
            dead_end(i,ap)
            if ok==1:
                sterge_stare(i)
            i+=1


    def pas5():
        nonlocal n2,qz,app,v,qz2

        app=[0]*n2
        app[v.index(qz2)]=1
        i=0

        parcurg(v.index(qz2)) #parcurg automatul, plecand din starea initiala si imi marchez toate starile in care ajung.

        while i<n2:
            if app[i]==0:
                sterge_stare(i)
            i+=1


    #1)explicitez automatul:

    n = automat[0]  # nr de stari=nr de linii
    qz = automat[4]  # stare initiala
    m = automat[2]  # nr de simboluri=nr de coloane
    M = automat[9]  # Matricea automatului
    stari=automat[1]
    qf=automat[6]
    t=automat[7]
    tranzitii=automat[8]
    d = {}
    for i in range(m):
        d[a[i]] = i

    M = [[-1 for i in range(m)] for j in range(n)]
    for i in range(t):
        xyz = tranzitii[i]
        x = int(xyz[0])
        y = xyz[1]
        z = int(xyz[2])
        M[x][d[y]]=z

    #declar variabile:

    A = []
    M2=[]
    v = []  # vectorul de stari
    n2 = 0
    qz2=0   #starea initiala, o declar de aici, dar nu va ramane 0, evident.
    qf2=[]
    ok=1
    nu=[]
    app=[]

    #2)Rezolvarea propriu-zisa:

    pas1_a()    #construiesc matricea de echivalenta si o initializez cu TRUE
    pas1_b()    #Marchez cu false perechiile (i,l) unde i e stare finala si l stare nefinala sau invers
    pas1_c()    #Marchez cu FALSE toate perechile (q, r) pentru care (δ(q, α), δ(r, α)) sunt marcate cu FALSE ∀α ∈ Σ.
    pas2()      #formez seturile(noile stari) si construiesc M2
    pas3()      #Calculez starile finale si initiale
    pas4()      #Elimin starile de tip dead_end
    pas5()      #Elimin starile neaccesibile

    #3)Imi construiesc noul automat:

    automat2=[0]*10

    automat2[0]=n2
    automat2[1]=v
    automat2[2]=m
    automat2[3]=automat[3]
    automat2[4]=qz2
    automat2[5]=len(qf2)
    automat2[6]=qf2
    tranzitii2=[]
    for i in range(n2):
        for j in range(m):
            if M2[i][j]:
                tranzitii2.append([v[i],a[j],M2[i][j]])
    automat2[7]=len(tranzitii2)
    automat2[8]=tranzitii2
    automat2[9]=M2
    return automat2


# main:
f = open("date.in")
g = open("date.out", "w")

n = int(f.readline())       # starile sunt de la 0 la n-1
stari=[0]*(n+1)
for i in range(n):
    stari[i]=i

m = int(f.readline())

a = f.readline().split()    # alfabetul

qz = int(f.readline())      # stare initiala

qfn = int(f.readline())       # nr stari finale
qf = f.readline().split()   # stari finale
for i in range(qfn):
    qf[i] = int(qf[i])

t = int(f.readline())       # nr de tranzitii

tranzitii=[]
for i in range(t):
    xyz = f.readline().split()
    x = int(xyz[0])
    y = xyz[1]
    z = int(xyz[2])
    tranzitii.append([x,y,z])

automat=[0]*10
automat[0]=n        #nr de stari=nr de linii
automat[1]=stari    #vectorul de stari
automat[2]=m        #nr de simboluri=nr de coloane
automat[3]=a        #alfabetul
automat[4]=qz       #starea initiala
automat[5]=qfn      #numarul de stari finale
automat[6]=qf       #vectorul de stari finale
automat[7]=t        #numarul de tranzitii
automat[8]=tranzitii

automat1=LambdaNFA_to_NFA(automat)
automat2=NFA_to_DFA(automat)
automat3=DFA_to_DFAMinimal(automat)
afisare(automat3)
