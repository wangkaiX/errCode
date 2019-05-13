#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from error_code_pkg.go_err import GoGen

if __name__ == "__main__":
    go_err = GoGen("etc/privategql.err", 40000, 50000)
    open("error.go", "w").write(go_err.gen())
    print(go_err.gen())
