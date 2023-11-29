#Conectar Base de datos

import pyodbc
try:
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=COMPUTER\SQL2012;DATABASE=PLANILLA;UID=sa;PWD=sistemas')
    print('Conexión exitosa')
except Exception as ex:
    print(ex)



import sys
from PyQt5 import uic, QtWidgets

qtCreatorFile = "boleta.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.cboArea.currentIndexChanged.connect(self.precios)
        self.btnCalcular.clicked.connect(self.calcular)
        self.btnNuevo.clicked.connect(self.refrescar)
        self.btnRegistrar.clicked.connect(self.registrar)
        self.btnSalir.clicked.connect(self.salir)

    def precios(self):
        posicion = self.cboArea.currentIndex()
        lista_precios = [21, 19.50, 17, 10]
        if posicion == 1:
            self.precio_hora = lista_precios[0]
        elif posicion == 2:
            self.precio_hora = lista_precios[1]
        elif posicion == 3:
            self.precio_hora = lista_precios[2]
        elif posicion == 4:
            self.precio_hora = lista_precios[3]
        else:
            self.precio_hora = 0
        self.txtPagoHora.setText(str(self.precio_hora))



    def calcular(self):
        nro_horas = int(self.txtNroHoras.text())
        sueldo_bruto = int(self.precio_hora * nro_horas)
        self.txtSueldoBruto.setText(str(sueldo_bruto))

        if sueldo_bruto > 2500:
            descuento = sueldo_bruto * 0.20
        else:
            descuento = sueldo_bruto * 0.15
            self.txtDescuento.setText(str(descuento))

            sueldo_total = sueldo_bruto - descuento
            self.txtSueldoTotal.setText(str(sueldo_total))


    def refrescar(self):
        self.txtPagoHora.clear()
        self.txtNroHoras.clear()
        self.txtSueldoBruto.clear()
        self.txtDescuento.clear()
        self.txtSueldoTotal.clear()
        self.txtEmpleado.clear()

    def registrar(self):
        empleado = self.txtEmpleado.text()
        cargo = self.cboArea.currentText()
        pago_hora = float(self.txtPagoHora.text())
        nro_horas = float(self.txtNroHoras.text())
        sueldo_bruto = float(self.txtSueldoBruto.text())
        descuento = float(self.txtDescuento.text())
        sueldo_total = float(self.txtSueldoTotal.text())


        cursorInsert = connection.cursor()
        query = 'INSERT INTO boleta_pago (empleado, cargo, pago_hora, nro_horas, sueldo_bruto, descuento, sueldo_total) VALUES(?,?,?,?,?,?,?)'
        cursorInsert.execute(query,(empleado, cargo, pago_hora, nro_horas, sueldo_bruto, descuento, sueldo_total))
        QtWidgets.QMessageBox.information(self, 'Registro de empleados', 'Se registró el empleado: ' + empleado)
        connection.commit()
        cursorInsert.close()

    def salir(self):
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())