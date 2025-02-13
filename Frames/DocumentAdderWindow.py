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

        # Получение словаря с данными из JSON
        self.documents: dict = Reader.get_documents()
        # Получение стека с действиями пользователя
        self.full_stack = ActionStack.get_full_stack()  # -> [Регистрация, Изобретение, Шаг первый]
        # Создание переменной для хранения текущей ветки JSON файла
        self.current_JSON_brunch = self.documents

        # Перебор стека для выявления текущей ветки и шага
        for stack_element in self.full_stack:  # [Регистрация, Тип документа, Шаг первый]
            # stack_element -> Регистрация -> Изобретение -> Шаг первый
            # Перезапись текущей ветки на более точную
            self.current_JSON_brunch = self.current_JSON_brunch[stack_element]
        print(self.current_JSON_brunch)

        # Создание разметки фрейма
        self.frame_layout = QHBoxLayout(self)
        # Удаление отступов от других объектов
        self.frame_layout.setSpacing(0)
        # Удаление отступов от краев приложения
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        # Запуск генерации интерфейса
        self.setup_ui()

    def setup_ui(self):
        """
        Функция создания интерфейса
        :return: Ничего не возвращается
        """
        """Заполнение левой части"""
        left_side_widget = QWidget()  # Создание черного левого виджета
        left_side_widget.setObjectName("left_side_widget")
        left_side_widget.setFixedWidth(200)
        # Разметка виджета
        left_side_widget_layout = QVBoxLayout(left_side_widget)

        # Создание текста логотипа
        logo_text = QLabel("ПатентРу")
        logo_text.setObjectName("logo_text")
        left_side_widget_layout.addWidget(logo_text, stretch=10)

        # Создание кнопки для перехода на шаг назад
        back_button = QPushButton("<- Назад")
        back_button.setObjectName("back_btn")
        back_button.clicked.connect(
            self.update_before_step  # Действие кнопки
        )
        left_side_widget_layout.addWidget(back_button, stretch=0)
        self.frame_layout.addWidget(left_side_widget)

        # Создание кнопки для перехода на следующий шаг
        next_button = QPushButton("Далее ->")
        next_button.setObjectName("back_btn")
        next_button.clicked.connect(
            self.update_next_step  # Действие кнопки
        )
        left_side_widget_layout.addWidget(next_button, stretch=0)
        # Добавление левой панели в окно
        self.frame_layout.addWidget(left_side_widget)

        """Заполнение правой части окна"""
        right_side_widget = QWidget()
        # Разметка виджета
        right_side_widget_layout = QVBoxLayout(right_side_widget)

        # Создание заголовка
        title = QLabel(self.current_JSON_brunch["Заголовок"])
        title.setObjectName("title")
        title.setWordWrap(True)
        right_side_widget_layout.addWidget(title)

        # Создание инструкции с действиями
        instruction = QLabel(self.current_JSON_brunch["Инструкция"])
        instruction.setWordWrap(True)
        instruction.setObjectName("instruction_text")
        right_side_widget_layout.addWidget(instruction, stretch=30)

        # Создание гипер-ссылок
        try:
            # Перебор текущей ветки в разделе "Ссылки"
            for link in self.current_JSON_brunch["Ссылки"]:
                # Установка ссылки в текст
                link_href = self.current_JSON_brunch["Ссылки"][link]["url"]  # Определение ссылки
                text = self.current_JSON_brunch["Ссылки"][link]["Текст"]  # Определение текста
                link_text = QLabel(f'''<a href='{link_href}'>{text}</a>''')  # Добавление ссылки в текст
                link_text.setWordWrap(True)
                link_text.setOpenExternalLinks(True)  # Разрешение на выход в интернет

                right_side_widget_layout.addWidget(link_text)  # Установка текста в разметку
        except Exception as error:
            print(error)
            pass

        # Выгрузка примеров документов
        # Получение пути к проекту на компе пользователя
        # ---- Заменить на метод библиотеки os для получения пути. Ввод через "" ненадежен
        try:
            # Для линукса
            path = os.popen("pwd").read()[:-1]
        except Exception:
            # Для Win
            path = os.popen("echo %cd%").read()[:-1]

        # Создание области для файлов
        try:
            # Перебор текущей ветки в разделе "Файлы"
            for icon_element in self.current_JSON_brunch["Файлы"]:
                print(f"{path}/Icons/" + self.current_JSON_brunch["Файлы"][icon_element]["Иконка"])
                # Виджет для документа и кнопок
                doc_widget = QWidget()
                # Горизонтальная разметка для картинки и блока кнопок
                doc_widget_hbox = QHBoxLayout(doc_widget)
                # Добавление в горизонтальную разметку Иконки
                doc_widget_hbox.addWidget(
                    self.create_document_icon(
                        f"{path}/Icons/" + self.current_JSON_brunch["Файлы"][icon_element]["Иконка"]))

                # Виджет для блока кнопок
                vertical_buttons_block_widget = QWidget()
                # Разметка для блока кнопок
                vertical_buttons_block_layout = QVBoxLayout(
                    vertical_buttons_block_widget)  # разметка для текста документа

                # Определение названия документа
                document_name = QLabel(self.current_JSON_brunch["Файлы"][icon_element]["Название"])
                document_name.setMinimumWidth(200)
                document_name.setWordWrap(True)
                vertical_buttons_block_layout.addWidget(document_name)

                # Создание кнопки для Скачивания файла
                install_btn = QPushButton("Скачать")
                install_btn.setObjectName("install_doc_btn")
                install_btn.setAccessibleName(self.current_JSON_brunch["Файлы"][icon_element]["path"])
                install_btn.setFixedHeight(30)
                install_btn.clicked.connect(
                    self.install_file  # Действие кнопки
                )

                # Создание кнопки для загрузки файла
                upload_file_btn = QPushButton("Загрузить файл")
                upload_file_btn.setObjectName("upload_btn")
                upload_file_btn.setFixedHeight(30)
                upload_file_btn.setAccessibleName(self.current_JSON_brunch["Файлы"][icon_element]["path"])
                upload_file_btn.clicked.connect(
                    self.upload_file  # Действие кнопки
                )

                # Создание кнопки для удаления загруженного файла
                del_file_btn = QPushButton("Удалить файл")
                del_file_btn.setObjectName(self.current_JSON_brunch["Файлы"][icon_element]["path"])
                # Установка стиля, т.к. через objectName это сделать нельзя
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
                del_file_btn.setStyleSheet(del_btn_style)
                del_file_btn.setFixedHeight(30)
                del_file_btn.clicked.connect(
                    self.del_file  # Действие кнопки
                )
                # Установка НЕАКТИВНА при создании
                del_file_btn.setEnabled(False)

                # Добавление кнопок в разметку блока кнопок
                vertical_buttons_block_layout.addWidget(install_btn)
                vertical_buttons_block_layout.addWidget(upload_file_btn)
                vertical_buttons_block_layout.addWidget(del_file_btn)

                # Добавления блока кнопок в разметку блока документа
                doc_widget_hbox.addWidget(vertical_buttons_block_widget)

                # Добавление блока с документами и кнопками в правый виджет
                right_side_widget_layout.addWidget(doc_widget)

        except Exception as error:
            print(error)
            pass

        # Создание области прокрутки
        doc_scroll = QScrollArea()
        # Установка адаптивности области
        doc_scroll.setWidgetResizable(True)
        # Добавление в область виджета правой стороны
        doc_scroll.setWidget(right_side_widget)
        # Установка области прокрутки в окно
        self.frame_layout.addWidget(doc_scroll)

    def upload_file(self):
        """
        Функция добавления файла в приложение
        :return: Ничего
        """
        # Открытие проводника с файлами
        file_name, _ = QFileDialog.getOpenFileName()
        # Проверка, что пользователь выбрал файл, а не закрыл окно
        if len(file_name) > 0:
            # Получение ключа для хранения файла  в стеке
            key = self.sender().accessibleName()

            # Получение ИМЕНИ файла, а не всего пути
            # ---- ПЕРЕДЕЛАТЬ
            if len(file_name.split("/")) > 1:  # Для линукса
                replace_file_name = file_name.split("/")[-1]
            else:  # Для Win
                replace_file_name = file_name.split("\\")[-1]

            # Запись файла в папку проекта
            shutil.copy2(file_name, f"./File_Container/{replace_file_name}")
            # Запись файла в стек с файлами
            FilesContainer.push(key, value=replace_file_name)

            # Определение кнопки "Удалить", которая принадлежит файлу
            del_btn = self.findChild(QObject, key)
            # Разрешение на использование
            del_btn.setEnabled(True)

    def del_file(self):
        """
        Функция удаления файла в приложение
        :return: Ничего
        """

        # Определение ключа, который будет удален из стека
        key = self.sender().objectName()
        # Удаление файла из папки
        os.remove(f"./File_Container/{FilesContainer.get_element(key)}")
        # Удаление элемента словаря
        FilesContainer.del_element(key)
        # Запрет на использование
        self.sender().setEnabled(False)

    def install_file(self):
        """
        Функция Установки файла из ЯД
        :return: Ничего
        """
        # Получение имени устанавливаемого файла
        file_url = self.sender().accessibleName()
        # Ссылка на папку на Яндекс Диске
        folder_url = "https://disk.yandex.ru/d/fSyWuiBUbpvjeQ"

        # Создание полной ссылки для установки
        url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download' + '?public_key=' + urllib.parse.quote(
            folder_url) + '&path=/' + urllib.parse.quote(file_url)

        # Получение кода страницы
        response = requests.get(url)

        # Получение ссылки для скачивания
        download_url = response.json()['href']
        # Загрузка и сохранение файла
        download_response = requests.get(download_url)
        try:
            # Запись файла
            with open(fr"{file_url}", 'wb') as f:  # Здесь укажите нужный путь к файлу
                f.write(download_response.content)
            # Информирование пользователя об успешной установке
            send_I_message(f"Файл установлен в директории: {file_url}")
        except Exception as error:
            print(error)
            # Информирование пользователя об ошибке
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
