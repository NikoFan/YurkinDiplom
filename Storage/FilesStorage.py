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
        return FilesContainer.files_container[key]


    @staticmethod
    def clear_container():
        """
        Функция очистки всего словаря
        :return: Ничего
        """
        FilesContainer.files_container = dict()


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