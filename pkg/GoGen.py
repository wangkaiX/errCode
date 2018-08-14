#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

class GoGen:
    def __init__(self, errCodes, dstDirs):
        self.errCodes = errCodes
        self.dstDirs = dstDirs

    def gen(self):
        el = "\n"
        bl = " " * 4
        strTemplate = open("etc/go.template", "r").read()
        #if not os.path.exists("tmp"):
        #    os.mkdir("tmp")
        #file = open("tmp/errors.go", "w")
        # 生成错误码
        # errs
        # code    msg    value
        errKeyList = ""
        errValueList = ""
        for errCode in self.errCodes:
            errKeyList += (bl + "%-32s ErrCode = %d" + el) % (errCode.code, errCode.value)
            errValueList += (bl + "%-32s\"%s\"," + el) % (errCode.code+":", errCode.msg)
        print errKeyList
        strTemplate = strTemplate.replace("%ErrKeyList%", errKeyList)
        strTemplate = strTemplate.replace("%ErrValueList%", errValueList)
        # 生成错误映射
        currDir = os.getcwd()
        for dstDir in self.dstDirs:
            os.chdir(dstDir)
            packageName = os.path.basename(os.getcwd())
            os.chdir(currDir)
            open(dstDir + "/" + "errors.go", "w").write(strTemplate.replace("%PackageName%", packageName))





