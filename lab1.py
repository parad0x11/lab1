import getpass
import json
import os
import platform
import shutil
import time
import urllib.request
import uuid


def get_public_ip() -> str:
    url = "https://ipv4.internet.yandex.net/api/v0/ip"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as response:
            return json.loads(response.read().decode("utf-8").strip())
    except Exception:
        return "Unavailable / Offline"


def get_common_info() -> dict:
    # сбор универсальных параметров под все ОС
    raw_mac = f"{uuid.getnode():012x}"
    mac_address = ":".join(raw_mac[i : i + 2] for i in range(0, 12, 2))

    return {
        "os_type": platform.system(),
        "hostname": platform.node(),
        "architecture": platform.machine(),
        "cpu_cores": os.cpu_count(),
        "current_user": getpass.getuser(),
        "timezone": time.tzname[0],
        "mac_address": mac_address,
        "public_ip": get_public_ip(),
        "python_version": platform.python_version(),
    }


def get_linux_info() -> dict:       # сбор параметров для linux
    # определение дистрибутива
    distro_name = "Linux"
    if hasattr(platform, "freedesktop_os_release"):
        try:
            distro_name = platform.freedesktop_os_release().get("PRETTY_NAME", "Linux")
        except OSError:
            pass
    elif os.path.exists("/etc/os-release"):
        with open("/etc/os-release", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    distro_name = line.split("=", 1)[1].strip().strip('"\'')
                    break

    # определение модели процессора
    cpu_model = "Unknown"
    if os.path.exists("/proc/cpuinfo"):
        with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
            for line in f:
                if "model name" in line:
                    cpu_model = line.split(":", 1)[1].strip()
                    break

    # определение аптайма машины
    uptime_hours = 0.0
    if os.path.exists("/proc/uptime"):
        with open("/proc/uptime", "r", encoding="utf-8") as f:
            uptime_hours = round(float(f.readline().split()[0]) / 3600, 2)

    # объем диска и ОЗУ
    root_disk = shutil.disk_usage("/")
    ram_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")

    return {
        "distro": distro_name,
        "kernel": platform.release(),
        "cpu_model": cpu_model,
        "uptime_hours": uptime_hours,
        "ram_total_gb": round(ram_bytes / (1024**3), 2),
        "disk_total_gb": round(root_disk.total / (1024**3), 2),
        "disk_free_gb": round(root_disk.free / (1024**3), 2),
    }


def get_windows_info() -> dict:
    return {
        "windows_release":planform.release(),
        "windows_version": planform.version(),
        "processor": planform.processor(),
        "working_folder": os.getcwd(),
    }
        


def main():
    current_os = platform.system()
    print(f"Запуск скрипта. ОС: {current_os}")

    # сбор универсальных параметров
    result_data = get_common_info()

    # сбор ОС-специфичных параметров
    if current_os == "Linux":
        result_data.update(get_linux_info())
    elif current_os == "Windows":
        result_data.update(get_windows_info())
    else:
        print(f"Операционная система {current_os} не поддерживается.")
        return

    # запись в JSON
    output_filename = "result.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=4, ensure_ascii=False)

    print(f"Данные успешно записаны в {output_filename}")


if __name__ == "__main__":
    main()
