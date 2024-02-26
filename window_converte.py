import sys
import json
import os
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QMessageBox, QGridLayout, QFileDialog, QGroupBox, QDialog, QScrollArea)
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor
from PySide6.QtCore import Qt
from mysql_conn import MySQlConnect

class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_init()
        self.layout_setting()
        self.connect_mysql()

    def connect_mysql(self):
        if os.path.exists('SQL.JSON'):
            host_data = []
            with open('SQL.JSON','r') as file:
                result = json.load(file)
                for keys, values in result.items():
                    host_data.append(values)
                
            self.conn = MySQlConnect(host_data[0],host_data[1],host_data[2],host_data[3],host_data[4])
            self.conn.connect_sql()
            os.remove('SQL.JSON')
            self.label_status.id_var = 1
        else:
            self.label_status.id_var = 0
            self.label_status.setText('Não está conectado!')
        

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
        groups_buttons = [QGroupBox() for i in range(2)]
        layout_buttons = [QGridLayout() for i in range(2)]
        list_name_groups = [' Transferir Para o Banco de Dados ',' Exportar e Converter em ']

        for i in range(2):
             groups_buttons[i].setLayout(layout_buttons[i])
             groups_buttons[i].setTitle(list_name_groups[i])

        list_name_buttons = ['xlsx','csv']
        button_export = [QPushButton() for i in range(2)]
        button_import = [QPushButton() for i in range(2)]

        index = 0
        for i in range(list_name_buttons.__len__() ):
            button_export[index].setText(list_name_buttons[index])
            button_import[index].setText(list_name_buttons[index])

            button_export[index].setFixedSize(100,50)
            button_import[index].setFixedSize(100,50)

            button_export[index].setStyleSheet('''QPushButton{
                                                    background-color: orange;
                                                    color: white;
                                                    border: 1px solid white;
                                                }
                                               
                                               QPushButton:hover{
                                                    background-color: #c27619;
                                               }''')
            
            button_import[index].setStyleSheet('''QPushButton{
                                                    background-color: orange;
                                                    color: white;
                                                    border: 1px solid white;
                                                }
                                               
                                               QPushButton:hover{
                                                    background-color: #c27619;
                                               }''')
            
            index += 1
            
        button_export[0].clicked.connect(lambda: self.load_file('*.xlsx'))
        button_export[1].clicked.connect(lambda: self.load_file('*.csv'))

        button_import[0].clicked.connect(self.return_result)

        row = 0
        column = 0
        for i in range(list_name_groups.__len__()):
            if row > 2:
                column += 1
                row = 0

            self.central_layout.addWidget(groups_buttons[i])

            layout_buttons[0].addWidget(button_export[i],column,row,1,1)
            layout_buttons[1].addWidget(button_import[i],column,row,1,1)
            row += 1
        
        layout_warning = QHBoxLayout()

        label_img_footer = gradientLabel()
        layout_label = QHBoxLayout()
        label_img_footer.setLayout(layout_label)
        layout_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_label.setContentsMargins(0,0,0,0)
        label_space = QLabel()
        label_space_max = QLabel()
        label_space_max.setFixedWidth(200)

        self.button_exit = QPushButton('Sair')
        self.button_exit.clicked.connect(self.close_window)
        self.button_exit.setFixedSize(80,40)
        self.button_exit.setStyleSheet('''
                                    QPushButton{
                                        background-color: orange;
                                        border: 1px solid white;
                                        color: white;
                                    }
                                  
                                    QPushButton:hover{
                                        border: 1px solid white;
                                        background-color: #f7c334;
                                        color: white;
                                    }
             
                                ''')

        self.label_status = QLabel(f'Está conectado ao banco de dados!')
        self.label_status.setStyleSheet('color: white')
        label_img_footer.setFixedHeight(40)
        

        layout_warning.addWidget(label_img_footer)


        self.central_layout.setContentsMargins(15,15,15,15)
        self.central_layout.addLayout(layout_warning)
        layout_label.addWidget(label_space)
        layout_label.addWidget(self.label_status)
        layout_label.addWidget(label_space_max)
        layout_label.addWidget(self.button_exit)

    def return_result(self):
        sheet = pd.DataFrame(self.conn.consult_data(), columns=['id','nome','cpf','email','nascimento'])
        sheet = sheet.drop(columns=['id'])

        for indice, linha in sheet.iterrows():
            sheet_dict = {'nome':linha[1],'cpf':linha[2],'email':linha[3],'nascimento':linha[4]}
            sheet = pd.DataFrame(sheet_dict, index=[indice])
            
    
    def load_file(self,type_):
        file_options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", f"Arquivo {type_};;Todos os Arquivos (*)", options=file_options)
        
        if self.file_name.endswith('.xlsx'):
            self.load_sheet()

        elif self.file_name.endswith('.csv'):
            self.load_csv()

    def load_sheet(self):
        sheet = pd.read_excel(self.file_name)
        self.window_header = DialogConverter()
        self.window_header.layout_set(sheet.columns.__len__(),sheet.columns.tolist())
        self.window_header.show()


    def load_csv(self):
        csv_sheet = pd.read_excel(self.file_name)

    def close_window(self):
        self.close()

    def mousePressEvent(self, event):
	    self.offset = event.pos()

    def mouseMoveEvent(self, event):
	    self.move(self.pos() + event.pos() - self.offset)

    def paintEvent(self, event):
        painter = QPainter(self)
        grad = QLinearGradient(0,0,0,self.height())
        grad.setColorAt(0,QColor(242, 144, 24))
        painter.fillRect(self.rect(), grad)


class gradientLabel(QLabel):
    id_var = 0
    def __init__(self):
        super().__init__()
        self.id_var = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        grad = QLinearGradient(0,0,self.width(),0)
        if self.id_var == 1:
            grad.setColorAt(0,QColor('orange'))
            grad.setColorAt(1,QColor('#f7c334'))
        elif self.id_var == 0:
            grad.setColorAt(0,QColor('blue'))
            grad.setColorAt(1,QColor('cyan'))
        painter.fillRect(self.rect(), grad)

class DialogConverter(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600,500)
        self.setWindowTitle('Rótulos')
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

    def layout_set(self, range_button:int, list_name: list):
        area_scroll_header = QScrollArea()
        widget_scroll_header = QWidget(area_scroll_header)
        layout_grid_scroll = QGridLayout(widget_scroll_header)
        area_scroll_header.setWidget(widget_scroll_header)
        area_scroll_header.setWidgetResizable(True)
        self.central_layout.addWidget(area_scroll_header)
        button_head = []

        
        for i in range(range_button):
            button_ref = QPushButton()
            button_head.append(button_ref)
            button_ref.setFixedHeight(150)
        
        for i in range(button_head.__len__()):
            button_head[i].setText(list_name[i])

        row = 0
        column = 0
        for i in range(list_name.__len__()):
            if row > 2:
                column += 1
                row = 0
            layout_grid_scroll.addWidget(button_head[i],row,column,1,1)     
            row += 1
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Converter()
    window.show()
    sys.exit(app.exec())