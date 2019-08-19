#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from error_code_pkg.go_err import GoGen

if __name__ == "__main__":
    gen = GoGen("etc/privategql.err", 10000, 10999, "error.go")
    print(gen.gen())
