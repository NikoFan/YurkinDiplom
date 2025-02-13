from PySide6.QtWidgets import (
    QMessageBox  # Всплывающее сообщение
)


def send_I_message(message_text: str):
    '''
    Функция создания и демонстрации Информационного сообщения
    :param message_text: Текст сообщения
    :return: UID кнопки, которую нажали
    '''
    # Создание объекта сообщение
    message = QMessageBox()
    # Установка текста
    message.setText(message_text)
    # Установка иконки ИНФОРМАЦИЯ
    message.setIcon(QMessageBox.Icon.Information)
    # Установка кнопки ДА
    message.setStandardButtons(QMessageBox.StandardButton.Yes)
    # Вывод кнопки. UID Нажатой кнопки хранится в user_result
    user_result = message.exec()
    return user_result


def send_W_message(message_text: str):
    '''
    Функция создания и демонстрации Предупреждающего сообщения
    :param message_text: Текст сообщения
    :return: UID кнопки, которую нажали
    '''
    # Создание объекта сообщение
    message = QMessageBox()
    # Установка текста
    message.setText(message_text)
    # Установка иконки ПРЕДУПРЕЖДЕНИЕ
    message.setIcon(QMessageBox.Icon.Warning)
    # Установка кнопки ДА или НЕТ
    message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    # Вывод кнопки. UID Нажатой кнопки хранится в user_result
    user_result = message.exec()
    return user_result


def send_C_message(message_text: str):
    '''
    Функция создания и демонстрации Запрещающего сообщения
    :param message_text: Текст сообщения
    :return: UID кнопки, которую нажали
    '''
    # Создание объекта сообщение
    message = QMessageBox()
    # Установка текста
    message.setText(message_text)
    # Установка иконки ЗАПРЕТ
    message.setIcon(QMessageBox.Icon.Critical)
    # Установка кнопки ДА
    message.setStandardButtons(QMessageBox.StandardButton.Yes)
    # Вывод кнопки. UID Нажатой кнопки хранится в user_result
    user_result = message.exec()
    return user_result