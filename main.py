#!/usr/bin/env python3
import platform
import os
import time
import subprocess
import sys
from colorama import init, Fore, Back, Style

# Инициализация colorama
init(autoreset=True)

def get_os_info():
    # Получить информацию об ОС/os info
    system = platform.system()
    if system == "Linux":
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=')[1].strip().strip('"')
        except:
            return "Linux"
    elif system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    elif system == "Windows":
        return f"Windows {platform.win32_ver()[0]}"
    else:
        return system

def get_uptime():
    #Получить время работы системы/using time
    try:
        if os.path.exists('/proc/uptime'):
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                return f"{hours}h {minutes}m"
        else:
            return "N/A"
    except:
        return "N/A"

def get_shell():
    if platform.system() == "Windows":
        return "cmd.exe"
    else:
        return os.path.basename(os.environ.get('SHELL', 'bash'))

def get_packages():
    #Получить количество пакетов/number of packages 
    try:
        if platform.system() == "Linux":
            result = subprocess.run(['dpkg', '--list'], capture_output=True, text=True)
            if result.returncode == 0:
                count = len([line for line in result.stdout.split('\n') if line.startswith('ii')])
                return str(count)
    except:
        pass
    return "N/A"

def get_disk_usage():
    #Получить использование диска/disk using 
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        used_gb = used // (2**30)
        total_gb = total // (2**30)
        return f"{used_gb}GB / {total_gb}GB"
    except:
        return "N/A"

def show_system_info():
    #Показать информацию о системе/system info
    info = {
        Fore.GREEN + "OS": get_os_info(),
        Fore.GREEN + "Kernel": platform.release(),
        Fore.GREEN + "Uptime": get_uptime(),
        Fore.GREEN + "Shell": get_shell(),
        Fore.GREEN + "Packages": get_packages(),
        Fore.GREEN + "Disk": get_disk_usage(),
        Fore.GREEN + "Terminal": os.environ.get('TERM', 'N/A')
    }
    
    for key, value in info.items():
        print(f"{key:15} {Fore.WHITE}{value}")

def edit_file(file_path):
    #Редактировать файл
    if not os.path.exists(file_path):
        print(Fore.RED + f"Файл не существует: {file_path}")
        return
    
    if os.path.isdir(file_path):
        print(Fore.RED + f"Это папка, а не файл: {file_path}")
        return
    
    try:
        # Читаем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            print(Fore.RED + "Не удалось прочитать файл (бинарный файл?)")
            return
    except Exception as e:
        print(Fore.RED + f"Ошибка чтения файла: {e}")
        return
    
    print(Fore.CYAN + f"\n┌── Редактирование файла: {file_path}")
    print(Fore.CYAN + "│")
    print(Fore.CYAN + "│" + Fore.YELLOW + " Команды редактора:")
    print(Fore.CYAN + "│" + Fore.GREEN + " :w" + Fore.WHITE + " - сохранить и выйти")
    print(Fore.CYAN + "│" + Fore.GREEN + " :q" + Fore.WHITE + " - выйти без сохранения")
    print(Fore.CYAN + "│" + Fore.GREEN + " :wq" + Fore.WHITE + " - сохранить и выйти")
    print(Fore.CYAN + "│")
    print(Fore.CYAN + "└──" + Fore.YELLOW + " Начните редактирование (пустая строка для завершения):")
    
    lines = content.split('\n')
    new_lines = []
    
    # Показываем текущее содержимое с нумерацией
    for i, line in enumerate(lines, 1):
        print(f"{Fore.BLUE}{i:3}{Fore.WHITE}│ {line}")
    
    print(Fore.CYAN + "\nВведите новые строки (пустая строка для завершения):")
    
    line_number = 1
    while True:
        try:
            user_input = input(f"{Fore.BLUE}{line_number:3}{Fore.WHITE}│ ")
            
            if user_input.strip() in [':w', ':q', ':wq']:
                command = user_input.strip()
                break
            elif user_input == "":
                # Пустая строка - завершаем ввод
                break
            else:
                new_lines.append(user_input)
                line_number += 1
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nПрервано пользователем")
            return
        except EOFError:
            break
    
    # Обрабатываем команды редактора
    if 'command' in locals():
        if command == ':w' or command == ':wq':
            # Сохраняем файл
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                print(Fore.GREEN + f"Файл сохранен: {file_path}")
            except Exception as e:
                print(Fore.RED + f"Ошибка сохранения: {e}")
        elif command == ':q':
            print(Fore.YELLOW + "Выход без сохранения")
            return
    else:
        # Сохраняем если был обычный ввод
        save = input(Fore.YELLOW + "Сохранить файл? (y/N): ").lower()
        if save == 'y':
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                print(Fore.GREEN + f"Файл сохранен: {file_path}")
            except Exception as e:
                print(Fore.RED + f"Ошибка сохранения: {e}")

def view_file(file_path):
    """Просмотреть содержимое файла"""
    if not os.path.exists(file_path):
        print(Fore.RED + f"Файл не существует: {file_path}")
        return
    
    if os.path.isdir(file_path):
        print(Fore.RED + f"Это папка, а не файл: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            print(Fore.RED + "Не удалось прочитать файл (бинарный файл?)")
            return
    except Exception as e:
        print(Fore.RED + f"Ошибка чтения файла: {e}")
        return
    
    print(Fore.CYAN + f"\n┌── Содержимое файла: {file_path}")
    print(Fore.CYAN + "│")
    lines = content.split('\n')
    for i, line in enumerate(lines[:50], 1):  # Показываем первые 50 строк
        print(f"{Fore.BLUE}{i:3}{Fore.WHITE}│ {line}")
    
    if len(lines) > 50:
        print(Fore.YELLOW + f"└── Показано 50 из {len(lines)} строк")
    else:
        print(Fore.CYAN + "└──")

def file_manager():
    """Простой файловый менеджер"""
    current_dir = os.getcwd()
    
    while True:
        print(f"\n{Fore.BLUE}┌──[{Fore.CYAN}Файловый менеджер{Fore.BLUE}]──[{Fore.YELLOW}{current_dir}{Fore.BLUE}]")
        print(f"{Fore.BLUE}│")
        print(f"{Fore.BLUE}│ {Fore.WHITE}Доступные команды:")
        print(f"{Fore.BLUE}│ {Fore.GREEN}ls{Fore.WHITE} - список файлов")
        print(f"{Fore.BLUE}│ {Fore.GREEN}cd <папка>{Fore.WHITE} - перейти в папку")
        print(f"{Fore.BLUE}│ {Fore.GREEN}mkdir <имя>{Fore.WHITE} - создать папку")
        print(f"{Fore.BLUE}│ {Fore.GREEN}touch <имя>{Fore.WHITE} - создать файл")
        print(f"{Fore.BLUE}│ {Fore.GREEN}rm <имя>{Fore.WHITE} - удалить файл/папку")
        print(f"{Fore.BLUE}│ {Fore.GREEN}edit <файл>{Fore.WHITE} - редактировать файл")
        print(f"{Fore.BLUE}│ {Fore.GREEN}view <файл>{Fore.WHITE} - просмотреть файл")
        print(f"{Fore.BLUE}│ {Fore.GREEN}pwd{Fore.WHITE} - текущая директория")
        print(f"{Fore.BLUE}│ {Fore.GREEN}exit{Fore.WHITE} - выйти")
        print(f"{Fore.BLUE}│")
        
        try:
            command = input(f"{Fore.BLUE}└──{Fore.CYAN}➜{Fore.WHITE} ").strip().split()
            
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == 'exit':
                print(Fore.YELLOW + "Выход из файлового менеджера...")
                break
                
            elif cmd == 'ls':
                try:
                    items = os.listdir(current_dir)
                    print(f"\n{Fore.CYAN}Содержимое {current_dir}:")
                    for item in items:
                        full_path = os.path.join(current_dir, item)
                        if os.path.isdir(full_path):
                            print(Fore.BLUE + f"  📁 {item}")
                        else:
                            size = os.path.getsize(full_path)
                            print(Fore.GREEN + f"  📄 {item} ({size} байт)")
                except Exception as e:
                    print(Fore.RED + f"Ошибка: {e}")
                    
            elif cmd == 'cd' and len(command) > 1:
                new_dir = command[1]
                if new_dir == "..":
                    current_dir = os.path.dirname(current_dir)
                else:
                    new_path = os.path.join(current_dir, new_dir)
                    if os.path.exists(new_path) and os.path.isdir(new_path):
                        current_dir = new_path
                    else:
                        print(Fore.RED + f"Папка не найдена: {new_path}")
                        
            elif cmd == 'mkdir' and len(command) > 1:
                dir_name = command[1]
                try:
                    os.makedirs(os.path.join(current_dir, dir_name), exist_ok=True)
                    print(Fore.GREEN + f"Папка создана: {dir_name}")
                except Exception as e:
                    print(Fore.RED + f"Ошибка создания папки: {e}")
                    
            elif cmd == 'touch' and len(command) > 1:
                file_name = command[1]
                try:
                    with open(os.path.join(current_dir, file_name), 'w') as f:
                        pass
                    print(Fore.GREEN + f"Файл создан: {file_name}")
                except Exception as e:
                    print(Fore.RED + f"Ошибка создания файла: {e}")
                    
            elif cmd == 'rm' and len(command) > 1:
                target = command[1]
                target_path = os.path.join(current_dir, target)
                try:
                    if os.path.isdir(target_path):
                        os.rmdir(target_path)
                        print(Fore.GREEN + f"Папка удалена: {target}")
                    else:
                        os.remove(target_path)
                        print(Fore.GREEN + f"Файл удален: {target}")
                except Exception as e:
                    print(Fore.RED + f"Ошибка удаления: {e}")
                    
            elif cmd == 'edit' and len(command) > 1:
                file_name = command[1]
                file_path = os.path.join(current_dir, file_name)
                edit_file(file_path)
                
            elif cmd == 'view' and len(command) > 1:
                file_name = command[1]
                file_path = os.path.join(current_dir, file_name)
                view_file(file_path)
                    
            elif cmd == 'pwd':
                print(Fore.CYAN + f"Текущая директория: {current_dir}")
                
            else:
                print(Fore.RED + "Неизвестная команда")
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nВыход из файлового менеджера...")
            break
        except Exception as e:
            print(Fore.RED + f"Ошибка: {e}")

def main():
    #Основная функция
    print(Fore.GREEN + "Simfetch - simple neofetch for Linux, Windows and macOS!")
    
    # Показываем информацию о системе
    show_system_info()
    
    # Запускаем файловый менеджер
    print(f"\n{Fore.YELLOW}Запуск файлового менеджера...")
    file_manager()

if __name__ == "__main__":
    main()
