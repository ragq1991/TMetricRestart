import os
import time
import psutil
import datetime
import traceback
import subprocess
import pygetwindow as gw


def start():
    tm_started = False
    while not tm_started:
        print("Ищу запущенный TMetric...")
        window_list = gw.getAllWindows()
        tm_started = False
        for window in window_list:
            if window.title == "TMetric Desktop":
                print("Запущенный TMetric найден")
                tm_started = True
                clearLogs()
                break
        if not tm_started:
            print("Пробую запустить...")
            username = os.getlogin()
            path = f"C:\\Users\\{username}\\AppData\\Local\\TMetric Desktop"
            executable_file_path = os.path.join(path, 'TMetricDesktop.exe')
            print(executable_file_path)
            if os.path.exists(executable_file_path):
                subprocess.Popen([executable_file_path])
                time.sleep(15)
            else:
                print("Файл TMetricDesktop.exe не обнаружен")
                print("Возможные причины:")
                print("1. Исполняемый файл данной утили расположен НЕ в одном каталоге с TMetric.exe")
                print(
                    "Решение: закройте утилиту, переместите исполняемый файл в каталог расположения TMetric.exe и запустите снова")
                print("2. У исполняемого фала нет прав администратора")
                print(
                    "Решение: закройте утилиту и запустите снова нажав правой кнопкой мыши \"Запустить от имени Администратора\"")
                print("Повторная попытка запуска через 60 секунд")
                time.sleep(60)
    print('Служба запущена')


def find_error():
    print('Зпущен цикличный поиск ошибок')
    while True:
        time.sleep(1)
        window_list = gw.getAllWindows()
        started = False
        for window in window_list:
            if window.title == "TMetric Desktop" and window.width == 293 and window.height == 149:
                print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), 'проблема обнаружена')
                time.sleep(3)
                for proc in psutil.process_iter(['name']):
                    if proc.name() == 'TMetricDesktop.exe':
                        proc.kill()
                        time.sleep(2)
                        current_directory = os.path.dirname(os.path.abspath(__file__))
                        executable_file_path = os.path.join(current_directory, 'TMetricDesktop.exe')
                        subprocess.Popen([executable_file_path])
                        print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), 'проблема устранена')
                        break
            elif window.title == "TMetric Desktop":
                started = True
        if not started == True:
            print('Не найден запущенный TMetric')
            return


def clearLogs():
    username = os.getlogin()
    folder_to_delete = f"C:\\Users\\{username}\\AppData\\Roaming\\Devart\\TMetric Desktop"

    try:
        # Получаем список файлов в папке
        files = os.listdir(folder_to_delete)

        # Перебираем файлы и удаляем их
        for file_name in files:
            file_path = os.path.join(folder_to_delete, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Файл {file_name} удален.")

        print("Все файлы в папке успешно удалены.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    while True:
        try:
            start()
            find_error()
        except Exception as e:
            # Записываем ошибку в файл
            with open("error_log.txt", "w") as f:
                f.write("An error occurred: " + str(e) + "\n")
                f.write(traceback.format_exc())


main()
