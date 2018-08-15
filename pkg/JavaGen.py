#!/usr/bin/env python
# -*- coding: utf-8 -*-


class JavaGen:
    def __init__(self, errCodes, dstDirs):
        self.errCodes = errCodes
        self.dstDirs = dstDirs

    def gen(self):
        el = "\n"
        bl = " " * 4
        strTemplate = open("etc/java.template", "r").read()
        # 生成错误码
        # errs
        # code    msg    value
        errList = ""
        for errCode in self.errCodes:
            errList += (bl + "%s(%d, \"%s\")" + el) % (errCode.code, errCode.value, errCode.msg)
        print errList
        strTemplate = strTemplate.replace("%ErrList%", errList)
        # 生成错误映射
        for dstDir in self.dstDirs:
            open(dstDir + "/" + "errors.java", "w").write(strTemplate)





