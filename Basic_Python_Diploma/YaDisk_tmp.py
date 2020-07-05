from pprint import pprint

import requests as r
import json
import os
import zipfile


class YaDisk:
    all_files = []
    all_folders = []

    def __init__(self):
        self.token = access_token
        self.URL = f"https://cloud-api.yandex.net/v1/disk/resources"
        self.params = {"path": '/'}
        self.headers = {"port": "443", "Authorization": f"OAuth {self.token}"}
        self.response = r.get(self.URL, params=self.params, headers=self.headers).json()
        self._parse_catalogues(self.response)

    def zip_file(self, file):
        full_name = os.path.basename(file)
        name = os.path.splitext(full_name)[0]
        with zipfile.ZipFile(name + '.zip', "w") as f:
            f.write(file)
        return f

    def _parse_catalogues(self, resp):
        def _cat_size(resp):
            size = 0
            for item in resp['_embedded']['items']:
                if item['type'] != "dir":
                    size += item["size"]
                else:
                    param = {"path": item["path"]}
                    new_resp = r.get(self.URL, params=param, headers=self.headers).json()
                    size += _cat_size(new_resp)
            return size

        for item in resp['_embedded']['items']:
            if item['type'] == "dir":
                param = {"path": item["path"]}
                resp = r.get(self.URL, params=param, headers=self.headers).json()
                self._parse_catalogues(resp)
                folder_size = {"size": _cat_size(resp)}
                item.update(folder_size)
                self.all_folders.append(item)
            else:
                file_dic = {
                    "name": item["name"],
                    "size": item["size"],
                    "link": item["file"],
                    "path": item["path"]
                }
                self.all_files.append(file_dic)

    def top10(self, _type=None):
        """For top10 you shall indicate '_type'-argument either as 'file' or 'folder' """
        collection = None
        if (_type is None) or (_type != 'file' and _type != 'folder'):
            return print(self.top10.__doc__)
        else:
            if _type == 'file':
                collection = self.all_files
            elif _type == 'folder':
                collection = self.all_folders
            size_list = {}
            for file in collection:
                size_list[file['name']] = file['size']
            values_list = list(set(size_list.values()))
            values_list.sort(reverse=True)
            top_10_nums = tuple(values_list[:10])
            top_10 = []
            for num, i in enumerate(top_10_nums, start=1):
                for keys, values in size_list.items():
                    if i == values:
                        size = int(round(values / 1024, 0))
                        if size > 100000:
                            size = str(round(size / 1024 ** 2, 2)) + " GB"
                        elif 100000 > size > 1000:
                            size = str(round(size / 1024, 2)) + " MB"
                        else:
                            size = str(size) + " KB"
                        top_10.append(f'{num}. {keys}, {size}')
            print(*top_10, sep="\n", end='\n\n')
            return top_10


class YaDownloader(YaDisk):
    def find_biggest(self, _type=None):
        """For find_biggest you shall indicate '_type'-argument either as 'file' or 'folder' """
        lst = None
        filename = None
        if (_type is None) or (_type != 'file' and _type != 'folder'):
            return print(self.find_biggest.__doc__)
        else:
            if _type == 'file':
                lst = self.all_files
                filename = "biggest_file_info.json"
            elif _type == 'folder':
                lst = self.all_folders
                filename = "biggest_folder_info.json"
        max_size = 0
        for dic in lst:
            if dic['size'] > max_size:
                max_size = dic['size']
        for dic in lst:
            for value in dic.values():
                if max_size == value:
                    with open(filename, "w", encoding="UTF8") as f:
                        json.dump(dic, f)
                    return dic

    def download(self, item):
        target_folder = 'downloads'
        try:
            if item['type'] == 'dir':
                target_folder = target_folder + "/" + item['path'].split('disk:/')[-1]
                if os.path.exists(target_folder) is False:
                    os.mkdir(target_folder)
                    target_folder = os.path.abspath(target_folder)
                else:
                    target_folder = os.path.abspath(target_folder)
        except KeyError:
            if os.path.exists(target_folder) is False:
                os.mkdir(target_folder)
                target_folder = os.path.abspath(target_folder)
            else:
                target_folder = os.path.abspath(target_folder)
        param = {'path': item['path']}
        response = r.get(self.URL, params=param, headers=self.headers).json()
        try:
            for item_ in response['_embedded']['items']:
                if item_['type'] == 'dir':
                    self.download(item_)
                else:
                    file_to_download = r.get(item_["file"])
                    with open(os.path.join(target_folder, item_["name"]), 'wb') as f:
                        f.write(file_to_download.content)
        except KeyError:
            file_to_download = r.get(response["file"])
            with open(os.path.join(target_folder, response["name"]), 'wb') as f:
                f.write(file_to_download.content)


class YaUploader(YaDisk):
    def __init__(self, path: str = None):
        super().__init__()
        if path:
            self.full_path = os.path.abspath(path)
            print(self.full_path)
            if "." in self.full_path:
                self.full_name = os.path.basename(self.full_path)
                print(self.full_name)
                self.name = os.path.splitext(self.full_path)[0].split(os.path.sep)[-1]
                print(self.name)
                for dic in self.all_files:
                    for value in dic.values():
                        try:
                            if self.name in value:
                                self.folder_name = dic['path']
                                print(self.folder_name)
                                break
                        except TypeError:
                            continue
            else:
                self.name = os.path.basename(self.full_path)
                print(self.name)
                counter = 0
                for dic in self.all_folders:
                    print(self.name in dic.values())
                    if self.name in dic.values():
                        counter += 1
                        for value in dic.values():
                            if self.name == value:
                                self.folder_name = dic['path']
                                print(self.folder_name)
                                break
                            else:
                                continue
                    if not counter:
                        self.create_folder(self.name)
        else:
            pass

    @staticmethod
    def upload_file(file, up_path=None):
        message = str
        if not up_path:
            folder_path = file.filename

    def upload_folder(self, folder_name):
        """Метод загруджает файлы по списку file_list на яндекс диск"""
        path = os.path.abspath(folder_name)
        file_list = os.listdir(path)
        message = str
        for file in file_list:
            try:
                param = {'path': f'{folder_name}/{file}'}
                full_path = os.path.join(path, file)
                upload_url = r.get(self.URL + '/up_load', params=param, headers=self.headers).json()["href"]
                with open(full_path, "rb") as f:
                    r.put(upload_url, data=f)
                    print(f'Файл "{file}" успешно загружен на Яндекс.Диск')
                message = f"\n======\n\n" \
                          f"Все файлы из папки {folder_name} успешно загружены на Яндекс.Диск"
            except KeyError:

                print(f'Файл "{file}" был ранее загружен на Яндекс.Диск')
                message = (f'\n======\n\n'
                           f'Все файлы из папки {folder_name} загружены на Яндекс.Диск')

        return message

    def create_folder(self, folder_name):
        """метод создает папку на яндекс.диске с таким же именем как и в self.file_path"""
        param = {"path": folder_name}
        test = r.get(self.URL, headers=self.headers, params=param)
        if test.status_code == 404:
            creator = YaUploader.create_folder(self)
            if creator[0] == 201:
                print(f'Папка "{folder_name}" успешно создана на Яндекс.Диске')
                print()
            else:
                print(creator)
                print()
        elif test.status_code == 200:
            print(f'Папка "{folder_name}" уже существует на Яндекс.Диске')
            print()
        else:
            print(test)
        put = r.put(self.URL, headers=self.headers)
        try:
            return put.status_code, put.json()["message"]
        except KeyError:
            return put.status_code, put.json()["href"]

    def delete(self, yadisk_path):
        """метод удаляет папку или файл в корзину яндекс.диска"""
        param = {'path': yadisk_path}
        put = r.delete(self.URL, headers=self.headers)
        try:
            return put.status_code, put.json()["message"]
        except KeyError:
            return put.status_code, put.json()["href"]


if __name__ == '__main__':
    # access_token = input("Введите токен: ")
    access_token = "AgAAAABCqug7AADLWzOfyZvGvUIFtKRDuWJAUxI"
    down = YaDownloader()
    down.top10('file')
    down.top10('folder')
    biggest_file = down.find_biggest('file')
    biggest_folder = down.find_biggest('folder')
    print(biggest_file['name'], biggest_file['size'])
    print(biggest_folder['name'], biggest_folder['size'])
    down.download(biggest_file)
    down.download(biggest_folder)

    # arch = down.zip_file(filename)
    # archive = os.path.abspath(arch.filename)
    # archive = 'P8200002.zip'
    # up_load = YaUploader("c:\my_folder")
    # up_load.upload_folder()
