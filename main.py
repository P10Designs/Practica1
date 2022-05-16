def saveRecord(movimientos, nivel):
    try:
        fichero = open("records.txt", "r")
        Lineas = fichero.readlines()
        records = []
        
        for i in Lineas:
            records.append(int(i.strip()))

        if (len(records)<=nivel):
            records.append(movimientos)
        else:
            records[nivel] = movimientos
        fichero.close()
        with open("records.txt", "w" ) as f:
            for s in records:
                f.write(str(s) +"\n")
            f.close()
            
    except:
        print('error')

def readPuntos():
    try:
        fichero = open("records.txt", "r")
        Lineas = fichero.readlines()
        records = []
        for i in Lineas:
            records.append(int(i.strip()))
        maxLevel = len(records)
    except:
        fichero = open("records.txt", "w")
        records = []
        maxLevel = len(records)
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

def selectInitial(maxLevel):
    printString = "Elija nivel (1-"+str(maxLevel+1)+"): "
    levelSelected = -1
    correct = False
    while correct == False:
        try:
            levelSelected = int(input(printString))
            if(levelSelected >= 1 and levelSelected <= (maxLevel +1)):
                correct = True
            else: 
                print("Seleccion incorrecta")
        except:
            print('ERROR TRY AGAIN')
    return levelSelected

def finish():
    playing = False
    check = True
    while check:
        text = input('Desea pasar al siguiente nivel? [S/N] ')
        if(text.upper() == 'S'):
            playing = True
            check = False
        elif (text.upper() == 'N'):
            playing = False
            check = False
        else:
            print('Error')
    
    return playing

class Coche:
    def __init__(self, string, letter):
        self.string = string
        self.direction = string[0]
        self.letter = letter
        self.posX = int(string[1])*5
        self.posY = int(string[2])*3
        self.length = int(string[3])

    def drawCar(self, tablero):
        won = False
        rangeX, rangeY = range(0,0), range(0,0)
        if (self.direction == 'H'):
            rangeY = range(self.posY, self.posY+3)
            rangeX = range(self.posX, self.posX+5*self.length)
        elif (self.direction == 'V'):
            rangeY = range(self.posY, self.posY+3*self.length)
            rangeX = range(self.posX, self.posX+5)
        for row in rangeY:
            for col in rangeX:
                if (row == self.posY):
                    if (col==self.posX):
                        tablero[row][col] = '┌'
                    elif(col==rangeX[-1]):
                        tablero[row][col] = '┐'
                    else:
                        tablero[row][col] = '─'
                elif (row == rangeY[-1]):
                    if (col==self.posX):
                        tablero[row][col] = '└'
                    elif(col==rangeX[-1]):
                        tablero[row][col] = '┘'
                    else:
                        tablero[row][col] = '─'
                elif(self.direction == 'H'):
                    if(col == self.posX +2):
                        tablero[row][col] = self.letter
                    elif(col==rangeX[-1]-2):
                        tablero[row][col] = self.letter.lower()
                    elif (col==self.posX or col==rangeX[-1]):
                        tablero[row][col] = '│'
                    else:
                        tablero[row][col] = ' '
                elif(self.direction == 'V'):
                    if (row == self.posY+1 and col == self.posX +2):
                        tablero[row][col] = self.letter
                    elif(row == rangeY[-1]-1 and col == self.posX +2):
                        tablero[row][col] = self.letter.lower()
                    elif (col==self.posX or col==rangeX[-1]):
                        tablero[row][col] = '│'
                    else:
                        tablero[row][col] = ' '
                if(self.letter == 'A' and rangeX[-1] >= len(tablero[-1])-5): won = True
        return tablero, won

    def checkMove(self, tablero, mov):
        error = False
        if(mov.lower() == mov):
            if (self.direction == 'H'):
                if(tablero[self.posY][self.posX+5*self.length+4] == ' '): error = False
                else: error = True
            if (self.direction == 'V'):
                if(tablero[self.posY+3*self.length+2][self.posX] == ' '): error = False
                else: error = True
        elif(mov.upper() == mov):
            if (self.direction == 'H'):
                if(tablero[self.posY][self.posX-5] == ' '): error = False
                else: error = True
            if (self.direction == 'V'):
                if(tablero[self.posY-3][self.posX] == ' '): error = False
                else: error = True
        return error

    def moveCar(self, mov, tablero):
        error = False
        movDone = False
        if(mov.upper() == self.letter):
            error = self.checkMove(tablero, mov)
            if (error == False):
                movDone = True
                if(mov.lower() == mov):
                    if (self.direction == 'H'):
                        self.posX += 5
                        self.lastMove = mov
                    elif (self.direction == 'V'):
                        self.posY +=3
                        self.lastMove = mov
                else:
                    if(self.direction == 'H'):
                        self.posX -= 5
                        self.lastMove = mov
                    elif (self.direction == 'V'):
                        self.posY -=3
                        self.lastMove = mov
        return error, movDone

class Nivel:
    def __init__(self, data, row, col):
        data.pop(0)
        self.row = row + 2
        self.col = col + 2
        self.cars = []
        self.tablero = []
        self.movimientos = 0
        count = 1
        for car in data:
            letter = chr(ord('@') + count)
            self.cars.append(Coche(car, letter))
            count += 1
        self.completed = False

    def drawBorder(self):
        tablero = [[' ' for c in range(self.col * 5)] for r in range(self.row * 3)]
        for rowC in range(len(tablero)):
            if(rowC < 3 or rowC >= (self.row * 3) - 3):
                for colC in range(len(tablero[rowC])):
                    tablero[rowC][colC] = '▒'
            else:
                for colC in range(len(tablero[rowC])):
                        if(colC < 5 or colC >= ((self.col * 5) - 5)):
                            if rowC >= 9 and rowC < 12:
                                if (colC < 5):
                                    tablero[rowC][colC] = '▒'
                            else:
                                tablero[rowC][colC] = '▒'
        self.tablero = tablero

    def start(self, points, level):
        movCounter = 0
        if (points == ''):
            print("NIVEL "+str(level+1)+" - NO HAY RECORD")
        else:
            print("NIVEL "+str(level+1)+" - RECORD "+str(points)+" MOVIMIENTOS")

        self.drawBorder()
        while self.completed == False:
            self.genTablero()
            self.printTablero()
            if (self.completed): break
            movimientos = input('Movimientos = ')
            for mov in movimientos:
                mainBreak = False
                for i in range(len(self.cars)):
                    error, movDone = self.cars[i].moveCar(mov, self.tablero)
                    if (error == True):
                        print('Movimiento '+ mov +' imposible por bloqueo')
                        mainBreak = True
                        break
                    self.drawBorder()
                    self.genTablero()
                    if (movDone): movCounter += 1
                    if (self.completed): mainBreak = True
                if mainBreak:
                    break
            self.drawBorder()

        self.genTablero()
        self.printTablero()
        print('ENHORABUENA, HA COMPLETADO EL NIVEL!')
        string = 'Movimientos: '+ str(movCounter)
        if (points == '' or movCounter < int(points)):
            string += ' (NUEVO RECORD!)'
            saveRecord(movCounter, level)
        print(string)

    def genTablero(self):
        won = False
        for i in range(len(self.cars)):
            self.tablero, wonReturned = self.cars[i].drawCar(self.tablero)
            if(wonReturned == True): won = True
        self.completed =  won

    def printTablero(self):
        for row in self.tablero:
            string = ""
            for cell in row:
                string += cell
            print(string)

if __name__ == "__main__":
    nNiveles, niveles  = readLevels(6, 6)
    records, maxLevel = readPuntos()
    playing = True
    level = selectInitial(maxLevel) - 1
    while playing == True:
        records, maxLevel = readPuntos()
        record = ''
        if(len(records) > level):
            record = records[level]
        niveles[level].start(record, level)
        playing = finish()
        level = level+1
        if(level > len(niveles)-1):
            print('!ENHORABUENA HAS COMPLETADO EL JUEGO¡')
            playing = False