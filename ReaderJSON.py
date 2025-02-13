import json


class Reader:
    documents_data = dict()

    @staticmethod
    def set_documents():
        """
        Функция чтения и записи файла json в переменную document_reader
        :return: Ничего
        """
        with open('./Storage/DocumentsData.json',
                  encoding="UTF-8") as file_json:
            Reader.documents_data = json.load(file_json)

    @staticmethod
    def get_documents():
        return Reader.documents_data
