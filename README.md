# Задание на дипломный проект первого блока «Основы языка программирования Python»:
# «Резервное копирование фотографий пользователей ВКонтакте + Облачный архиватор Яндекс.Диск»

---
#### _!Nota Bene:_

_При релизации задания использованы внешние библиотеки Selenium, tqdm и проч. Запускной файл chromedriver.exe для работы Selenium размещён вместе с программой в репозитории.
Все необходимые библиотеки указаны в requirement.txt. При развёртывании программы на новой машине рекомендуется запустить автоматическую установку библиотек из requirement.txt._

_Для авторизации в ВК требуется логин и пароль пользователя. Программа не сохраняет логин и пароль пользователя. Учётные данные передаются только в сервис авторизации ВКонтакте для получения ключа доступа.
Авторизация проводится при первом запуске программы, а также в случае истечения срока действия ключа._
_По умолчанию ключ доступа выдаётся на срок 24 часа. Ключ записыватся в отдельный файл и считывается оттуда в течение работы программы._
---
## Описание:
Облачные хранилища стали для человека уже нормой. 
Загрузить в облако альбом с фотографиями или поделиться какими-либо документами не составляет большой сложности. 
Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соцсети могут быть недоступны по каким-либо причинам. Давайте защитимся от такого.  

Нужно написать программу для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.  Для названий фотографий использовать количество лайков и дату загрузки. 

Но есть одна проблема — на Яндекс.Диске может закончиться место.  
Было бы неплохо уметь архивировать самый большой и тяжёлый файл или папку и загружать обратно в облако - так можно сохранить больше свободного места.


## Задание:
Нужно написать программу, которая будет:

1. [x] Получать фотографии с профиля. Для этого нужно использовать метод [photos.get](https://vk.com/dev/photos.get).
2. [x] Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
3. [x] Для имени фотографий использовать количество лайков и дату загрузки.
4. [x] Сохранять информацию по фотографиям в json-файл с результатами.
5. [x] Получать информацию по всем папкам в Я.Диске.
6. [x] Искать среди них самый тяжёлый.
7. [x] Скачивать файл на компьютер, где запущена программа.
8. [x] Архивировать файл.
9. [x] Загружать его обратно в ту же папку, откуда он был скачан.
10. [x] Записывать информацию по измененному файлу в json-файл.

### Входные данные:
Пользователь вводит:
1. id пользователя vk;
2. токен с [Полигона Яндекс.Диска](https://yandex.ru/dev/disk/poligon/).
*Важно:* Токен публиковать в github не нужно!

### Выходные данные:
1. json-файл с информацией по файлу с фото:
    ```
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
    ```
2. json-файл с информацией по файлу архива:
    ```
        {
        “file_name”: “diplom.docx”,
        “size”: “исходный размер файла”,
        “path”: “disk:/Netology/diplom.docx”
        }
    ```
3. Измененный Я.Диск, куда добавился новый архив и фотографии.​​

### Обязательные требования к программе:
1. [x] Использовать REST API Я.Диска и ключ, полученный с полигона.
2. [x] Для загруженных фотографий нужно создать свою папку.
3. [x] Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
4. [x] Для архивации файлов или папки использовать библиотеку zipfile.
5. [x] Опционально предлагать пользователю удалить с Диска файл/папку вместо загружаемого файла.
6. [x] Сделать прогресс-бар для отслеживания процесса программы.
7. [x] Код программы должен удовлетворять PEP8.​

### Дополнительные требования к программе:
1. [x] Сохранять фотографии и из других альбомов.
2. ~~[ ] Сохранять фотографии на Google.Drive.~~
3. [x] Выдача топ-10 файлов по размеру.
4. ~~[ ] Запись в гугл-таблицу список файлов в табличном виде - название, каталог хранения, размер.~~