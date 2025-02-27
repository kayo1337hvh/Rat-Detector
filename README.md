   _   _ _______ _____ _____         _______   _             _    _  _                    _                   _   _                ___  
   /\   | \ | |   |_   _|   \     /\|   | | |           | |  | || |                  (_)                 | | | |              / _ \ 
   /  \  |  \| |  | |    | | | |) |   /  \  | |    | |  _   _  | || || |_ _     _ _  _     _ _    | | | | ____ _ _   _| | | |
   / /\ \ | .  |  | |    | | |  _  /   / /\ \ | |    | '_ \| | | | | '_ \__   _| '_ \ / _ | '| |  / _` | '_ \ / _` | | |/ / _` | | | | | | |
  / ____ \| |\  |  | |   _| |_| | \ \  / ____ \| |    | |_) | |_| | | | | | | | | | | (_| | |  | | | (_| | | | | (_| | |   < (_| | |_| | |_| |
 /_/    \_\_| \_|  |_|  |_____|_|  \_\/_/    \_\_|    |_./ \__, | |_| |_| |_| |_| |_|\__,_|_|  |_|  \__,_|_| |_|\__,_| |_|\_\__,_|\__, |\___/ 
                                                              / |                                                                  / |      
                                                             |___/                                                                  |___/
                                                             
Этот скрипт предназначен для проведения базовой диагностики и очистки системы Windows от подозрительных файлов, RAT вируса, ошибок в реестре. Он выполняет следующие основные функции:

    Получение сетевых подключений - анализирует текущие сетевые подключения и выводит активные IP-адреса.
    Поиск подозрительных файлов - сканирует системные каталоги на наличие исполнимых файлов (.exe, .bat), которые могут быть потенциально вредоносными.
    Проверка и исправление записей реестра - проверяет и восстанавливает критические значения в реестре, связанные с запуском системы и автозагрузкой.
    Проверка и восстановление файла hosts - восстанавливает стандартное содержимое файла hosts для устранения возможных манипуляций с сетевыми настройками.

Файл нужно запускать от имени Администратора

Требования

    Python 3.x
    Установленные библиотеки:
        psutil - для работы с сетевыми соединениями.
        colorama - для добавления цветного вывода в консоль.
        winreg - для работы с реестром Windows.

Чтобы установить необходимые библиотеки, выполните следующую команду:

pip install psutil colorama

Как использовать

    Скачайте скрипт на вашу машину.
    Запустите его через Python:

python script_name.py

    В интерфейсе будет предложено выбрать один из следующих вариантов:
        1 - Просканировать IP-адреса, подключенные к ПК.
        2 - Информация о создателях скрипта.
        3 - Найти и удалить подозрительные файлы.
        4 - Проверить и исправить реестр и файл hosts.

    После выполнения операции будет предложено продолжить работу с другими функциями или выйти из программы.


Ищет в системных папках .exe и .bat файлы, которые могут быть вредоносными. Проводится поиск в папках:

    C:\
    D:\
    E:\
    C:\Program Files
    C:\Program Files (x86)

Отображает найденные подозрительные файлы и позволяет пользователю выбрать их для удаления.

Проверяет и исправляет ключевые записи в реестре Windows:

    Ветку Winlogon, чтобы убедиться, что запускается Explorer.exe.
    Запись Userinit, чтобы удостовериться, что используется правильный путь к файлу userinit.exe.
    Очистка автозагрузки от нежелательных записей.


Восстанавливает стандартное содержимое файла hosts для предотвращения возможных атак или манипуляций с DNS.
Важное замечание

    Будьте осторожны при удалении файлов, так как не все найденные файлы являются вредоносными. Убедитесь, что вы понимаете, что удаляете.
    Некоторые функции требуют прав администратора для корректного выполнения (например, изменения в реестре и доступ к системным файлам).

