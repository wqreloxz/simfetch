import psutil
import platform
import os
import time
import datetime

#Сбор данных

# Используем другое имя, чтобы не испортить модуль os
sys_info = platform.freedesktop_os_release()
distro = sys_info.get('PRETTY_NAME', 'Linux')
distro_id = sys_info.get('ID', 'linux') # Нужно для выбора логотипа

kernel = platform.release()
arch = platform.machine()

# Окружение и оболочка
de = os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')
shell = os.environ.get('SHELL', '/bin/bash').split('/')[-1]

# Железо
cpu = platform.processor() or "Generic CPU"
ram = psutil.virtual_memory()
disk = psutil.disk_usage('/')

# Температура (с защитой от ошибок)
try:
    temps = psutil.sensors_temperatures()
    # Берем первый попавшийся датчик
    curr_temp = list(temps.values())[0][0].current if temps else "N/A"
except:
    curr_temp = "N/A"

# Файловая система
fs_type = "Unknown"
for p in psutil.disk_partitions():
    if p.mountpoint == '/':
        fs_type = p.fstype
        break

# Аптайм (переводим из секунд в читаемый вид)
uptime_sec = time.time() - psutil.boot_time()
uptime = str(datetime.timedelta(seconds=int(uptime_sec)))

# Подготовка логотипа и инфо

# Выбираем логотип в зависимости от ID системы
if "ubuntu" in distro_id:
    logo = [
        "     .--.       ",
        "    |o_o |      ",
        "    |:_/ |      ",
        "   //   \\ \\     ",
        "  (|     | )    ",
        " /'\_   _/`\\    ",
        " \___)=(___/    "
    ]
else: # Стандартный пингвин (очень упрощенный)
    logo = [
        "     .--.       ",
        "    |o_o |      ",
        "    |:_/ |      ",
        "   //   \\ \\     ",
        "  (|     | )    ",
        " /'\_   _/`\\    ",
        " \___)=(___/    "
    ]

# Формируем список строк с данными
info = [
    f"\033[1;32mOS:\033[0m {distro}",
    f"\033[1;32mKernel:\033[0m {kernel} ({arch})",
    f"\033[1;32mDE:\033[0m {de}",
    f"\033[1;32mShell:\033[0m {shell}",
    f"\033[1;32mCPU:\033[0m {cpu[:20]}...",
    f"\033[1;32mTemp:\033[0m {curr_temp}°C",
    f"\033[1;32mRAM:\033[0m {ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB",
    f"\033[1;32mDisk:\033[0m {disk.percent}% ({fs_type})",
    f"\033[1;32mUptime:\033[0m {uptime}"
]

# Вывод

print("\n \033[1;36m--- SYSTEM INFO ---\033[0m\n")

# Определяем, сколько строк выводить (максимум из лого или инфо)
max_lines = max(len(logo), len(info))

for i in range(max_lines):
    # Берем строку лого или пустую строку, если лого кончилось
    l_line = logo[i] if i < len(logo) else " " * 16
    # Берем строку инфо или пусто
    i_line = info[i] if i < len(info) else ""
    
    # Печатаем их в один ряд
    print(f"{l_line}   {i_line}")
    time.sleep(0.8) # Твой эффект задержки

print("\n")
