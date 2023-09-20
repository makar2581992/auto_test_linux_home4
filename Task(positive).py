import string

import yaml
from random import random, choices
from checks import checkout, check_hash_crc32, ssh_checkout
import pytest


class TestSSHPositive:
    with open('config.yaml') as fy:
        data = yaml.safe_load(fy)

    def test_add_archive(self, make_folder, clear_folder, make_files):
        res = list()

        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'ls {self.data["folder_out"]}', f'arx2.{self.data["ta"]}'))

        assert all(res)

    def test_check_e_extract(self, clear_folder, make_files):  #
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z e arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                    f'ls {self.data["folder_ext"]}', item))

        assert all(res)

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z e arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                    f'ls {self.data["folder_ext"]}', item))
        for item in make_subfolder:
            res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                    f'ls {self.data["folder_ext"]}', item))

        assert all(res)

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        # files, subflder and files in subfolder
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z x arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                    f'ls {self.data["folder_ext"]}', item))

        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'ls {self.data["folder_ext"]}', make_subfolder[0]))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'ls {self.data["folder_ext"]}/{make_subfolder[0]}', make_subfolder[1]))

        assert all(res)

    def test_check_x_files(self, clear_folder, make_files):  # only files
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z x arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                    f'ls {self.data["folder_ext"]}', item))
        assert all(res)

    def test_totality(self, clear_folder, make_files):
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z t arx2.{self.data["ta"]}', "Everything is Ok"))

        assert all(res)

    def test_delete(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z d arx2.{self.data["ta"]}',
                                "Everything is Ok"))

        assert all(res)

    def test_update(self, make_folder, clear_folder, make_files):
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))

        file_name = ''.join(choices(string.ascii_lowercase + string.digits, k=5))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; dd if=/dev/urandom of={file_name} bs={self.data["bs"]} count=1 iflag=fullblock',
                                ''))

        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z u {self.data["folder_out"]}/arx2.{self.data["ta"]}',
                                "Everything is Ok"))

        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'7z l {self.data["folder_out"]}/arx2.{self.data["ta"]}', file_name))
        return all(res)

    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                                "Everything is Ok"))
        res.append(ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                                f'cd {self.data["folder_out"]}; 7z l arx2.{self.data["ta"]}', f'{len(make_files)} files'))


if __name__ == '__main__':
    pytest.main(['-vv'])