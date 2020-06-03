# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Diseno.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox, QFileDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(903, 481)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 431, 391))
        self.groupBox.setObjectName("groupBox")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(10, 20, 411, 361))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 407, 357))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 411, 361))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(9)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(460, 10, 431, 391))
        self.groupBox_2.setObjectName("groupBox_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox_2)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 20, 411, 361))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 407, 357))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.textBrowser = QtWidgets.QTextBrowser(
            self.scrollAreaWidgetContents_2)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 411, 361))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(8)
        self.textBrowser.setFont(font)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setPlaceholderText("")
        self.textBrowser.setObjectName("textBrowser")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(50, 410, 91, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 410, 75, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 410, 47, 14))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 903, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuEjecutar = QtWidgets.QMenu(self.menubar)
        self.menuEjecutar.setObjectName("menuEjecutar")
        self.menuEjecutar_Ascendente = QtWidgets.QMenu(self.menuEjecutar)
        self.menuEjecutar_Ascendente.setObjectName("menuEjecutar_Ascendente")
        self.menuReportes = QtWidgets.QMenu(self.menuEjecutar)
        self.menuReportes.setObjectName("menuReportes")
        self.menuOpciones = QtWidgets.QMenu(self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNuevo = QtWidgets.QAction(MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_como.setObjectName("actionGuardar_como")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionEjecutar_Descendente = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Descendente.setObjectName(
            "actionEjecutar_Descendente")
        self.actionCambiar_color = QtWidgets.QAction(MainWindow)
        self.actionCambiar_color.setObjectName("actionCambiar_color")
        self.actionQuitar_numeros = QtWidgets.QAction(MainWindow)
        self.actionQuitar_numeros.setObjectName("actionQuitar_numeros")
        self.actionAcerca_de = QtWidgets.QAction(MainWindow)
        self.actionAcerca_de.setObjectName("actionAcerca_de")
        self.actionEjecutar_Todo = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Todo.setObjectName("actionEjecutar_Todo")
        self.actionErrores = QtWidgets.QAction(MainWindow)
        self.actionErrores.setObjectName("actionErrores")
        self.actionEjecutar_Todo_2 = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Todo_2.setObjectName("actionEjecutar_Todo_2")
        self.actionTabla_de_Simbolos = QtWidgets.QAction(MainWindow)
        self.actionTabla_de_Simbolos.setObjectName("actionTabla_de_Simbolos")
        self.actionAST = QtWidgets.QAction(MainWindow)
        self.actionAST.setObjectName("actionAST")
        self.actionGramatical = QtWidgets.QAction(MainWindow)
        self.actionGramatical.setObjectName("actionGramatical")
        self.actionErrores_2 = QtWidgets.QAction(MainWindow)
        self.actionErrores_2.setObjectName("actionErrores_2")
        self.actionEjecutar_Todo_3 = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Todo_3.setObjectName("actionEjecutar_Todo_3")
        self.actionEjecutar_Linea_a_Linea_Debug = QtWidgets.QAction(MainWindow)
        self.actionEjecutar_Linea_a_Linea_Debug.setObjectName(
            "actionEjecutar_Linea_a_Linea_Debug")
        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_como)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionSalir)
        self.menuEjecutar_Ascendente.addAction(self.actionEjecutar_Todo_3)
        self.menuEjecutar_Ascendente.addAction(
            self.actionEjecutar_Linea_a_Linea_Debug)
        self.menuReportes.addAction(self.actionTabla_de_Simbolos)
        self.menuReportes.addAction(self.actionAST)
        self.menuReportes.addAction(self.actionGramatical)
        self.menuReportes.addAction(self.actionErrores_2)
        self.menuEjecutar.addAction(self.menuEjecutar_Ascendente.menuAction())
        self.menuEjecutar.addAction(self.actionEjecutar_Descendente)
        self.menuEjecutar.addSeparator()
        self.menuEjecutar.addAction(self.menuReportes.menuAction())
        self.menuOpciones.addAction(self.actionCambiar_color)
        self.menuOpciones.addAction(self.actionQuitar_numeros)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuEjecutar.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.settingEvents()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Archivo"))
        self.textEdit.setPlaceholderText(
            _translate("MainWindow", "Tu código Augus aquí."))
        self.groupBox_2.setTitle(_translate("MainWindow", "Consola"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Fixedsys\'; font-size:8pt; font-weight:400; font-style:normal;\" bgcolor=\"#2d3436\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#dfe6e9;\">¡Hola, Programador! Aquí verás la salida de tu código Augus...</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Siguiente Linea"))
        self.pushButton_2.setText(_translate("MainWindow", "Detener"))
        self.label.setText(_translate("MainWindow", "Debug:"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuEjecutar.setTitle(_translate("MainWindow", "Ejecutar"))
        self.menuEjecutar_Ascendente.setTitle(
            _translate("MainWindow", "Ejecutar Ascendente"))
        self.menuReportes.setTitle(_translate("MainWindow", "Reportes"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Opciones"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(
            _translate("MainWindow", "Guardar como"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))
        self.actionEjecutar_Descendente.setText(
            _translate("MainWindow", "Ejecutar Descendente"))
        self.actionCambiar_color.setText(
            _translate("MainWindow", "Cambiar color"))
        self.actionQuitar_numeros.setText(
            _translate("MainWindow", "Quitar numeros"))
        self.actionAcerca_de.setText(_translate("MainWindow", "Acerca de"))
        self.actionEjecutar_Todo.setText(
            _translate("MainWindow", "Ejecutar Todo"))
        self.actionErrores.setText(_translate("MainWindow", "Errores"))
        self.actionEjecutar_Todo_2.setText(
            _translate("MainWindow", "Ejecutar Todo"))
        self.actionTabla_de_Simbolos.setText(
            _translate("MainWindow", "Tabla de Simbolos"))
        self.actionAST.setText(_translate("MainWindow", "AST"))
        self.actionGramatical.setText(_translate("MainWindow", "Gramatical"))
        self.actionErrores_2.setText(_translate("MainWindow", "Errores"))
        self.actionEjecutar_Todo_3.setText(
            _translate("MainWindow", "Ejecutar Todo"))
        self.actionEjecutar_Linea_a_Linea_Debug.setText(
            _translate("MainWindow", "Ejecutar Linea a Linea (Debug)"))

    def settingEvents(self):
        self.actual_file_route = ""
        # Widget operations by binding signals
        self.actionNuevo.triggered.connect(self.newFile)
        self.actionAbrir.triggered.connect(self.openFile)
        self.actionGuardar.triggered.connect(self.saveFile)
        self.actionGuardar_como.triggered.connect(self.saveFileAs)
        self.actionSalir.triggered.connect(self.closeAndExit)

    def newFile(self):
        msgBox = QMessageBox()
        msgBox.setText("¿Deseas guardar el documento que estabas trabajando?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        choosen_option = msgBox.exec()
        if(choosen_option == QMessageBox.Save):
            self.saveFile()    
        elif(choosen_option == QMessageBox.Discard):
            '''Discard changes'''
            self.discardChanges()
        elif(choosen_option == QMessageBox.Cancel):
            '''Does nothing'''
    
    def discardChanges(self):
        self.textEdit.setText("")
        self.textBrowser.setText("")

    def openFile(self):
        try:
            selected_files = QFileDialog.getOpenFileName(
                None, 'Abrir Archivo', None, "Archivos TXT (*.txt)")
            opened_file = open(selected_files[0], "r")
            value = opened_file.read()
            opened_file.close()
            self.textEdit.setText(value)
            self.actual_file_route = selected_files[0]
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setText("No se seleccionó ningún documento.")
            msgBox.exec()

    def saveFile(self):
        if(len(self.actual_file_route) > 0):
            try:
                saved_file = open(self.actual_file_route, "w")
                saved_file.write(self.textEdit.toPlainText())
                saved_file.close()
                return True
            except FileNotFoundError:
                msgBox = QMessageBox()
                msgBox.setText("No se seleccionó ningún documento.")
                msgBox.exec()
                return False
        else:
            return self.saveFileAs()

    def saveFileAs(self):
        try:
            saved_file_name = QFileDialog.getSaveFileName(
                None, "Guardar Archivo", None, "Archivos TXT (*.txt)")
            saved_file = open(saved_file_name[0], "w")
            saved_file.write(self.textEdit.toPlainText())
            saved_file.close()
            self.actual_file_route = saved_file_name[0]
            return True
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setText("No se seleccionó ningún documento.")
            msgBox.exec()
            return False
    def closeAndExit(self):
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
