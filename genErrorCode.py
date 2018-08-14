#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
#import defines
import ConfigParser
from pkg.JavaGen import JavaGen
from pkg.GoGen import GoGen
from pkg.CGen import CGen
from pkg.ErrCode import ErrCode

#dstDirs = defines.dstDirs
#dstLanguages = defines.dstLanguages
#srcErrFiles = defines.srcErrFiles
#gitAddList = defines.gitAddList


cf = ConfigParser.ConfigParser()
configFile = "etc/range.config"



def genGo(errList, dstDirs):
    gen = GoGen(errList, dstDirs)
    gen.gen()

    return


def genJava(errList, dstDirs):
    gen = JavaGen(errList, dstDirs)
    gen.gen()

    return


def genC(errList, dstDirs):
    gen = CGen(errList, dstDirs)
    gen.gen()

    return


def readFile(fileName):
    file = open(fileName)
    value = -1
    errList = []
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
    return errList


def readErrs(srcErrFiles):
    if 0 == len(srcErrFiles):
        srcErrFiles = os.popen("ls etc/*.err").read().split()
    errList = []
    for srcErrFile in srcErrFiles:
        errList += readFile(srcErrFile)
    return errList


# if __name__ == "__main__":
def genErrors(srcErrFiles, dstDirs, dstLanguages, gitAddList):
    assert(len(dstDirs) and len(dstLanguages))
    assert(os.path.exists(configFile))
    # 先更新git
    if 0 != os.system("git pull"):
        assert False
    cf.read(configFile)
    # 读入错误配置
    errList = readErrs(srcErrFiles)
    for dstLanguage in dstLanguages:
        if "go" == dstLanguage:
            genGo(errList, dstDirs)
        elif "c" == dstLanguage:
            genC(errList, dstDirs)
        elif "java" == dstLanguage:
            genJava(errList, dstDirs)
        else:
            assert False

    # 同步git
    strAdd = "git add " + " ".join(gitAddList)
    print strAdd
    os.system(strAdd)
    os.system("git commit -m\"更新错误码\"")
    if 0 != os.system("git push"):
        assert False


