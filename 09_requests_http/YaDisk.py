import requests as r
import os


class YaUploader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.folder_name = os.path.basename(file_path)
        self.URL = f"https://cloud-api.yandex.net/v1/disk/resources?path={self.folder_name}"
        self.headers = {"port": "443", "Authorization": f"OAuth {token}"}
        test = r.get(self.URL, headers=self.headers)
        if test.status_code == 404:
            creator = YaUploader.create_folder(self)
            if creator[0] == 201:
                print(f'Папка "{self.folder_name}" успешно создана на Яндекс.Диске')
                print()
            else:
                print(creator)
                print()
        elif test.status_code == 200:
            print(f'Папка "{self.folder_name}" уже существует на Яндекс.Диске')
            print()
        else:
            print(test)

    def _get_files_from_folder(self) -> list:
        """Метод получает список файлов из каталога по пути self.file_path и возвращает список файлов для дальнейшей
        работы """
        return os.listdir(self.file_path)

    def upload(self):
        """Метод загруджает файлы по списку file_list на яндекс диск"""
        file_list = YaUploader._get_files_from_folder(self)
        message = str

        for file in file_list:
            try:
                params = {"path": f"{self.folder_name}/{file}"}
                full_path = os.path.join(self.file_path, file)
                upload_url = r.get(f"https://cloud-api.yandex.net/v1/disk/resources/upload", params=params,
                                   headers=self.headers).json()["href"]
                with open(full_path, "rb") as f:
                    r.put(upload_url, data=f)
                    print(f'Файл "{file}" успешно загружен на Яндекс.Диск')
                message = f"\n======\n\n" \
                          f"Все файлы из папки {self.folder_name} успешно загружены на Яндекс.Диск"
            except KeyError:

                print(f'Файл "{file}" был ранее загружен на Яндекс.Диск')
                message = (f'\n======\n\n'
                           f'Все файлы из папки {self.folder_name} загружены на Яндекс.Диск')

        return message

    def create_folder(self):
        """метод создает папку на яндекс.диске с таким же именем как и в self.file_path"""
        put = r.put(self.URL, headers=self.headers)
        try:
            return put.status_code, put.json()["message"]
        except KeyError:
            return put.status_code, put.json()["href"]


if __name__ == '__main__':
    # folder_path = "c:\my_folder"
    # token = "AgAAAABCqug7AADLWzOfyZvGvUIFtKRDuWJAUxI"
    folder_path = input("Укажите путь к папке с файлами: ")
    token = input("Введите токен для авторизации: ")

    uploader = YaUploader(folder_path)
    result = uploader.upload()

    print(result)
