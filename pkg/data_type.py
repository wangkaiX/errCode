#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ErrorInfo():
    def __init__(self, code, msg, number):
        self.code = code
        self.msg = msg
        self.number = number

    def __eq__(self, o):
        return self.code == o.code or self.number == o.number
