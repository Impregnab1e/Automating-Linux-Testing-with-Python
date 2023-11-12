import random
import string
from datetime import datetime

import paramiko
import pytest
import yaml
import time

from checkers import ssh_checkout, ssh_get
from files import upload_files

with open('config.yaml') as f:
    # chitaem document YAML
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "1111",
                        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                      data["folder_ext2"]),
                        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "1111",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename,
                                                                                               data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "1111",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                            data["folder_ext2"]), '')


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "1111", "cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
                 "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "1111", "truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")
    # yield
    # checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]),"")


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "1111", "/home/vboxuser/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "1111", "echo '1111' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "1111", "echo '1111' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)


@pytest.fixture(autouse=True)
def write_stats(request):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    stat_line = f"{current_time}, {data['count']}, {data['bs']}, {get_last_load_average()}\n"
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect("0.0.0.0", username="user2", password="1111")
        with ssh_client.open_sftp() as sftp:
            with sftp.file("stat.txt", "a") as stat_file:
                stat_file.write(stat_line)


def get_last_load_average():
    with open("/proc/loadavg", "r") as loadavg_file:
        lines = loadavg_file.readlines()
        return lines[-1].strip() if lines else "N/A"

# @pytest.fixture(autouse=True)
# def write_stat(request):
#     with open("stat.txt", "a") as stat_file:
#         current_time = time.strftime("%Y-%m-%d %H:%M:%S")
#         stat_line = f"{current_time}, {data['count']}, {data['bs']}, {get_last_load_average()}\n"
#         stat_file.write(stat_line)


# @pytest.fixture(autouse=True, scope="module")
# def start_time():
#     return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#
# # primer kak mojno sdelat'
# @pytest.fixture(scope="module")
# def safe_log(stat.txt, starttime):
#     with open(stat.txt,, 'w') as f:
#         f.write(ssh_get("0.0.0.0", "user2", "1111", "journalctl --since".format(starttime)))
