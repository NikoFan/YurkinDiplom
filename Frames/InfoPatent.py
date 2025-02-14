import sys
import os
from PySide6.QtWidgets import (QFrame, QWidget, QPushButton, QLabel,
                               QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea,QTextEdit)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush
from Frames import ChooseTypeOfPatent
from ReaderJSON import Reader
from Storage.UsersAction import ActionStack


# Стили для приложения


class InfoPatent(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Хранится ин используемый документ
        self.use_title = ActionStack.get_element_by_index(-2)
        self.use_topic = ActionStack.get_element_by_index(-3)
        data = Reader.get_documents() # Получение словаря с данными
        self.use_info = data[self.use_topic][self.use_title][ActionStack.get_last()]


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

        back_button = QPushButton("<-Назад")
        back_button.setObjectName("back_btn")
        back_button.clicked.connect(
            lambda: (ActionStack.pop(), self.controller.switch_frames(ChooseTypeOfPatent.ChooseTypeOfPatent))
        )
        left_side_widget_layout.addWidget(back_button, stretch=0)

        self.frame_layout.addWidget(left_side_widget)

        # Заполнение правой части окна

        # часть с прокруткой
        self.create_scrollable_area()

    def create_scrollable_area(self):
        # Создаем Scroll Area
        information_scroll = QScrollArea()
        information_scroll.setWidgetResizable(True)
        information_scroll.setViewportMargins(10, 10, 10, 10)

        # Контейнер для содержимого
        content_widget = QWidget()
        information_scroll.setWidget(content_widget)

        # Вертикальный layout
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel(self.use_title)
        title.setObjectName("title")
        title.setWordWrap(True)
        content_layout.addWidget(title)

        # Добавляем текстовое поле
        text_information = QTextEdit(self.use_info)
        text_information.setObjectName("text_information")
        text_information.setReadOnly(True)
        content_layout.addWidget(text_information)

        self.frame_layout.addWidget(information_scroll)

"""
class InfoPatentInventions(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller


        # Создание разметки фрейма
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.setup_ui()

    def setup_ui(self):
        
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
            lambda: print("Переход к предыдущему экрану")
        )
        left_side_widget_layout.addWidget(back_button, stretch=0)

        self.frame_layout.addWidget(left_side_widget)

"""