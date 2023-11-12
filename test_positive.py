import subprocess

import yaml

from checkers import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self):
        # test1
        result1 = ssh_checkout("0.0.0.0", "user2", "1111",
                               "cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "1111", "cd {}; ls".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, make_files):
        # test2
        result1 = ssh_checkout("0.0.0.0", "user2", "1111",
                               "cd {}; 7z e arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "1111", "cd {}; ls".format(data["folder_ext"]), make_files[0])
        assert result1 and result2, "test2 FAIL"

    def test_step3(self):
        # test3
        assert ssh_checkout("0.0.0.0", "user2", "1111", "cd /{}; 7z t arx2.7z".format(data["folder_out"]),
                            "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert ssh_checkout("0.0.0.0", "user2", "1111",
                            "cd {}; 7z u {}arx2.7z".format(data["folder_in"], data["folder_out"]),
                            "Everything is Ok"), "test4 FAIL"

    # def test_step5(self):
    #     # test5 HW2
    #     result1 = checkout("cd {}; 7z l arx2.7z".format(data["folder_out"]), "111")
    #     result2 = checkout("cd {}; 7z l arx2.7z".format(data["folder_out"]), "ggg")
    #     assert result1 and result2, "test5 FAIL"

    def test_step6(self):
        # test6 HW2
        assert ssh_checkout("0.0.0.0", "user2", "1111",
                            "cd {}; 7z x arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext2"]),
                            "Everything is Ok"), "test6 FAIL"
        # result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext2"]),
        #                    "Everything is Ok")
        # result2 = checkout("cd {}; ls".format(data["folder_ext2"]), "111")
        # result3 = checkout("cd {}; ls".format(data["folder_ext2"]), "ggg")
        # assert result1 and result2 and result3, "test6 FAIL"

    def test_step7(self):
        # test7
        assert ssh_checkout("0.0.0.0", "user2", "1111", "cd {}; 7z d arx2".format(data["folder_out"]),
                            "Everything is Ok"), "test7 FAIL"

    def test_step8(self):
        # test8
        archive_path = "arx2.7z"
        cmd_crc32 = 'cd {} && crc32 {}'.format(data["folder_out"], archive_path)
        cmd_7z = 'cd {} && 7z h {}'.format(data["folder_out"], archive_path)

        result1 = ssh_checkout("0.0.0.0", "user2", "1111", cmd_crc32, "")
        result2 = ssh_checkout("0.0.0.0", "user2", "1111", cmd_7z, "")

        assert result1 == result2, f'Test8 Fail. Hash mismatch. CRC32: {result1}, 7z: {result2}'
