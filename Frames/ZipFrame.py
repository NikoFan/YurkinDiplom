from PySide6.QtWidgets import (QFrame, QWidget, QPushButton, QLabel,
                               QVBoxLayout, QHBoxLayout, QScrollArea,
                               QFileDialog, QTextBrowser)
from PySide6.QtCore import Qt, QRect, QObject
from PySide6.QtGui import QPixmap

from Frames import ChooseTypeOfPatent, DocumentAdderWindow
from ReaderJSON import Reader
from Storage.UsersAction import ActionStack
import os, shutil  # Для получения пути к программе
from SendMessageBox import *
from Storage.FilesStorage import FilesContainer


class ZipClass(QFrame):
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
        print("--", self.current_JSON_brunch)

        # Создание переменной - разрешения на создание архива
        self.zip_create_license: bool = False

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
        # Добавление левой панели в окно
        self.frame_layout.addWidget(left_side_widget)

        """Заполнение правой части окна"""
        right_side_widget = QWidget()
        # Разметка виджета
        right_side_widget_layout = QVBoxLayout(right_side_widget)

        # Заголовок окна
        title = QLabel("Создайте архив документов")
        title.setObjectName("title")

        text_hbox = QHBoxLayout()  # Разметка для текста "Список файлов          0/10"
        file_list = QLabel("Список добавленных файлов")
        # Получение количества подгруженных файлов
        exist_files = FilesContainer.get_stack_len()  # Количество подгруженных файлов
        max_count_files = self.current_JSON_brunch["Количество"]  # Требуемое количество
        zip_name = self.current_JSON_brunch["Название"]

        # Если количество подгруженных == требуемому количеству
        if max_count_files == exist_files:
            self.zip_create_license = True

        # Создание текстового поля с соотношением
        file_count = QLabel(f"{exist_files}/{max_count_files}")
        file_count.setAlignment(Qt.AlignmentFlag.AlignRight)

        text_hbox.addWidget(file_list)
        text_hbox.addWidget(file_count)

        # Область прокрутки, в которой будет вся информация
        information_scroll_area = QScrollArea()
        information_scroll_area.setWidgetResizable(True)

        # Заполнение области прокрутки
        # Контейнер виджетов для ScrollArea
        scroll_area_files_container = QWidget()
        # Разметка контейнера
        scroll_area_files_container_layout = QVBoxLayout(scroll_area_files_container)
        try:
            # Для линукса
            self.path = os.popen("pwd").read()[:-1]
        except Exception:
            # Для Win
            self.path = os.popen("echo %cd%").read()[:-1]
        for file_key, file_value in FilesContainer.get_full_stack().items():
            files_widget = QWidget()
            files_widget.setObjectName("files_widget")
            files_widget.setFixedHeight(80)
            file_hbox = QHBoxLayout(files_widget)
            if file_value.split(".")[-1] not in ["pdf", "docx", "doc"]:
                icon = self.create_document_icon(
                    f"{self.path}/Icons/wrong_icon.png"
                )
            else:
                icon = self.create_document_icon(
                    f"{self.path}/Icons/" + file_value.split(".")[-1] + "_icon.png"
                )
            file_hbox.addWidget(icon)
            # Имя файла в области прокрутки
            file_name = QLabel(file_value)
            file_name.setWordWrap(True)
            file_name.setObjectName("file_name")

            file_hbox.addWidget(file_name)
            scroll_area_files_container_layout.addWidget(files_widget)

        # Все элементы ScrollArea будут сверху, независимо от количества
        scroll_area_files_container_layout.addStretch()

        # Добавление контейнера в область прокрутки
        information_scroll_area.setWidget(scroll_area_files_container)

        # Добавление элементов в правый виджет
        right_side_widget_layout.addWidget(title)
        right_side_widget_layout.addLayout(text_hbox)
        right_side_widget_layout.addWidget(information_scroll_area)

        # Создание кнопки для архивации
        zip_create = QPushButton(f"Создать {zip_name}.zip")
        zip_create.setFixedHeight(40)
        zip_create.clicked.connect(
            lambda : shutil.make_archive(zip_name, 'zip', r'./File_Container')
        )
        if self.zip_create_license:
            zip_create.setEnabled(True)
            zip_create.setStyleSheet("""
            QPushButton {
            background: #5bbd42;
            border: none;
            color: white;
            font-size: 18px;
            }
            
            QPushButton:hover {
            background: #5bbd42;
            border: none;
            color: white;
            font-size: 20px;
            font-weight: bold;
            }
            """)

        else:
            zip_create.setEnabled(False)
            zip_create.setStyleSheet("""
            QPushButton {
            background: gray;
            border: none;
            color: white;
            font-size: 18px;
            }
            """)
        right_side_widget_layout.addWidget(zip_create)


        self.frame_layout.addWidget(right_side_widget)

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
            self.controller.switch_frames(DocumentAdderWindow.DocumentAdderClass, "--change--")
        elif num_of_step - 1 <= 0:
            # Переход на окно выбора документов
            if send_W_message(
                    "Вы точно хотите вернуться к выбору документа? Все загруженные документы будут удалены!") < 20_000:
                ActionStack.pop()
                self.controller.switch_frames(ChooseTypeOfPatent.ChooseTypeOfPatent)

    def create_document_icon(self, path: str, w: int = 52, h: int = 52):
        """
        Паттерн по созданию иконки документа
        :param path: Путь к иконке на локальной машине
        :return: QLabel() -> В котором лежит иконка 104х104
        """
        icon_socket = QLabel()
        icon_socket.setObjectName("icon_socket")
        icon = QPixmap(path)
        icon_socket.setFixedSize(w, h)
        icon_socket.setScaledContents(True)
        icon_socket.setPixmap(icon)

        return icon_socket
