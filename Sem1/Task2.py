import subprocess
if __name__ == '__main__':
    result = subprocess.run(args="cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout

    if result.returncode == 0:
        lst = out.split("\n")
        if 'VERSION="22.04.2 LTS (Jammy Jellyfish)"' in lst and 'VERSION_CODENAME=jammy' in lst:
            print("SUCCESS")
        else:
            print("FAIL")
    else:
        print('Fail! Result code !=0')
