import sys
from PySide6.QtWidgets import (QFrame, QWidget, QPushButton, QLabel,
                               QVBoxLayout, QHBoxLayout, QScrollArea,
                               QFileDialog, QTextBrowser)
from PySide6.QtCore import Qt, QRect, QObject
from PySide6.QtGui import QPixmap


import requests
import urllib.parse
from Frames import ChooseTypeOfPatent
from ReaderJSON import Reader
from Storage.UsersAction import ActionStack
import os, shutil  # Для получения пути к программе
from SendMessageBox import *
from Storage.FilesStorage import FilesContainer


# Стили для приложения


class DocumentAdderClass(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Считывание данных из JSON
        self.documents: dict = Reader.get_documents()
        print("----------------------------------------")
        self.full_stack = ActionStack.get_full_stack()  # -> [Регистрация, Изобретение, Шаг первый]
        self.current_doc_brunch = self.documents
        # [Регистрация, Тип документа, Шаг первый]
        for stack_element in self.full_stack:
            # stack_element -> Регистрация -> Изобретение -> Шаг первый
            self.current_doc_brunch = self.current_doc_brunch[stack_element]
        print(self.current_doc_brunch)

        # Создание разметки фрейма
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.setup_ui()

    def setup_ui(self):
        """
        Функция создания интерфейса
        :return: Ничего не возвращается
        """
        # Заполнение левой части
        left_side_widget = QWidget()  # Создание черного левого виджета
        left_side_widget.setObjectName("left_side_widget")
        left_side_widget.setFixedWidth(200)

        # Разметка виджета
        left_side_widget_layout = QVBoxLayout(left_side_widget)

        # Создание текста логотипа
        logo_text = QLabel("ПатентРу")
        logo_text.setObjectName("logo_text")
        left_side_widget_layout.addWidget(logo_text, stretch=10)

        back_button = QPushButton("<- Назад")
        back_button.setObjectName("back_btn")
        back_button.clicked.connect(
            self.update_before_step
        )
        left_side_widget_layout.addWidget(back_button, stretch=0)

        self.frame_layout.addWidget(left_side_widget)
        next_button = QPushButton("Далее ->")
        next_button.setObjectName("back_btn")
        next_button.clicked.connect(
            self.update_next_step
        )
        left_side_widget_layout.addWidget(next_button, stretch=0)

        self.frame_layout.addWidget(left_side_widget)

        # Заполнение правой части окна
        right_side_widget = QWidget()
        right_side_widget_layout = QVBoxLayout(right_side_widget)

        title = QLabel(self.current_doc_brunch["Заголовок"])
        title.setObjectName("title")
        title.setWordWrap(True)
        right_side_widget_layout.addWidget(title)

        instruction = QLabel(self.current_doc_brunch["Инструкция"])
        instruction.setWordWrap(True)
        instruction.setObjectName("instruction_text")
        right_side_widget_layout.addWidget(instruction, stretch=30)
        try:
            for link in self.current_doc_brunch["Ссылки"]:
                print("link:", link)
                # Установка ссылки в текст
                link_href = self.current_doc_brunch["Ссылки"][link]["url"] # Определение ссылки
                text = self.current_doc_brunch["Ссылки"][link]["Текст"] # Определение текста
                link_text = QLabel(f'''<a href='{link_href}'>{text}</a>''') # Добавление ссылки в текст
                link_text.setWordWrap(True)
                link_text.setOpenExternalLinks(True) # Разрешение на выход в интернет

                right_side_widget_layout.addWidget(link_text) # Установка текста в разметку
        except Exception as error:
            print(error)
            pass

        # Выгрузка примеров документов
        # Создание иконки
        try:
            # Для линукса
            path = os.popen("pwd").read()[:-1]
        except Exception:
            # Для Win
            path = os.popen("echo %cd%").read()[:-1]

        try:
            for icon_element in self.current_doc_brunch["Файлы"]:
                print(f"{path}/Icons/" + self.current_doc_brunch["Файлы"][icon_element]["Иконка"])
                # Виджет для документов
                doc_widget = QWidget()
                # Горизонтальная разметка для картинки
                doc_widget_hbox = QHBoxLayout(doc_widget)
                doc_widget_hbox.addWidget(
                    self.create_document_icon(
                        f"{path}/Icons/" + self.current_doc_brunch["Файлы"][icon_element]["Иконка"]))

                vertical_widget = QWidget()
                vertical_text_layout = QVBoxLayout(vertical_widget)  # разметка для текста документа

                doc_text = QLabel(self.current_doc_brunch["Файлы"][icon_element]["Название"])
                doc_text.setMinimumWidth(200)
                doc_text.setWordWrap(True)
                vertical_text_layout.addWidget(doc_text)

                # Кнопка установки
                install_btn = QPushButton("Скачать")
                install_btn.setObjectName("install_doc_btn")
                install_btn.setAccessibleName(self.current_doc_brunch["Файлы"][icon_element]["path"])
                install_btn.setFixedHeight(30)
                install_btn.clicked.connect(
                    self.install_file
                )

                upload_file_btn = QPushButton("Загрузить файл")
                upload_file_btn.setObjectName("upload_btn")
                upload_file_btn.setFixedHeight(30)
                upload_file_btn.setAccessibleName(self.current_doc_brunch["Файлы"][icon_element]["path"])
                upload_file_btn.clicked.connect(
                    self.upload_file
                )

                self.del_file_btn = QPushButton("Удалить файл")
                self.del_file_btn.setObjectName(self.current_doc_brunch["Файлы"][icon_element]["path"])
                # Установка стиля, т.к. через objectNameэто сдлеать нельзя
                del_btn_style = """
QPushButton {
background: #972b2b;
color: white;
font-size: 16px;
}

QPushButton:hover{
background: #972b2b;
color: white;
font-size: 20px;
font-weight: bold;
}

                """
                self.del_file_btn.setStyleSheet(del_btn_style)
                self.del_file_btn.setFixedHeight(30)
                self.del_file_btn.clicked.connect(
                    self.del_file
                )
                self.del_file_btn.setEnabled(False)

                vertical_text_layout.addWidget(install_btn)
                vertical_text_layout.addWidget(upload_file_btn)
                vertical_text_layout.addWidget(self.del_file_btn)

                doc_widget_hbox.addWidget(vertical_widget)

                right_side_widget_layout.addWidget(doc_widget)

        except Exception as error:
            print("---", error)
            pass

        doc_scroll = QScrollArea()
        doc_scroll.setWidgetResizable(True)
        doc_scroll.setWidget(right_side_widget)
        self.frame_layout.addWidget(doc_scroll)

    def upload_file(self):
        """
        Функция добавления файла в приложение
        :return: Ничего
        """

        file_name, _ = QFileDialog.getOpenFileName()
        if len(file_name) > 0:
            key = self.sender().accessibleName()
            # Перемещение файла в папку для хранения
            if len(file_name.split("/")) > 1:
                replace_file_name = file_name.split("/")[-1]
            else:
                replace_file_name = file_name.split("\\")[-1]
            shutil.copy2(file_name, f"./File_Container/{replace_file_name}")
            FilesContainer.push(key, value=replace_file_name)

            del_btn = self.findChild(QObject, key)

            del_btn.setEnabled(True)

    def del_file(self):
        """
        Функция удаления файла в приложение
        :return: Ничего
        """

        key = self.sender().objectName()
        os.remove(f"./File_Container/{FilesContainer.get_element(key)}")
        FilesContainer.del_element(key)

        self.sender().setEnabled(False)

    def install_file(self):
        """
        Функция Установки файла из ЯД
        :return: Ничего
        """
        file_url = self.sender().accessibleName()
        folder_url = "https://disk.yandex.ru/d/fSyWuiBUbpvjeQ"

        url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download' + '?public_key=' + urllib.parse.quote(
            folder_url) + '&path=/' + urllib.parse.quote(file_url)

        response = requests.get(url)
        download_url = response.json()['href']
        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)
        try:
            with open(fr"{file_url}", 'wb') as f:  # Здесь укажите нужный путь к файлу
                f.write(download_response.content)
            send_I_message(f"Файл установлен в директории: {file_url}")
        except Exception as error:
            print(error)
            send_W_message(f"Ошибка установки файла")

    def update_next_step(self):
        """
        Функция обновления следующего шага в стеке
        :return: Ничего не возвращается
        """
        # Обновление шага
        last_step = ActionStack.get_last()  # -> получаем Действующий шаг
        last_step = last_step.split(" ")  # -> "Шаг 1" -> ['Шаг', '1']
        num_of_step = int(last_step[-1])  # -> num_of_step = 1

        # Получение максимального количества шагов для операции
        current_len = len(self.documents[self.full_stack[0]][
                              self.full_stack[1]]) - 1  # -> Информация тоже попадает в список, ее удаляем

        if num_of_step + 1 > current_len:
            # Переход на Последнее окно -> Создание архива
            ...
        elif (num_of_step + 1) in range(2, current_len + 1):
            num_of_step += 1  # -> num_of_step = 2
            next_step = f"{last_step[0]} {num_of_step}"
            ActionStack.change_step(next_step)

            self.controller.switch_frames(DocumentAdderClass, "--change--")

    def update_before_step(self):
        """
        Функция обновления следующего шага в стеке
        :return: Ничего не возвращается
        """
        # Обновление шага
        last_step = ActionStack.get_last()  # -> получаем Действующий шаг
        last_step = last_step.split(" ")  # -> "Шаг 1" -> ['Шаг', '1']
        num_of_step = int(last_step[-1])  # -> num_of_step = 1

        if num_of_step - 1 > 0:
            num_of_step -= 1
            next_step = f"{last_step[0]} {num_of_step}"
            ActionStack.change_step(next_step)
            self.controller.switch_frames(DocumentAdderClass, "--change--")
        elif num_of_step - 1 <= 0:
            # Переход на окно выбора документов
            ActionStack.pop()
            self.controller.switch_frames(ChooseTypeOfPatent.ChooseTypeOfPatent)

    def create_document_icon(self, path: str):
        """
        Паттерн по созданию иконки документа
        :param path: Путь к иконке на локальной машине
        :return: QLabel() -> В котором лежит иконка 104х104
        """
        icon_socket = QLabel()
        icon = QPixmap(path)
        icon_socket.setFixedSize(104, 104)
        icon_socket.setScaledContents(True)
        icon_socket.setPixmap(icon)

        return icon_socket
