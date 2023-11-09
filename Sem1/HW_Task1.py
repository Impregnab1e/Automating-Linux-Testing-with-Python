# import subprocess
#
# def check_command_output(command, text_to_find):
#     result = subprocess.run(args=command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
#     if result.returncode == 0 and text_to_find in result.stdout:
#         return True
#     return False
#
# command = "ls /snap"
# text = 'README'
# if check_command_output(command, text):
#     print("SUCCESS")
# else:
#     print("FAIL")
#

import subprocess

def check_command_output(command, text_to_find):
    try:
        result = subprocess.run(args=command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if result.returncode == 0:
            if text_to_find in result.stdout:
                return True
        return False
    except Exception as e:
        return False

def main():
    command = "ls /snap"
    text = 'README'
    if check_command_output(command, text):
        print("SUCCESS")
    else:
        print("FAIL")

if __name__ == "__main__":
    main()
