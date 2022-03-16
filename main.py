from itertools import count
from tokenize import String
from tracemalloc import start

def drawBorder(row, col):
    tablero = [[' ' for c in range(col * 5)] for r in range(row * 3)]
    for rowC in range(len(tablero)):
        if(rowC < 3 or rowC >= (row * 3) - 3):
            for colC in range(len(tablero[rowC])):
                tablero[rowC][colC] = '▒'
        else:
            for colC in range(len(tablero[rowC])):
                    if(colC < 5 or colC >= ((col * 5) - 5)):
                        if rowC >= 9 and rowC < 12:
                            if (colC < 5):
                                tablero[rowC][colC] = '▒'
                        else:
                            tablero[rowC][colC] = '▒'
    return tablero


class Coche:
    def __init__(self, string, letter):
        self.direction = string[0]
        self.letter = letter
        self.posX = int(string[1])+4
        self.posY = int(string[2])+2
        self.length = int(string[3])

    def drawCar(self, tablero):
        return tablero
    
class Nivel:
    def __init__(self, data, row, col):
        data.pop(0)
        self.cars = []
        count = 1
        for car in data:
            letter = chr(ord('@') + count)
            self.cars.append(Coche(car, letter))
            count += 1
        self.tablero = drawBorder((row + 2), (col + 2))


    def draw(self):
        for i in range(len(self.cars)):
            self.tablero = self.cars[i].drawCar(self.tablero)
        
        for row in self.tablero:
            string = ""
            for cell in row:
                string += cell
            print(string)

def readPuntos():
    try:
        fichero = open("records.txt", "r")
        Lineas = fichero.readlines()
        records = []
        for i in Lineas:
            records.append(int(i.strip()))
        if len(records) == 0:
            records = ['']
            maxLevel = 1
        else:
            print(records)
            maxLevel = len(records)
    except:
        fichero = open("records.txt", "w")
        records = ['']
        maxLevel = 1
    return records, maxLevel

def readLevels(rows, cols):
    try:
        fichero = open("niveles.txt", "r")
        Lineas = fichero.readlines()
        nNiveles = Lineas[0].strip()
        niveles = []
        data = []
        Lineas.pop(0)
        for linea in Lineas:
            if(linea.strip().isdigit() and len(data) != 0):
                nivel = Nivel(data, rows, cols)
                niveles.append(nivel)
                data = []
            data.append(linea.strip())
        return nNiveles, niveles

    except:
        print("El archivo niveles.txt, no existe.")

def startGame(records, maxLevel):
    printString = "Elija nivel (1-"+str(maxLevel)+"): "
    levelSelected = -1
    correct = False
    while correct == False:
        levelSelected = int(input(printString))
        if(levelSelected >= 1 and levelSelected <= maxLevel):
            correct = True
        else: 
            print("Seleccion incorrecta")

    toPrintRecord = str(records[int(levelSelected)-1])
    if (toPrintRecord == ''):
        print("NIVEL "+str(levelSelected)+" - NO HAY RECORD")
    else:
        print("NIVEL "+str(levelSelected)+" - RECORD "+toPrintRecord+" MOVIMIENTOS")


if __name__ == "__main__":
    nNiveles, niveles  = readLevels(6, 6)
    records, maxLevel = readPuntos()
    startGame(records, maxLevel)
    niveles[0].draw()
    

"""
COCHE 3 DE LONGITUD
┌──── ───── ────┐
│ A           a │ 
└──── ───── ────┘

COE = u'\u2500' # ─
CNS = u'\u2502' # │
CSE = u'\u250C' # ┌
CSO = u'\u2510' # ┐
CNE = u'\u2514' # └
CNO = u'\u2518' # ┘
CBLH = u'\u2550' # ═
CBLV = u'\u2551' # ║
CPAR = u'\u2592' # ▒

- TABLERO 7x7 PARA DIBUJAR LOS BORDER

 NOTAS:
    - DIBUJA EL TABLERO
    - FALTA DIBUJAR
"""