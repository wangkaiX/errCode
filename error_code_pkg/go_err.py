#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mako.template import Template
import os
import error_code_pkg.data_type as data_type


class GoGen:
    def __init__(self, err_file, begin_no, end_no, package_name='errno'):
        self.err_infos = []
        self.err_file = err_file
        self.begin_no = begin_no
        self.end_no = end_no
        self.package_name = package_name

    def append(self, err_info):
        if err_info not in self.err_infos:
            self.err_infos.append(err_info)

    def gen(self):
        mako_file = "etc/go.mako"
        if not os.path.exists(mako_file):
            print(mako_file + " not exists!")
            assert False

        f = open(self.err_file)
        ls = f.readlines()
        counter = self.begin_no
        for l in ls:
            assert counter <= self.end_no
            err_line = l.split()
            assert len(err_line) > 1
            if 2 == len(err_line):
                code, msg = err_line
                number = counter
                self.append(data_type.ErrorInfo(code, msg, number))
                counter = counter + 1
            elif 3 == len(err_line):
                code, msg, number = err_line
                number = int(number)
                assert number <= self.end_no
                self.append(data_type.ErrorInfo(code, msg, number))
                counter = number + 1

        t = Template(filename="etc/go.mako", input_encoding="utf8")
        return t.render(err_infos=self.err_infos, package_name=self.package_name)
