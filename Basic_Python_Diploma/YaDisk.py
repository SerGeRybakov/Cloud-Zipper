import json
import os
import zipfile
from datetime import datetime
import requests
from tqdm import tqdm

"""
    Класс YaDisk - основной класс программы, содержащий в себе все методы для работы с такими сущностями Яндекс.Диска
    как папки и файлы. 
    Классы YaFile и YaFolder - наследники класса YaFile и YaDisk. Они не имеют собственных методов, но имеют все 
    атрибуты, присущие файлам и папкам, хранящимся на Яндекс.Диске. 
    
    Основные методы для работы с этими сущностями являются: 
     - create_folder,
     - find_biggest,
     - delete,
     - download,
     - upload,
     - zip_file.
     Основные методы влияют на файлы и папки непосредственным образом. Поэтому они должны быть унаследованы 
     экземплярами классов YaFile и YaFolder.
     
     Вспомогательными методами являются:
     - _parse_catalogues,
     - print_all,
     - reload,
     - top10.
     Данные методы не влияют непосредственно на сами файлы и папки, а лишь собирают и/или выводят обобщенную
     статистическую информацию о файлах или папках. Вероятно, что такие методы не должны наследоваться экземплярами 
     классов YaFile и YaFolder. При этом метод _parse_catalogues автоматически инициирует экземпляры классов YaFile и 
     YaFolder с тем, чтобы программа имела полную информацию о текущем содержимом облака, а метод reload пересобирает 
     эту информацию каждый раз, когда содержимое облака должно измениться после использования основных методов, влияющих 
     на такое содержимое.          
     
     В то же время, программа не предполагает непосредственных операций с экземплярами классов YaFile и YaFolder.
     На старте программы инициируется единственный экзепляр класса YaDisk, который обращается присущими ему методами с     
     экземплярами классов YaFile и YaFolder - получает, обрабатывает, выводит информацию о всех них или о каждом 
     отдельном экземпляре, а также непосредственно влияет на них тем или иным образом.
     
     Кроме этого, в целях избежания дублирования кода, функция __repr__ перегружена из класса YaDisk с тем, чтобы 
     экземпляры наследников этого класса выводились на печать правильно (с моей точки зрения).
     См. комментарий к __repr__.
     """

class YaDisk:
    def __init__(self, token):
        self.all_files = []
        self.all_folders = []
        self.token = token
        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.params = {"path": '/'}
        self.headers = {"port": "443", "Authorization": f"OAuth {self.token}"}
        self._parse_catalogues()

    def __repr__(self):
        return self.name

    def _parse_catalogues(self, resp=None):
        def _cat_size(resp):
            size = 0
            for item in resp['_embedded']['items']:
                if item['type'] != "dir":
                    size += item["size"]
                else:
                    param = {"path": item["path"]}
                    new_resp = requests.get(self.URL, params=param, headers=self.headers).json()
                    size += _cat_size(new_resp)
            return size

        if resp is None:
            response = requests.get(self.URL, params=self.params, headers=self.headers).json()
        else:
            response = resp
        for item in response['_embedded']['items']:
            if item in self.all_folders or item in self.all_files:
                continue
            else:
                if item['type'] == "dir":
                    param = {"path": item["path"]}
                    response = requests.get(self.URL, params=param, headers=self.headers).json()
                    self._parse_catalogues(response)
                    folder_size = {"size": _cat_size(response)}
                    item.update(folder_size)
                    self.all_folders.append(YaFolder(item))
                else:
                    self.all_files.append(YaFile(item))

    def create_folder(self, folder_name, path=None):
        """метод создает папку на яндекс.диске с заданным именем"""

        def _create(_param):
            put = requests.put(self.URL, headers=self.headers, params=_param)
            try:
                return put.status_code, put.json()["href"]
            except KeyError:
                return put.status_code, put.json()["message"]

        if path is None:
            print("Текущий список папок:")
            for num, dir in enumerate(self.all_folders):
                print("dir <index>" + str(num) + ".", dir)
            print("\nЕсли вы хотите создать папку в корне диска - нажмите Enter.\n"
                  "Если вы хотите создать папку внутри другой папки - введите индекс соответствующей папки.\n")
            tree = input('Введите ответ?')
            if not tree:
                param = {"path": folder_name}
            else:
                param = {"path": self.all_folders[int(tree)].path + "/" + folder_name}
        else:
            param = {"path": path}
        print(param)
        test = requests.get(self.URL, headers=self.headers, params=param)
        if test.status_code == 404:
            creator = _create(param)
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

        self.reload()
        print("Текущий список папок:")
        self.print_all('folder')

    def find_biggest(self, obj_type=None):
        """For find_biggest you shall indicate 'obj_type'-argument: either 'file' or 'folder' """
        lst = None
        filename = None
        if (obj_type is None) or (obj_type != 'file' and obj_type != 'folder'):
            return print(self.find_biggest.__doc__)
        else:
            if obj_type == 'file':
                lst = self.all_files
                filename = "biggest_file_info.json"
            elif obj_type == 'folder':
                lst = self.all_folders
                filename = "biggest_folder_info.json"
        max_size_object = max(lst, key=lambda obj: obj.size)
        with open(filename, "w", encoding="UTF-8") as f:
            json.dump({max_size_object.name: max_size_object.size}, f)

        return max_size_object

    def delete(self, *objects):
        """метод удаляет папку или файл с яндекс.диска в корзину или навсегда"""

        print("\nДля удаления объекта(-ов) в Корзину просто нажмите Enter.\n"
              "Для полного удаления объекта(-ов) без возможности восстановления введите 1.")
        permanent = input("Введите ответ: ")
        perm_del = ''
        if permanent == "1":
            perm_del = {"permanently": "true"}

        for obj in objects:
            param = {'path': obj.path}
            if perm_del:
                param.update(perm_del)
            put = requests.delete(self.URL, headers=self.headers, params=param)
            if put.status_code >= 300:
                return put.status_code, put.json()
        self.reload()

        for num, dir in enumerate(self.all_folders):
            print("dir" + str(num) + ".", dir)
        string = ''
        if len(objects) == 1:
            string = objects[0]
        elif len(objects) > 1:
            string = ", ".join(objects)

        if perm_del:
            return f'Объекты {string} успешно удалены с Яндекс.Диска.'
        else:
            return f'Объекты {string} успешно удалены в Корзину.'

    def download(self, item):
        target_folder = 'downloads'
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        try:
            if item.type == 'dir':
                target_folder = os.path.join(target_folder, item.path.split('disk:/')[-1])
                if not os.path.exists(target_folder):
                    os.mkdir(target_folder)
                target_folder = os.path.abspath(target_folder)
            else:
                target_folder = os.path.abspath(target_folder)
                file_to_download = requests.get(item.link)
                with open(os.path.join(target_folder, item.name), 'wb') as f:
                    f.write(file_to_download.content)
        except (KeyError, AttributeError):
            if item['type'] == 'dir':
                target_folder = os.path.join(target_folder, item['path'].split('disk:/')[-1])
                if not os.path.exists(target_folder):
                    os.mkdir(target_folder)
                target_folder = os.path.abspath(target_folder)
        try:
            param = {'path': item.path}
        except (KeyError, AttributeError):
            param = {'path': item['path']}

        response = requests.get(self.URL, params=param, headers=self.headers).json()
        try:
            for new_item in response['_embedded']['items']:
                if new_item['type'] == 'dir':
                    self.download(new_item)
                else:
                    file_to_download = requests.get(new_item["file"])
                    with open(os.path.join(target_folder, new_item["name"]), 'wb') as f:
                        f.write(file_to_download.content)
        except KeyError:
            file_to_download = requests.get(response["file"])
            with open(os.path.join(target_folder, response["name"]), 'wb') as f:
                f.write(file_to_download.content)

    def print_all(self, obj_type=None):
        """For print_all you shall indicate 'obj_type'-argument: either 'file' or 'folder' """
        collection = None
        if (obj_type is None) or (obj_type != 'file' and obj_type != 'folder'):
            return print(self.top10.__doc__)
        else:
            if obj_type == 'file':
                collection = self.all_files
            elif obj_type == 'folder':
                collection = self.all_folders
            for num, file in enumerate(collection):
                print(obj_type + " " + str(num) + ".", file, file.size)
        return collection

    def reload(self):
        self.all_folders = []
        self.all_files = []
        self._parse_catalogues()

    def top10(self, obj_type=None):
        """For top10 you shall indicate 'obj_type'-argument: either 'file' or 'folder' """
        collection = None
        if (obj_type is None) or (obj_type != 'file' and obj_type != 'folder'):
            return print(self.top10.__doc__)
        else:
            if obj_type == 'file':
                collection = self.all_files
            elif obj_type == 'folder':
                collection = self.all_folders
            top10 = sorted(collection, key=lambda obj: obj.size, reverse=True)[:10]
            top_10 = []
            for num, i in enumerate(top10, start=1):
                size = int(round(i.size / 1024, 0))
                if size > 100000:
                    size = str(round(size / 1024 ** 2, 2)) + " GB"
                elif 100000 > size > 1000:
                    size = str(round(size / 1024, 2)) + " MB"
                else:
                    size = str(size) + " KB"
                top_10.append(f'{num}. {i}, {size}')
            print(*top_10, sep="\n", end='\n\n')
            return top_10

    def upload(self, object, url=None):
        """Метод загруджает на яндекс диск файлы и папки с компьютера, а также фотографии из сети, имеющие URL."""
        def _upload_folder(folder_path):
            file_list = os.listdir(folder_path)
            message = str
            for file in file_list:
                try:
                    param = {"path": f"{folder_path}/{file}"}
                    full_path = os.path.join(folder_path, file)
                    upload_url = requests.get(self.URL, headers=self.headers, params=param).json()["href"]
                    with open(full_path, "rb") as f:
                        requests.put(upload_url, data=f)
                        print(f'Файл "{file}" успешно загружен на Яндекс.Диск')
                    message = f"\n======\n\n" \
                              f"Все файлы из папки {folder_name} успешно загружены на Яндекс.Диск"
                except KeyError:

                    print(f'Файл "{file}" был ранее загружен на Яндекс.Диск')
                    message = (f'\n======\n\n'
                               f'Все файлы из папки {folder_name} загружены на Яндекс.Диск')

        def _upload_file():
            try:
                param = {"path": f"{folder_path}/{file}"}
                full_path = os.path.join(folder_path, file)
                upload_url = requests.get(self.URL, headers=self.headers, params=param).json()["href"]
                with open(full_path, "rb") as f:
                    requests.put(upload_url, data=f)
                    print(f'Файл "{file}" успешно загружен на Яндекс.Диск')
                message = f"\n======\n\n" \
                          f"Все файлы из папки {folder_name} успешно загружены на Яндекс.Диск"
            except KeyError:

                print(f'Файл "{file}" был ранее загружен на Яндекс.Диск')

        def _upload_url(url, likes, date):
            date = str(datetime.fromtimestamp(date).date())
            param = {"path": target_folderpath + "/" + str(likes) + "_" + date + ".jpg", "url": url}
            return requests.post(self.URL+"/upload", headers=self.headers, params=param)

        def _check_folder_existanse(folder_name, target_folderpath):
            param = {"path": target_folderpath}
            test = requests.get(self.URL, headers=self.headers, params=param)
            if test.status_code == 404:
                folder = target_folderpath.split("/")[0]
                param = {"path": folder}
                test = requests.get(self.URL, headers=self.headers, params=param)
                if test.status_code == 404:
                    folder_name = folder.split("/")[-1]
                    self.create_folder(folder_name, folder)
                    folder_name = target_folderpath.split("/")[1]
                    self.create_folder(folder_name, target_folderpath)
                else:
                    self.create_folder(folder_name, target_folderpath)

        if len(object) == 2:
            folder = "vk_photo"
            folder_name = object[1]
            target_folderpath = folder + "/" + folder_name
            _check_folder_existanse(folder_name, target_folderpath)
            for url, likes, date in object[0]:
                up = _upload_url(url, likes, date)
        else:
            object_full_path = str
            if os.path.exists(os.path.abspath(object)):
                object_full_path = os.path.join('.', object)
            else:
                folder_scan = os.walk(os.path.curdir)
                for root, dirs, files in folder_scan:
                    for dir in dirs:
                        if object == dir:
                            object_full_path = os.path.join(root, dir)
                    else:
                        for file in files:
                            if object == file:
                                object_full_path = os.path.join(root, file)
            print(100, object_full_path)
            object_realpath = object_full_path.split('.\\')[1]
            print(1000, object_realpath)
            folder_name = object
            target_folderpath = object_realpath.replace("\\", "/")
            _check_folder_existanse(folder_name, target_folderpath)
            if os.path.isdir(object_full_path):
                up = _upload_folder(target_folderpath)
            else:
                folder_path = object_full_path.split(object)[0].replace("\\", "/")
                print(folder_path)
                up = _upload_file()


        # if not os.path.isdir(object_realpath):
        #     target_folderpath = ya_disk_path + object_realpath.replace("\\", "/").split("/" + object)[0]
        # else:
        #     target_folderpath = ya_disk_path + object
        # # print(10000, target_folderpath)
        # folder_name = os.path.basename(target_folderpath)
        # # target_path = ya_disk_path + target_folderpath
        # # print(target_path)
        # paths = {dir.path for dir in self.all_folders}
        # if os.path.isdir(object_realpath):
        #     if target_folderpath in paths:
        #         pass
        #     else:
        #         self.create_folder(folder_name, target_folderpath)
        #
        # message = str
        # if os.path.isdir(object_full_path):
        #     file_list = os.listdir(object_full_path)
        #     print(file_list)
        #     for file in file_list:
        #         try:
        #             param = {'path': target_folderpath + "/" + file}
        #             upload_url = requests.get(self.URL + '/upload', params=param, headers=self.headers).json()
        #             with open(os.path.join(object_full_path, file), "rb") as f:
        #                 requests.put(upload_url['href'], data=f)
        #                 print(f'Файл "{file}" успешно загружен на Яндекс.Диск')
        #             message = f"\n======\n\n" \
        #                       f"Все файлы из папки {folder_path} успешно загружены на Яндекс.Диск"
        #         except KeyError:
        #             print(f'Файл "{file}" был ранее загружен на Яндекс.Диск')
        #             message = (f'\n======\n\n'
        #                        f'Все файлы из папки {folder_path} загружены на Яндекс.Диск')
        #
        # else:
        #     try:
        #         param = {'path': target_folderpath}
        #         upload_url = requests.get(self.URL + '/upload', params=param, headers=self.headers).json()
        #         with open(object_full_path, "rb") as f:
        #             requests.put(upload_url['href'], data=f)
        #             print(f'Файл "{object}" успешно загружен на Яндекс.Диск')
        #         message = f"\n======\n\n" \
        #                   f"Все файлы из папки {folder_path} успешно загружены на Яндекс.Диск"
        #     except KeyError:
        #         print(f'Файл "{object}" был ранее загружен на Яндекс.Диск')
        #         message = (f'\n======\n\n'
        #                    f'Все файлы из папки {folder_path} загружены на Яндекс.Диск')
        #
        # return message

    @staticmethod
    def zip_file(item):
        base_path = "downloads"
        full_name = item.name
        name = os.path.splitext(full_name)[0]
        path = item.path.split('disk:/')[1]
        with zipfile.ZipFile(os.path.join(base_path, name) + '.zip', "w") as fzip:
            if "." in item.name:
                fzip.write(filename=os.path.join(base_path, full_name), arcname=full_name)
            else:
                folder = os.walk(os.path.join(base_path, path))
                for root, dirs, files in folder:
                    dir_name = root.split(base_path)[1]
                    fzip.write(filename=root, arcname=dir_name)
                    for filename in files:
                        fzip.write(filename=os.path.join(root, filename), arcname=os.path.join(dir_name, filename))
        return os.path.abspath(fzip.filename)


class YaFile(YaDisk):
    # noinspection PyMissingConstructor
    def __init__(self, item):
        self.antivirus_status = item['antivirus_status']
        self.size = item['size']
        self.comment_ids = item['comment_ids']
        self.name = item['name']
        self.exif = item['exif']
        self.created = item['created']
        self.resource_id = item['resource_id']
        self.modified = item['modified']
        self.mime_type = item['mime_type']
        self.link = item['file']
        self.path = item['path']
        self.media_type = item['media_type']
        self.sha256 = item['sha256']
        self.md5 = item['md5']
        self.type = item['type']
        self.revision = item['revision']


class YaFolder(YaDisk):
    # noinspection PyMissingConstructor
    def __init__(self, item):
        self.name = item['name']
        self.exif = item['exif']
        self.created = item['created']
        self.resource_id = item['resource_id']
        self.modified = item['modified']
        self.comment_ids = item['comment_ids']
        self.path = item['path']
        self.type = item['type']
        self.revision = item['revision']
        self.size = item['size']
