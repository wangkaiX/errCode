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
        curr_path = os.path.split(os.path.realpath(__file__))[0] + "/../"
        mako_file = curr_path + mako_file
        print("mako_file:", mako_file)
        if not os.path.exists(mako_file):
            print(mako_file + " not exists!")
            assert False

        f = open(self.err_file)
        ls = f.readlines()
        counter = self.begin_no

        def check_number(number, begin, end):
            if 0 != number:
                assert number >= begin and number <= end

        for l in ls:
            if l.strip(" \n\r\t") == "" or l[0] == "#":
                continue

            err_line = l.split()
            assert len(err_line) > 1
            if 2 == len(err_line):
                code, msg = err_line
                check_number(counter, self.begin_no, self.end_no)
                number = counter
                self.append(data_type.ErrorInfo(code, msg, number))
                counter = counter + 1
            elif 3 == len(err_line):
                code, msg, number = err_line
                number = int(number)
                check_number(number, self.begin_no, self.end_no)
                self.append(data_type.ErrorInfo(code, msg, number))
                counter = number + 1

        t = Template(filename=mako_file, input_encoding="utf8")
        return t.render(err_infos=self.err_infos, package_name=self.package_name)
