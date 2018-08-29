#!/usr/bin/env python
# -*- coding: utf-8 -*-

from genErrorCode import genErrors

# ["pro/src/"]不指定则不生成
# dstDirs = ["../", "/tmp", "."]
dstDirs = ["."]

# ["c", "java", "go"]不指定则不生成
# dstLanguages = ["c", "java", "go"]
dstLanguages = ["go", "java"]

# ["a.err", "b.err"]不指定则默认生成所有的错误码
srcErrFiles = []

# 需要同步及更新的文件
gitAddList = ["genErrorCode.py", "etc/*.err", "etc/range.config", "etc/*.template", "pkg/*.py", "readme", "run.py"]

if __name__ == "__main__":
    genErrors(srcErrFiles, dstDirs, dstLanguages, gitAddList)
#
