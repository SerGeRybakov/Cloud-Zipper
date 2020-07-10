import json
import os
import zipfile

import requests as r


class YaDisk:
    all_files = []
    all_folders = []

    def __init__(self):
        self.token = access_token
        self.URL = f"https://cloud-api.yandex.net/v1/disk/resources"
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
                    new_resp = r.get(self.URL, params=param, headers=self.headers).json()
                    size += _cat_size(new_resp)
            return size

        if resp is None:
            response = r.get(self.URL, params=self.params, headers=self.headers).json()
        else:
            response = resp
        for item in response['_embedded']['items']:
            if item in self.all_folders or item in self.all_files:
                continue
            else:
                if item['type'] == "dir":
                    param = {"path": item["path"]}
                    response = r.get(self.URL, params=param, headers=self.headers).json()
                    self._parse_catalogues(response)
                    folder_size = {"size": _cat_size(response)}
                    item.update(folder_size)
                    self.all_folders.append(YaFolder(item))
                else:
                    self.all_files.append(YaFile(item))

    def create_folder(self, folder_name, path=None):
        """метод создает папку на яндекс.диске с заданным именем"""

        def _create(_param):
            put = r.put(self.URL, headers=self.headers, params=_param)
            try:
                return put.status_code, put.json()["href"]
            except KeyError:
                return put.status_code, put.json()["message"]

        if path is None:
            print("Текущий список папок:")
            for num, dir in enumerate(ya.all_folders):
                print("dir <index>" + str(num) + ".", dir)
            print("\nЕсли вы хотите создать папку в корне диска - нажмите Enter.\n"
                  "Если вы хотите создать папку внутри другой папки - введите индекс соответствующей папки.\n")
            tree = input('Введите ответ?')
            if not tree:
                param = {"path": folder_name}
            else:
                param = {"path": os.path.join(self.all_folders[int(tree)].object_realpath + "/", folder_name)}
        else:
            param = {"path": path}
        print(param)
        test = r.get(self.URL, headers=self.headers, params=param)
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
        max_size = 0
        for obj in lst:
            if obj.size > max_size:
                max_size = obj.size
        for obj in lst:
            if max_size == obj.size:
                with open(filename, "w", encoding="UTF-8") as f:
                    json.dump({obj.name: obj.size}, f)
                return obj

    def delete(self, *objects):
        """метод удаляет папку или файл с яндекс.диска в корзину или навсегда"""

        print("\nДля удаления объекта(-ов) в Корзину просто нажмите Enter.\n"
              "Для полного удаления объекта(-ов) без возможности восстановления введите 1.")
        permanent = input("Введите ответ: ")
        perm_del = ''
        if permanent == "1":
            perm_del = {"permanently": "true"}

        for obj in objects:
            param = {'path': obj.object_realpath}
            if perm_del:
                param.update(perm_del)
            put = r.delete(self.URL, headers=self.headers, params=param)
            if not str(put.status_code).startswith('2'):
                return put.status_code, put.json()
            else:
                self.reload()

        for num, dir in enumerate(ya.all_folders):
            print("dir" + str(num) + ".", dir)
        string = ''
        if len(objects) == 1:
            string = objects[0]
        elif len(objects) > 1:
            string = f'{", ".join(objects)}'

        if perm_del:
            return f'Объекты {string} успешно удалены с Яндекс.Диска.'
        else:
            return f'Объекты {string} успешно удалены в Корзину.'

    def download(self, item):
        target_folder = 'downloads'
        if os.path.exists(target_folder) is False:
            os.mkdir(target_folder)
        try:
            if item.type == 'dir':
                target_folder = os.path.join(target_folder, item.object_realpath.split('disk:/')[-1])
                if os.path.exists(target_folder) is False:
                    os.mkdir(target_folder)
                    target_folder = os.path.abspath(target_folder)
                else:
                    target_folder = os.path.abspath(target_folder)
            else:
                target_folder = os.path.abspath(target_folder)
                file_to_download = r.get(item.link)
                with open(os.path.join(target_folder, item.name), 'wb') as f:
                    f.write(file_to_download.content)
        except (KeyError, AttributeError):
            if item['type'] == 'dir':
                target_folder = os.path.join(target_folder, item['path'].split('disk:/')[-1])
                if os.path.exists(target_folder) is False:
                    os.mkdir(target_folder)
                    target_folder = os.path.abspath(target_folder)
                else:
                    target_folder = os.path.abspath(target_folder)
        try:
            param = {'path': item.object_realpath}
        except (KeyError, AttributeError):
            param = {'path': item['path']}

        response = r.get(self.URL, params=param, headers=self.headers).json()
        try:
            for new_item in response['_embedded']['items']:
                if new_item['type'] == 'dir':
                    self.download(new_item)
                else:
                    file_to_download = r.get(new_item["file"])
                    with open(os.path.join(target_folder, new_item["name"]), 'wb') as f:
                        f.write(file_to_download.content)
        except KeyError:
            file_to_download = r.get(response["file"])
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
                print(obj_type + " " + str(num) + ".", file)
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
            size_list = {}
            for file in collection:
                size_list[file.name] = file.size
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

    def upload(self, object):
        """Метод загруджает файлы по списку file_list на яндекс диск"""

        object_full_path = ''
        folder_scan = os.walk(os.path.curdir)
        for root, dirs, files in folder_scan:
            for file in files:
                if object == file:
                    object_full_path = os.path.join(root, object)

        ya_disk_path = "disk:/"
        object_realpath = object_full_path.split('.\\')[1]
        folder_path = object_full_path.split(object)[0].replace("\\", "/")
        target_folder_path = ya_disk_path + object_realpath.replace("\\", "/").split("/" + object)[0]
        folder_name = os.path.basename(target_folder_path)
        target_path = ya_disk_path + object_realpath.replace("\\", "/")

        paths = {dir.path for dir in self.all_folders}
        if target_folder_path in paths:
            pass
        else:
            self.create_folder(folder_name, target_folder_path)

        message = str
        if os.path.isdir(object) is True:
            file_list = os.listdir(os.path.abspath(folder_path))
            for file in file_list:
                try:
                    param = {'path': target_path}
                    upload_url = r.get(self.URL + '/upload', params=param, headers=self.headers).json()
                    with open(object_full_path, "rb") as f:
                        r.put(upload_url['href'], data=f)
                        print(f'Файл "{file}" успешно загружен на Яндекс.Диск')
                    message = f"\n======\n\n" \
                              f"Все файлы из папки {folder_path} успешно загружены на Яндекс.Диск"
                except KeyError:
                    print(f'Файл "{file}" был ранее загружен на Яндекс.Диск')
                    message = (f'\n======\n\n'
                               f'Все файлы из папки {folder_path} загружены на Яндекс.Диск')

        else:
            try:
                param = {'path': target_path}
                upload_url = r.get(self.URL + '/upload', params=param, headers=self.headers).json()
                with open(object_full_path, "rb") as f:
                    r.put(upload_url['href'], data=f)
                    print(f'Файл "{object}" успешно загружен на Яндекс.Диск')
                message = f"\n======\n\n" \
                          f"Все файлы из папки {folder_path} успешно загружены на Яндекс.Диск"
            except KeyError:
                print(f'Файл "{object}" был ранее загружен на Яндекс.Диск')
                message = (f'\n======\n\n'
                           f'Все файлы из папки {folder_path} загружены на Яндекс.Диск')
        self.reload()
        self.print_all("file")
        self.print_all("folder")
        return message

    @staticmethod
    def zip_file(item):
        base_path = "downloads"
        full_name = item.name
        name = os.path.splitext(full_name)[0]
        path = item.object_realpath.split('disk:/')[1]
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


if __name__ == '__main__':
    access_token = input("Введите токен Яндекс.Диска: ")
    ya = YaDisk()
    # ya.print_all("file")
    # ya.print_all("folder")

    # print(ya.delete(ya.all_files[13:]))
    # print(ya.delete(ya.all_folders[int(input("Введите индекс папки для удаления: "))]))

    # ya.top10('file')
    # ya.top10('folder')

    # biggest_file = ya.find_biggest('file')
    # biggest_folder = ya.find_biggest('folder')
    # print(biggest_file)
    # print(biggest_folder)

    # ya.download(biggest_file)
    # ya.download(biggest_folder)

    # arch_file = ya.zip_file(biggest_file)
    # print(arch_file)
    # arch_folder = ya.zip_file(biggest_folder)
    # print(arch_folder)

    # ya.create_folder("test")
    print(ya.upload("test.txt"))
