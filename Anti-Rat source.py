import psutil
import socket
import os
import glob
import winreg
import shutil
from colorama import init, Fore

# Инициализация colorama
init(autoreset=True)

# Функция для получения сетевых подключений
def get_connections():
    try:
        connections = psutil.net_connections(kind='inet')
        ip_addresses = set()

        for conn in connections:
            # Получаем локальный и удаленный адреса
            local_address = conn.laddr
            remote_address = conn.raddr

            # Добавляем локальный адрес
            ip_addresses.add(local_address.ip)

            # Если есть удаленный адрес, добавляем его
            if remote_address:
                ip_addresses.add(remote_address.ip)

        return ip_addresses
    except Exception as e:
        print(Fore.RED + f"Ошибка при получении сетевых подключений: {e}")
        return set()

# Функция для отображения IP адресов
def display_ip_addresses(ip_addresses):
    print(Fore.GREEN + "IP адреса, подключенные к ПК:")
    if not ip_addresses:
        print(Fore.RED + "Нет активных подключений.")
    for ip in ip_addresses:
        try:
            # Получаем доменное имя по IP
            domain_name = socket.gethostbyaddr(ip)[0]
            print(Fore.CYAN + f"{ip} - {domain_name}")
        except socket.herror:
            print(Fore.RED + f"{ip} - Увы, не смогли получить имя домена")

# Функция для поиска подозрительных файлов
def find_suspicious_files():
    suspicious_files = []
    # Поиск всех .exe и .bat файлов в системных директориях
    search_paths = ['C:\\', 'D:\\', 'E:\\', 'C:\\Program Files', 'C:\\Program Files (x86)']
    for path in search_paths:
        # Обработка исключений, если директория не существует
        if os.path.exists(path):
            suspicious_files.extend(glob.glob(os.path.join(path, '**', '*.exe'), recursive=True))
            suspicious_files.extend(glob.glob(os.path.join(path, '**', '*.bat'), recursive=True))

    return suspicious_files

# Функция для отображения подозрительных файлов и удаления
def handle_suspicious_files(files):
    if not files:
        print(Fore.GREEN + "Подозрительных файлов не найдено.")
        return

    print(Fore.YELLOW + "Найдены подозрительные файлы:")
    for i, file in enumerate(files, 1):
        print(Fore.CYAN + f"{i}. {file}")

    choice = input(Fore.WHITE + "Хотите удалить эти файлы? Введите номера через запятую (например, 1,3) или 'q' для выхода: ")
    if choice.lower() == 'q':
        print(Fore.GREEN + "Выход без удаления.")
        return

    indices_to_delete = [int(num.strip()) - 1 for num in choice.split(',') if num.strip().isdigit()]
    
    for index in indices_to_delete:
        if 0 <= index < len(files):
            file_to_delete = files[index]
            delete_choice = input(Fore.WHITE + f"Вы уверены, что хотите удалить файл {file_to_delete}? (y/n): ")
            if delete_choice.lower() == 'y':
                try:
                    os.remove(file_to_delete)
                    print(Fore.GREEN + f"Файл {file_to_delete} был успешно удален.")
                except Exception as e:
                    print(Fore.RED + f"Ошибка при удалении файла {file_to_delete}: {e}")
            else:
                print(Fore.YELLOW + f"Файл {file_to_delete} оставлен.")
        else:
            print(Fore.RED + "Некорректный выбор файла.")

# Функция для проверки и исправления реестра
def fix_registry():
    print(Fore.YELLOW + "\nПроверка и исправление записей реестра...")

    try:
        # Проверка и исправление ветки Winlogon
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon", 0, winreg.KEY_WRITE)
        shell_value, _ = winreg.QueryValueEx(reg_key, "Shell")
        if shell_value != "Explorer.exe":
            winreg.SetValueEx(reg_key, "Shell", 0, winreg.REG_SZ, "Explorer.exe")
            print(Fore.GREEN + "Исправлена запись Shell в реестре.")
        winreg.CloseKey(reg_key)

        # Проверка записи Userinit
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon", 0, winreg.KEY_WRITE)
        userinit_value, _ = winreg.QueryValueEx(reg_key, "Userinit")
        if userinit_value != "C:\\Windows\\system32\\userinit.exe":
            winreg.SetValueEx(reg_key, "Userinit", 0, winreg.REG_SZ, "C:\\Windows\\system32\\userinit.exe")
            print(Fore.GREEN + "Исправлена запись Userinit в реестре.")
        winreg.CloseKey(reg_key)

        # Очистка автозагрузки в реестре
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        num_values = winreg.QueryInfoKey(reg_key)[1]
        for i in range(num_values):
            value_name = winreg.EnumValue(reg_key, i)[0]
            if value_name.lower() not in ["antivirus", "someothercriticalapp"]:  # Исключаем нужные программы
                winreg.DeleteValue(reg_key, value_name)
                print(Fore.GREEN + f"Удалена запись: {value_name}")
        winreg.CloseKey(reg_key)

    except Exception as e:
        print(Fore.RED + f"Ошибка при работе с реестром: {e}")

# Функция для замены файла hosts
def fix_hosts():
    print(Fore.YELLOW + "\nПроверка и восстановление файла hosts...")

    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    standard_hosts_content = """127.0.0.1       localhost
::1             localhost
"""
    try:
        with open(hosts_path, 'w') as hosts_file:
            hosts_file.write(standard_hosts_content)
            print(Fore.GREEN + "Файл hosts был восстановлен.")
    except Exception as e:
        print(Fore.RED + f"Ошибка при восстановлении файла hosts: {e}")

def main():
    ip_addresses = get_connections()
    display_ip_addresses(ip_addresses)
    
    suspicious_files = find_suspicious_files()
    if suspicious_files:
        handle_suspicious_files(suspicious_files)
    else:
        print(Fore.GREEN + "Подозрительных файлов не найдено.")

    fix_registry()
    fix_hosts()

if __name__ == "__main__":
    # Окрасим ASCII в оранжевый
    print(Fore.RED + r"""
______  _____  _   _  _____  _      _____ ______  _____ ______   _              _____                             _            _                          __   _____  _____  ______
|  _  \|  ___|| | | ||  ___|| |    |  _  || ___ \|  ___||  _  \ | |            /  ___|                           (_)   ___    | |                        /  | |____ ||____ ||___  /
| | | || |__  | | | || |__  | |    | | | || |_/ /| |__  | | | | | |__   _   _  \ `--.   __ _  _   _   ___   _ __  _   ( _ )   | | __  __ _  _   _   ___  `| |     / /    / /   / / 
| | | ||  __| | | | ||  __| | |    | | | ||  __/ |  __| | | | | | '_ \ | | | |  `--. \ / _` || | | | / _ \ | '__|| |  / _ \/\ | |/ / / _` || | | | / _ \  | |     \ \    \ \  / /  
| |/ / | |___ \ \_/ /| |___ | |____\ \_/ /| |    | |___ | |/ /  | |_) || |_| | /\__/ /| (_| || |_| || (_) || |   | | | (_>  < |   < | (_| || |_| || (_) |_| |_.___/ /.___/ /./ /   
|___/  \____/  \___/ \____/ \_____/ \___/ \_|    \____/ |___/   |_.__/  \__, | \____/  \__,_| \__, | \___/ |_|   |_|  \___/\/ |_|\_\ \__,_| \__, | \___/ \___/\____/ \____/ \_/    
                                                                         __/ |                 __/ |                                         __/ |                                 
                                                                        |___/                 |___/                                         |___/                                  
    """)

    while True:
        print(Fore.YELLOW + "1 - Просканировать IP адреса подключенные к ПК")
        print(Fore.YELLOW + "2 - О создателях")
        print(Fore.YELLOW + "3 - Найти и удалить подозрительные файлы")
        print(Fore.YELLOW + "4 - Проверить и исправить реестр и hosts")

        choose = input(Fore.WHITE + "Введите цифру: ")

        if choose == "1":
            main()
        elif choose == "2":
            print(Fore.CYAN + "Sayori увлекается по большей части Java , фанат DDLC - 2 псевдоним cykadev")
            print(Fore.BLUE + "kayo1337 - увлекается пайтоном уже 2 года, добрый позитивный человек :D")
        elif choose == "3":
            suspicious_files = find_suspicious_files()
            if suspicious_files:
                handle_suspicious_files(suspicious_files)
            else:
                print(Fore.GREEN + "Подозрительных файлов не найдено.")
        elif choose == "4":
            fix_registry()
            fix_hosts()
        else:
            print(Fore.RED + "Неверный выбор. Пожалуйста, введите 1, 2, 3 или 4.")

        cont = input(Fore.WHITE + "\nХотите продолжить? (y/n): ")
        if cont.lower() != 'y':
            break

    input(Fore.WHITE + "\nНажмите Enter, чтобы выйти...")
