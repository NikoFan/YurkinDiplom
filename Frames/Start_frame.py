import sys
from PySide6.QtWidgets import (QFrame, QWidget, QPushButton, QLabel,
                               QVBoxLayout, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette

from Storage.UsersAction import ActionStack
from Storage.FilesStorage import FilesContainer

from Frames.ChooseTypeOfPatent import ChooseTypeOfPatent
import shutil, os # Для удаления папки


# Стили для приложения


class MainWindow(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Очистка стека с действиями
        ActionStack.clear_stack()
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

        # Создание контактов
        contacts = ["vk.com", "tg", "+79999999999"]
        for contact in contacts:
            contact_label = QLabel(contact)
            contact_label.setObjectName("contact_label")
            contact_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
            left_side_widget_layout.addWidget(contact_label, stretch=0)

        self.frame_layout.addWidget(left_side_widget)

        # Заполнение правой части окна
        right_side_widget = QWidget()
        right_side_widget_layout = QVBoxLayout(right_side_widget)
        title = QLabel("Выберите интересующий пакет документов")
        title.setObjectName("title")
        title.setWordWrap(True)

        # Создание кнопок
        registration_btn = QPushButton("Регистрация Патента")
        registration_btn.setObjectName("main_frame_btn")
        registration_btn.setFixedHeight(150)
        registration_btn.clicked.connect(
            lambda: (self.controller.switch_frames(ChooseTypeOfPatent, "Регистрация патента"))
        )

        or_label = QLabel("или")
        or_label.setObjectName("title")

        take_duplicate_btn = QPushButton("Выдача Дубликата")
        take_duplicate_btn.setObjectName("main_frame_btn")
        take_duplicate_btn.setFixedHeight(150)
        take_duplicate_btn.move(200, 0)
        take_duplicate_btn.clicked.connect(
            lambda: (self.controller.switch_frames(ChooseTypeOfPatent, "Выдача дубликата"))
        )

        right_side_widget_layout.addWidget(title)
        right_side_widget_layout.addWidget(registration_btn)
        right_side_widget_layout.addWidget(or_label)
        right_side_widget_layout.addWidget(take_duplicate_btn)
        self.frame_layout.addWidget(right_side_widget)
