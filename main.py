from graphics import *
from math import *
from copy import copy


class Stare:
    def __init__(self, name):
        self.nume = name

    def Punct(self):
        return Point(x, y)


def same(nod1, nod2):
    if nod1.name == nod2.name:
        return 1
    else:
        return 0

def search(lista, nume):
    for i in range(len(lista)):
        if lista[i].nume == nume:
            return i
    else:
        return "eroare"


def selftranzitie(nod, nume, win):
    x = nod.x
    y = nod.y
    if x < 250:
        directie = "left"
    elif x > 550:
        directie = "right"
    elif y <= 250:
        directie = "up"
    else:
        directie = "down"
    if directie == "left":
        x -= 70
        c = Circle(Point(x + 20, y), 2)

    if directie == "right":
        x += 70
        c = Circle(Point(x - 20, y), 2)

    if directie == "up":
        y -= 70
        c = Circle(Point(x, y + 20), 2)

    if directie == "down":
        y += 70
        c = Circle(Point(x, y - 20), 2)
    c.setFill('pink')
    c.setOutline('pink')
    cir = Circle(Point(x, y), 20)
    cir.setOutline('pink')
    cir.setWidth(2)
    cir.draw(win)
    c.draw(win)
    text = Text(Point(x, y), nume)
    text.setSize(10)
    text.setTextColor('pink')
    text.draw(win)


def tranzitie(nod1, nod2, nume, win):
    x1 = nod1.x
    y1 = nod1.y
    x2 = nod2.x
    y2 = nod2.y
    ln = Line(Point(x1, y1), Point(x2, y2))
    ln.setArrow("last")
    ln.setWidth(3)
    x = (3 * x1 + x2) // 4
    y = (3 * y1 + y2) // 4
    pt = Point(x, y)
    if x1 > x2 or y1 < y2:
        ln.setFill('aqua')

    else:
        ln.setFill('yellow')
    tx = Text(pt, nume)
    tx.setTextColor('red')
    tx.setSize(20)
    ln.draw(win)
    tx.draw(win)


def stare(nod, final, win):
    x = nod.x
    y = nod.y
    text = nod.nume
    cir = Circle(Point(x, y), 50)
    cir.setOutline('white')
    cir.setWidth(2)
    cir.draw(win)

    if final == 1:
        cir2 = Circle(Point(x, y), 40)
        cir2.setOutline('white')
        cir2.setWidth(2)
        cir2.draw(win)
    elif final == -1:
        ln = Line(Point(x, y + 100), Point(x, y + 50))
        ln.setArrow("last")
        ln.setWidth(3)
        ln.setOutline('green')
        ln.draw(win)

    tx = Text(Point(x, y), text)
    tx.setSize(20)
    tx.setTextColor('red')
    tx.draw(win)

def transform(lista):           #transforma o lista de stari intr-un string, reprezentand o stare
    st = "[" + lista[0].nume
    for j in range(1, len(lista)):
        st += "," + lista[j].nume
    st += "]"
    return st

def search2(obiect,lista):
    for i in range(len(lista)):
        if transform(obiect)==lista[i].nume:
            return i
    return "eroare"


class Automat:
    #stari - multimea de stari
    #sin - stare initiala
    #sfin - stare finala
    #tranzitii - multimea de tranzitii stocate sub forma unui dictionar {stare:{tranzitie:[stare1,..]}
    def citire(self):
        with open("automat.in", 'r') as f:
            f.readline()
            s = f.readline().split()  #
            self.stari = []

            for i in s:
                self.stari.append(Stare(i))
            t = f.readline().replace("\n", "")  #
            self.sin = self.stari[search(self.stari, t)]
            s = f.readline().split()
            self.sfin = []

            for i in s:
                (self.sfin).append(self.stari[search(self.stari, i)])
            self.tranzitii = {}

            for i in self.stari:
                self.tranzitii[i] = {}

            x = f.readline()

            while x:
                x = x.split()
                if x[1] not in self.tranzitii[self.stari[search(self.stari,x[0])]].keys():
                    self.tranzitii[self.stari[search(self.stari, x[0])]][x[1]]=[]
                self.tranzitii[self.stari[search(self.stari, x[0])]][x[1]].append(self.stari[search(self.stari, x[2])])
                x = f.readline()


    def afisare_grafica(self,screen=1):
        #screen = 1 in prima jumatate a ecranului, screen= 2 in a doua jumatate a ecranului

        ##############################
        # determinare coordonate noduri
        ##############################

        n = len(self.stari)
        alpha = 2 * pi / n
        # print(alpha)
        r = 300  # raza

        if screen == 1:
            for i in range(n):
                x = r * sin(i * alpha)
                y = r * cos(i * alpha)
                self.stari[i].x = x + 400
                self.stari[i].y = y + 400
                # print(x,y)
        else:
            for i in range(n):
                x = r * sin(i * alpha)
                y = r * cos(i * alpha)
                self.stari[i].x = x + 1200
                self.stari[i].y = y + 400


        afisate=[]
        for i in self.stari:
            if i in self.sfin:
                stare(i, 1, win)
            elif i == self.sin:
                stare(i, -1, win)
            else:
                stare(i, 0, win)
            if i in self.tranzitii.keys():
                for j in self.tranzitii[i].keys():
                    if  isinstance(self.tranzitii[i][j],list):
                        for m in self.tranzitii[i][j]:
                            if (i.nume,m.nume) not in afisate:
                                tran=j
                                for p in self.tranzitii[i].keys():
                                    if m in self.tranzitii[i][p] and p!=tran:
                                        tran=tran+","+p
                                if i == m:
                                    selftranzitie(i, tran, win)
                                else:
                                    tranzitie(i, m, tran, win)
                                afisate.append((i.nume,m.nume))
                    else:
                        m=self.tranzitii[i][j]
                        if (i.nume, m.nume) not in afisate:
                            tran = j
                            for p in self.tranzitii[i].keys():
                                if m == self.tranzitii[i][p] and p != tran:
                                    tran = tran + "," + p
                            if i == m:
                                selftranzitie(i, tran, win)
                            else:
                                tranzitie(i, m, tran, win)
                            afisate.append((i.nume, m.nume))



    def convert(self):
        stari2=copy(self.stari)
        sfin2=copy(self.sfin)
        sin2=copy(self.sin)
        tranzitii2=copy(self.tranzitii)
        tranz=[]
        for i in tranzitii2.values():
            for j in i.keys():
                if j not in tranz:
                    tranz.append(str(j))
        self.stari=[]
        stari=[]
        self.sfin=[]
        stari.append([self.sin])
        self.stari.append(Stare(transform(stari[0])))
        self.sin=self.stari[0]
        self.tranzitii = {}
        poz=0
        for i in stari:
            for j in tranz:
                st=[]
                for k in i:
                    if j in tranzitii2[k].keys():
                        for l in tranzitii2[k][j]:
                            if l not in st:
                                st.append(l)
                if len(st)>0:
                    for v in stari:
                        if set(v)==set(st):
                            break
                    else:
                        stari.append(st)
                        self.stari.append(Stare(transform(st)))
                        poz+=1
                        for fin in sfin2:
                            if fin in st:
                                self.sfin.append(self.stari[poz])
                if len(st)>0:
                    a=self.stari[search2(i,self.stari)]
                    if a not in self.tranzitii.keys():
                        self.tranzitii[a]={}
                        print(a.nume," da ")
                    else:
                        print(a.nume,"nu")
                    self.tranzitii[a][j]=self.stari[search2(st,self.stari)]

        print(self.stari)
        print(self.tranzitii)
        for i in self.sfin:
            print(i.nume,end=", ")
        print()
        for i in self.tranzitii.keys():
            print(i.nume,end=" : {")
            for j in self.tranzitii[i].keys():
                print(j, self.tranzitii[i][j].nume, sep=" :[",end="] ")
            print("}, ",end="")
            ###rezolva problema cu muchii lipsa
            ###initializeaza starile initiale si finale
        #####################################
        #####################################



aut = Automat()
aut.citire()
######################
win = GraphWin("Automat", 1600, 800)
win.setBackground('black')
aut.afisare_grafica()
aut.convert()
aut.afisare_grafica(2)
win.getMouse()
#######################
