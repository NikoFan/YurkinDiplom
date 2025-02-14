class FilesContainer:

    files_container = dict()

    @staticmethod
    def push(key, value):
        """
        Функция добавление элемента в словарь
        :param key: Ключ
        :param value: Путь к файлу
        :return: Ничего
        """
        FilesContainer.files_container[key] = value

    @staticmethod
    def get_element(key):
        """
        Функция для получения элемента словаря
        :param key: Ключ
        :return: Значение словаря
        """
        print(FilesContainer.files_container)
        try:
            return FilesContainer.files_container[key]
        except Exception:
            return {}

    @staticmethod
    def get_full_stack():
        return FilesContainer.files_container


    @staticmethod
    def clear_container():
        """
        Функция очистки всего словаря
        :return: Ничего
        """
        FilesContainer.files_container = dict()


    @staticmethod
    def get_stack_len():
        """
        Функция получения количества подгруженных файлов
        :return: None
        """
        return len(FilesContainer.files_container)


    @staticmethod
    def del_element(key):
        """
        Функция удаления файла из контейнера
        :param key: Ключ для удаления
        :return: Ничего
        """
        print(FilesContainer.files_container)
        del FilesContainer.files_container[key]
        print(FilesContainer.files_container)