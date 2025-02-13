import sys
from PySide6.QtWidgets import (QFrame, QWidget, QPushButton, QLabel,
                               QVBoxLayout, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush

from Frames import Start_frame, DocumentAdderWindow
from ReaderJSON import Reader
from Storage.UsersAction import ActionStack
from Frames.InfoPatent import InfoPatent
import os, shutil
from Storage.FilesStorage import FilesContainer


# Стили для приложения


class ChooseTypeOfPatent(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # очистка папки с файлами для новых действий пользователя
        try:
            shutil.rmtree("./File_Container")
            os.mkdir('./File_Container')
        except Exception:
            os.mkdir('./File_Container')
        # Очистка стека с файлами
        FilesContainer.clear_container()
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
            lambda: self.controller.switch_frames(Start_frame.MainWindow)
        )
        left_side_widget_layout.addWidget(back_button, stretch=0)

        self.frame_layout.addWidget(left_side_widget)

        # Заполнение правой части окна
        right_side_widget = QWidget()
        right_side_widget_layout = QVBoxLayout(right_side_widget)

        title = QLabel("Выберите интересующую категорию подачи документов")
        title.setObjectName("title")
        title.setWordWrap(True)
        right_side_widget_layout.addWidget(title, stretch=0)

        topic: dict = Reader.get_documents()
        print("--", topic)
        for value in topic[ActionStack.get_last()]:
            print(value)
            # Кнопка "Изобретение" с кругом справа
            invention_layout = QHBoxLayout()  # Горизонтальная разметка для кнопки и круга
            main_btn = QPushButton(value)
            main_btn.setObjectName("main_frame_btn")
            main_btn.setAccessibleName(value)
            main_btn.setFixedHeight(150)
            main_btn.clicked.connect(
                self.update_stac_for_action
            )
            invention_layout.addWidget(main_btn)

            # Создание круга
            information_btn = QPushButton("i")  # Текст внутри круга
            information_btn.setFixedSize(50, 50)
            information_btn.setObjectName("circle_label")
            information_btn.setAccessibleName(value)
            information_btn.clicked.connect(
                self.update_stack
            )
            invention_layout.addWidget(information_btn)

            right_side_widget_layout.addLayout(invention_layout)  # Добавляем горизонтальную разметку

        self.frame_layout.addWidget(right_side_widget)

    def update_stack(self):
        """
        Функция записи AccessibleName ы Стек
        :return: Ничего
        """
        sender = self.sender()
        ActionStack.push(sender.accessibleName())
        self.controller.switch_frames(InfoPatent, "Информация")

    def update_stac_for_action(self):
        """
        Функция записи AccessibleName ы Стек
        :return: Ничего
        """
        sender = self.sender()
        ActionStack.push(sender.accessibleName())
        self.controller.switch_frames(DocumentAdderWindow.DocumentAdderClass, "Шаг 1")
