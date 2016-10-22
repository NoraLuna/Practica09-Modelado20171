#importamos las clases a usar
import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint

#creamos la clase principal
class MainWindow(QtGui.QMainWindow):

    #creamos el constructor de la clase
    def __init__(self):
        super(MainWindow, self).__init__()
        self.empieza_interfaz()
        self.juego_iniciado = False
        self.juego_en_pausa = False
        self.timer = None
        self.serpientes_juego = []


    #Con esta funcion inicializamos los elementos de la interfaz
    def empieza_interfaz(self):
        #llamamos la funcion .ui
        uic.loadUi('servidor.ui', self)
        self.pushButton_3.hide()
        self.cambia_tab()
        self.inicia_tabla()
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.spinBox_2.valueChanged.connect(self.actualizar_tabla)
        self.spinBox_3.valueChanged.connect(self.actualizar_tabla)
        self.spinBox.valueChanged.connect(self.actualiza_timer)
        self.pushButton_2.clicked.connect(self.inicia_juego)
        self.pushButton_3.clicked.connect(self.terminar_juego)
        self.show()
        
    #Funcion para iniciar el juego
    def inicia_juego(self):
        if not self.juego_iniciado:
            self.timer = QtCore.QTimer(self)
            self.pushButton_3.show()
            
            #Creamos a la serpiente con un color al azar
            serpiente_1 = Serpiente(randint(0,255),randint(0,255),randint(0,255))
            self.serpientes_juego.append(serpiente_1)
            self.pushButton_2.setText("Pausa")

            self.dibuja_serpientes()
            
            self.timer.timeout.connect(self.mover_serpientes)
            self.timer.start(200)
            
            self.tableWidget.installEventFilter(self) 
            self.juego_iniciado = True

        elif self.juego_iniciado and not self.juego_en_pausa:
            self.timer.stop()

            self.juego_en_pausa = True 
            self.pushButton_2.setText("Continuar")

        elif self.juego_en_pausa:
            self.timer.start()

            self.juego_en_pausa = False
            self.pushButton_2.setText("Pausa")


    #Funcion que termina el juego e inicializa las variables.
    def terminar_juego(self):        
        self.timer.stop()
        self.serpientes_juego = []
        
        self.juego_iniciado = False

        self.pushButton_3.hide()
        self.pushButton_2.setText("Inicia Juego")
        self.inicia_tabla()
    

    #Funcion para cambiar el tamao de la tabla
    def cambia_tab(self):   
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)


    #Funcion para cambiar el tiempo
    def actualiza_timer(self):        
        self.timer.setInterval(self.spinBox.value())


    #Funcion que dibuja las serpientes
    def dibuja_serpientes(self):        
        for serpiente in self.serpientes_juego:
            for seccion_corporal in serpiente.casillas:
                self.tableWidget.item(seccion_corporal[0], seccion_corporal[1]).setBackground(QtGui.QColor(serpiente.color[0], serpiente.color[1], serpiente.color[2]))


    #Usando el timer vemos si la serpiente no ha chocado consigo misma
    def choco_con_ella(self, serpiente):
        for seccion_corporal in serpiente.casillas[0:len(serpiente.casillas)-2]:
            if serpiente.casillas[-1][0] == seccion_corporal[0] and serpiente.casillas[-1][1] == seccion_corporal[1]:
                self.label_7.setStyleSheet("QLabel { color : #ff0000; }")
                #Sirve para reasignar un texto  
                QtCore.QTimer.singleShot(2000, lambda: self.label_7.setText(''))
                return True
        return False


    #Funcion para mover la serpiente
    def mover_serpientes(self):       
        for serpiente in self.serpientes_juego:
            if self.choco_con_ella(serpiente):
                self.terminar_juego()
                
            self.tableWidget.item(serpiente.casillas[0][0],serpiente.casillas[0][1]).setBackground(QtGui.QColor(255, 255, 255))
            x = 0
            
            #se van pintando las casillas para que la serpiente avance
            for t in serpiente.casillas[0: len(serpiente.casillas)-1]:
                x += 1
                t[0] = serpiente.casillas[x][0]
                t[1] = serpiente.casillas[x][1]
 
            #Se checa la direccion dada para ver cuales casillas pintara
            if serpiente.direccion is "Abajo":
                if serpiente.casillas[-1][0] + 1 < self.tableWidget.rowCount():
                    serpiente.casillas[-1][0] += 1
                else:
                    serpiente.casillas[-1][0] = 0
            if serpiente.direccion is "Derecha":
                if serpiente.casillas[-1][1] + 1 < self.tableWidget.columnCount():
                    serpiente.casillas[-1][1] += 1
                else:
                    serpiente.casillas[-1][1] = 0
            if serpiente.direccion is "Arriba":
                if serpiente.casillas[-1][0] != 0:
                    serpiente.casillas[-1][0] -= 1
                else:
                    serpiente.casillas[-1][0] = self.tableWidget.rowCount()-1
            if serpiente.direccion is "Izquierda":
                if serpiente.casillas[-1][1] != 0:
                    serpiente.casillas[-1][1] -= 1
                else:
                    serpiente.casillas[-1][1] = self.tableWidget.columnCount()-1

        self.dibuja_serpientes()
        

    #Se encarga de crear un Item en cada celda para colorear las celdas de distinto color simulando el movimiento
    def inicia_tabla(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(QtGui.QColor(255, 255, 255))



    #Funcion que para aumentar el numero de filas y columnas de la tabla.
    def actualizar_tabla(self):       
        self.tableWidget.setRowCount(self.spinBox_3.value())
        self.tableWidget.setColumnCount(self.spinBox_2.value())
        self.inicializa_tabla()



    #metodo para poder mover la serpiente con las teclas
    def eventFilter(self, source, event):        
        if event.type() == QtCore.QEvent.KeyPress and source is self.tableWidget:
                key = event.key()
                if key == QtCore.Qt.Key_Up and source is self.tableWidget:
                    for serpiente in self.serpientes_juego:
                        if serpiente.direccion is not "Abajo":
                            serpiente.direccion = "Arriba"
                elif key == QtCore.Qt.Key_Down and source is self.tableWidget:
                    for serpiente in self.serpientes_juego:
                        if serpiente.direccion is not "Arriba":
                            serpiente.direccion = "Abajo"
                elif key == QtCore.Qt.Key_Right and source is self.tableWidget:
                    for serpiente in self.serpientes_juego:
                        if serpiente.direccion is not "Izquierda":
                            serpiente.direccion = "Derecha"
                elif key == QtCore.Qt.Key_Left and source is self.tableWidget:
                    for serpiente in self.serpientes_juego:
                        if serpiente.direccion is not "Derecha":
                            serpiente.direccion = "Izquierda"
                            
        return QtGui.QMainWindow.eventFilter(self, source, event)


class Serpiente():

    def __init__(self, red, green, blue):
        self.color = (red, green, blue)
        self.tam = 8
        self.casillas = []
        for i in range(4, self.tam+4):
            self.casillas.append([i, 0])
        
        self.direccion = "Abajo"


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
