import sys
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
                               QMessageBox)
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor
from PySide6.QtCore import Qt
from mysql_conn import MySQlConnect
from window_converte import Converter

class ConverterSheet(QMainWindow):

    def __init__(self):
        super().__init__()
        self.set_init()
        self.layout_setting()

    def set_init(self):
        self.setWindowTitle('MySQL Conversor')
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(500,500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_widget.setLayout(self.central_layout)

    def layout_setting(self):
        layout_header = QVBoxLayout()
        layout_form = QVBoxLayout()
        layout_bottom = QHBoxLayout()

        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        label_header_image = QLabel()
        pixmap_header = QPixmap()
        pixmap_header.load('img/header.jpg')
        label_header_image.setPixmap(pixmap_header)

        label_space = [QLabel() for i in range(2)]

        form_layouts_set = [QHBoxLayout() for i in range(5)]
        label_form_set = [QLabel() for i in range(5)]
        self.input_form_set = [QLineEdit() for i in range(5)]

        # FORMS ======================

        list_labels_name = ['Database','Host','Port','Username','Password']

        for i in range(5):
            self.input_form_set[i].setFixedWidth(300)
            label_form_set[i].setFixedWidth(60)

            label_form_set[i].setStyleSheet('color: white')
            self.input_form_set[i].setStyleSheet('''QLineEdit{
                                                background-color: #a5c9c7;
                                                outline: 0px;
                                            }
                                            QLineEdit:focus{
                                                border-color: white;
                                            }
                                            QLineEdit:hover{
                                                background-color: #809c9a;
                                            }
                                            ''')

            label_form_set[i].setText(list_labels_name[i])
            form_layouts_set[i].addWidget(label_form_set[i])
            form_layouts_set[i].addWidget(self.input_form_set[i])
            layout_form.addLayout(form_layouts_set[i])

        # ============================
            
        button_start_connection = QPushButton('Conectar')
        button_start_connection.setStyleSheet('''
                                    QPushButton{
                                        background-color: orange;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                   
                                    QPushButton:hover{
                                        background-color: #c27619;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                    ''')
        button_start_connection.setFixedSize(200,70)
        button_start_connection.clicked.connect(self.button_connect)

        button_close = QPushButton('Sair')
        button_close.setFixedSize(200,70)
        button_close.setStyleSheet('''
                                    QPushButton{
                                        background-color: orange;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                   
                                    QPushButton:hover{
                                        background-color: #c27619;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                    ''')
        button_close.clicked.connect(lambda: self.close())

        label_style_layout = QLabel()
        layout_buttons_label = QHBoxLayout()
        label_style_layout.setLayout(layout_buttons_label)

        label_style_layout.setObjectName('main')
        label_style_layout.setStyleSheet('''QLabel#main{
                                         background-color: orange;
                                         }''')
        label_style_layout.setFixedSize(500,200)

        layout_bottom.setContentsMargins(0,0,0,0)
        layout_buttons_label.setContentsMargins(0,0,0,39)

        layout_bottom.addWidget(label_style_layout)
        layout_buttons_label.addWidget(button_start_connection)
        layout_buttons_label.addWidget(button_close)

        layout_header.addWidget(label_header_image)
        
        self.central_layout.addLayout(layout_header)
        self.central_layout.addWidget(label_space[0])
        self.central_layout.addLayout(layout_form)
        self.central_layout.addWidget(label_space[1])
        self.central_layout.addLayout(layout_bottom)

    def button_connect(self):
        try:
            if self.input_form_set[4] != '' or self.input_form_set[4] is not None:
                self.mysql_conn = MySQlConnect(self.input_form_set[0].text(),self.input_form_set[1].text(),self.input_form_set[2].text(),self.input_form_set[3].text(),self.input_form_set[4].text())
            else:
                self.mysql_conn = MySQlConnect(self.input_form_set[0].text(),self.input_form_set[1].text(),self.input_form_set[2].text(),self.input_form_set[3].text())
            self.mysql_conn.connect_sql()

            dict_pass = {'database':self.input_form_set[0].text(),
                         'host':self.input_form_set[1].text(),
                         'port':self.input_form_set[2].text(),
                         'username':self.input_form_set[3].text(),
                         'password':self.input_form_set[4].text()}
            with open('SQL.JSON','w') as file:
                 json.dump(dict_pass , file, indent=2)

            self.window_interface = Converter()
            self.window_interface.show()

            self.close()
        except TypeError as err:
            self.show_message_box('Erro','Não foi possível conectar ao banco de dados.')
            print(err)

    def close_connection(self):
        self.mysql_conn.close_connection()
        self.close()

    def show_message_box(self, title_message, message):
        message_box = QMessageBox(self)
        message_box.setContentsMargins(0,0,28,0)
        message_box.setWindowTitle(title_message)
        message_box.setText(message)
        message_box.exec()

    def mousePressEvent(self, event):
	    self.offset = event.pos()
         
    def mouseMoveEvent(self, event):
	    self.move(self.pos() + event.pos() - self.offset)

    def paintEvent(self, event):
        painter = QPainter(self)
        grad = QLinearGradient(0,0,0,self.height())
        grad.setColorAt(0,QColor(242, 144, 24))
        painter.fillRect(self.rect(), grad)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterSheet()
    window.show()
    sys.exit(app.exec())