# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess

def check_command_output(command, text_to_find):
    result = subprocess.run(args=command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0 and text_to_find in result.stdout:
        return True
    return False

command = "ls /snap"
text = 'README'
if check_command_output(command, text):
    print("SUCCESS")
else:
    print("FAIL")
