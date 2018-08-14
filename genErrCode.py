#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import defines
import ConfigParser
from pkg.JavaGen import JavaGen
from pkg.GoGen import GoGen
from pkg.CGen import CGen
from pkg.ErrCode import ErrCode

dstDirs = defines.dstDirs
dstLanguages = defines.dstLanguages
srcErrFiles = defines.srcErrFiles
gitAddList = defines.gitAddList


cf = ConfigParser.ConfigParser()
configFile = "etc/range.config"

errList = []


def genGo():
    gen = GoGen(errList, dstDirs)
    gen.gen()

    return


def genJava():
    gen = JavaGen(errList, dstDirs)
    gen.gen()

    return


def genC():
    gen = CGen(errList, dstDirs)
    gen.gen()

    return


def readFile(fileName):
    file = open(fileName)
    value = -1
    for l in file.readlines():
        if '#' == l[0]:
            continue
        errCode = l.split()
        if 2 == len(errCode):
            assert(-1 != value)
            code, msg = errCode
            value = value + 1
        elif 3 == len(errCode):
            code, msg, value = errCode
            value = int(value)
        else:
            print "配置文件有误[" + fileName + "]"
            assert False
        errList.append(ErrCode(code, msg, value))

    #print errList
    return


def readErrs():
    global srcErrFiles
    if 0 == len(srcErrFiles):
        srcErrFiles = os.popen("ls etc/*.err").read().split()
    for srcErrFile in srcErrFiles:
        readFile(srcErrFile)





if __name__ == "__main__":
    assert(len(dstDirs) and len(dstLanguages))
    assert(os.path.exists(configFile))
    # 先更新git
    os.system("git pull")
    cf.read(configFile)
    # 读入错误配置
    readErrs()
    for dstLanguage in dstLanguages:
        if "go" == dstLanguage:
            genGo()
        elif "c" == dstLanguage:
            genC()
        elif "java" == dstLanguage:
            genJava()
        else:
            assert False

    # 同步git
    strAdd = "git add " + " ".join(gitAddList)
    print strAdd
    os.system(strAdd)
    os.system("git commit -m\"更新错误码\"")
    os.system("git push")


