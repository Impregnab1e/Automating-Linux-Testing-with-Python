import random
import string
import pytest
import yaml
import time

from checkers import checkout

with open('config.yaml') as f:
    # chitaem document YAML
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return checkout(
        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"]),
        "")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename,
                                                                                           data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                        data["folder_ext2"]), '')


@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
             "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")
    # yield
    # checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]),"")


@pytest.fixture(autouse=True)
def write_stat(request):
    with open("stat.txt", "a") as stat_file:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        stat_line = f"{current_time}, {data['count']}, {data['bs']}, {get_last_load_average()}\n"
        stat_file.write(stat_line)


def get_last_load_average():
    with open("/proc/loadavg", "r") as loadavg_file:
        lines = loadavg_file.readlines()
        return lines[-1].strip() if lines else "N/A"
