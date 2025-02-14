# app.py
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QApplication
)
from PySide6.QtCore import QSize

from ReaderJSON import Reader
from Storage.UsersAction import ActionStack
from SendMessageBox import send_W_message

import sys
from Frames.Start_frame import MainWindow  # Исправленный импорт


class MainApplicationClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мастер Подачи Документов")
        self.resize(900, 600)
        self.setMinimumSize(700, 550)
        # Чтение JSON файла с данными
        Reader.set_documents()

        print(Reader.get_documents())
        # Создание контейнера для фреймов
        self.frames_container = QStackedWidget()
        # Добавление второго фрейма (страница подачи документов на патент)
        patent_frame = MainWindow(self)
        self.frames_container.addWidget(patent_frame)

        self.setCentralWidget(self.frames_container)

    def switch_frames(self, frame_name, action: str = None):
        if action == "--change--":
            pass
        elif action:
            ActionStack.push(action)
        elif action == None:
            ActionStack.pop()
        current_frame = frame_name(self)
        self.frames_container.removeWidget(current_frame)
        self.frames_container.addWidget(current_frame)
        self.frames_container.setCurrentWidget(current_frame)

    def closeEvent(self, event):
        """
        Функция контролирует закрытие приложения. Это системная встроенная функция
        :param event: Закрытие окна
        :return: Ничего
        """
        if send_W_message("вы точно хотите выйти из приложения?") < 20_000:
            event.accept()
        else:
            event.ignore()




# Стили для приложения
styles_sheet = '''
QWidget {
    background-color: white;
}

QMessageBox QLabel {
color: black;
background: white;
}

QMessageBox QPushButton {
color: black;
background: white;
}

QMessageBox {
background: white;
}

QMessageBox QIcon {
background: white;
}

QLabel {
color: black;
}

QPushButton {
border: none;
}

#text_information {
color: black;
font-size: 20px;
}

#instruction_text {
color: black;
qproperty-alignment: AlignTop;
font-size: 18px;
}

#circle_label {
background-color: #2E86C1;
border-radius: 25px;
color: white;
font-size: 24px;
font-weight: bold;
border: 2px solid #1B4F72;
}

#logo_text {
color: #FFFFFF;
font-size: 34px;
qproperty-alignment: AlignCenter;
font-weight: bold;
background: none;
}

#contact_label {
color: #FFFFFF;
font-size: 20px;
background: none;
font-weight: bold;
}

#back_btn {
color: white;
font-size: 25px;
border: None;
background: black;
margin: 20px;
}

#file_name {
color: black;
font-size: 20px;
background: none;
}

#icon_socket{
background: none;
}

#link_text {
font-style: italic;
font-size: 18px;
background: none;
qproperty-alignment: AlignRight;
}

#files_widget {
background: #f0f0f0;
}

#back_btn:hover {
color: white;
font-size: 30px;
border: None;
background: black;
font-weight: bold;
margin: 20px;
}

QTextEdit {
background: white;
border: none;
padding: 15px;
font-size: 20px;
line-height: 1.5;
}

#document_name {
color: #000000;
font-size: 20px;
font-style: italic;
background: none;
}

#title {
color: #000000;
font-size: 40px;
font-weight: bold;
background: none;
qproperty-alignment: AlignCenter;
}

#main_frame_btn {
background: black;
color: #ffffff;
font-size: 30px;
border-radius: 20px;
}

#left_side_widget {
background: #000000;
border-top-right-radius: 20px;
border-bottom-right-radius: 20px;
}

#upload_btn {
background: #5bbd42;
color: white;
font-size: 16px;
}

#upload_btn:hover{
background: #5bbd42;
color: white;
font-size: 20px;
font-weight: bold;
}

#install_doc_btn {
background: #000000;
color: #FFFFFF;
font-size: 16px;
}

#install_doc_btn:hover {
background: black;
color: white;
font-size: 20px;
font-weight: bold;
}

'''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Применение стилей
    app.setStyleSheet(styles_sheet)
    window = MainApplicationClass()
    window.show()
    app.exec()
