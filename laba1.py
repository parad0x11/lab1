import platform
import os
import socket
import shutil
import getpass
print("Операционная система:")
print("Система:", platform.system())
print("Версия:",platform.version())
print("Релиз:", platform.release())
print("Полное имя:", platform.platform())
print("Оборудование:")
print("Архитектура:", platform.machine())
print("Процессор:", platform.processor or "Не определен")
print("Ядра:", os.cpu_count())
print("Имя компьютера:", socket.gethostname())
print("Имя пользователя:", getpass.getuser())


#более короткая программа, но без имени компьютера и пользователя
import platform, os, shutil
print(platform.uname())
print("Ядра:", os.cpu_count())


