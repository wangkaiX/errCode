#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mako.template import Template
import os
import error_code_pkg.data_type as data_type


class GoGen:
    def __init__(self, error_file, begin_no, end_no, out_file):
        self.err_infos = []
        self.error_file = error_file
        self.begin_no = begin_no
        self.end_no = end_no
        self.out_file = out_file
        self.package_name = os.path.basename(os.path.dirname(out_file))

    def append(self, err_info):
        if err_info not in self.err_infos:
            self.err_infos.append(err_info)

    def gen(self):
        print("error_file:", self.error_file)
        if not os.path.exists(self.error_file):
            print(self.error_file + " not exists!")
            assert False

        f = open(self.error_file)
        ls = f.readlines()
        counter = self.begin_no
        for l in ls:
            if l.strip(" \n\r\t") == "" or l[0] == "#":
                continue
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

        curr_path = os.path.split(os.path.realpath(__file__))[0] + "/../"
        mako_file = curr_path + "etc/error.go"
        t = Template(filename=mako_file, input_encoding="utf8")
        s = t.render(err_infos=self.err_infos, package_name=self.package_name)
        with open(self.out_file, "w") as f:
            f.write(s)
        return s
