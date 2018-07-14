#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from TF_DICT import *
'''
class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No,QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif',10))

        # MENU

        openFile = QAction('&Input filename', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.showFileDialog)
        openFile.setStatusTip('Your filename here')

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)
        # INPUT
        self.btn = QPushButton('Dialog', self)
        self.btn.move(30, 70)
        self.btn.clicked.connect(self.showFileDialog)
        self.text_edit = QTextEdit(self)
        self.text_edit.move(30,100)
        # MAIN
        self.setGeometry(300,300,640,480)
        self.setWindowTitle('TF IDF')
        self.setWindowIcon(QIcon('txt-file-symbol_318-45119.jpg'))


        grid = QGridLayout()
        grid.setSpacing(10)
        reviewEdit = QTextEdit()
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        self.show()

    def showFileDialog(self):
        fnames1, ok1 = QInputDialog.getText(self, 'Input Dialog',
            'Введите названия двух файлов для анализа через пробел:')
        fnames2, ok2 = QInputDialog.getText(self, 'Input Dialog',
            'Введите названия всех файлов через пробел:')
        if ok1 and ok2:
            analysis_files_list = fnames1.split(' ')[:2]
            all_files_list = fnames2.split(' ')
            analysis_files_list.extend(all_files_list)
        try:
            self.text_edit.setText(str(tru_esimilarity(analysis_files_list)))
            self.text_edit.adjustSize()
        except FileNotFoundError:
            self.text_edit.setText('Вы выбрали файл, который невозможно обработать.')
            self.text_edit.adjustSize()
'''

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(15)

        self.firstEdit = QTextEdit(self)
        grid.addWidget(self.firstEdit, 1, 1)
        self.secondEdit = QTextEdit(self)
        grid.addWidget(self.secondEdit, 1, 2)
        button1 = QPushButton('Посчитать!')
        grid.addWidget(button1,2,1,2,1)
        self.similarity_label2 = QLabel(self)
        grid.addWidget(self.similarity_label2,2,2,2,1)
        self.setLayout(grid)

        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('TF IDF')
        self.show()

        button1.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        text1 = self.firstEdit.toPlainText()
        text2 = self.secondEdit.toPlainText()
        b = directed_tfidf_dict_high_level_with_stemming_for_two_texts_but_faster(text1,text2)
        first2 = b[0]
        second2 = b[1]
        self.similarity_label2.setText(str(true_similarity(first2,second2)))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex1 = Widget()
    sys.exit(app.exec_())
