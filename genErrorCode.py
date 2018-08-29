#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess
import sys
from collections import defaultdict
import ConfigParser
from pkg.JavaGen import JavaGen
from pkg.GoGen import GoGen
from pkg.CGen import CGen
from pkg.ErrCode import ErrCode


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


def git_pull():
    if 0 != os.system("git stash"):
        assert False
    if 0 != os.system("git pull"):
        assert False
    prog = subprocess.Popen(["git", "stash", "pop"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (outstr, errstr) = prog.communicate()
    # print(outstr, errstr)
    if -1 == outstr.find("Dropped") and \
            -1 == errstr.find("No stash"):
        assert False


def readFile(fileName):
    file = open(fileName, "r")
    value = -1
    errList = []
    i = 0
    lines = file.readlines()
    for l in lines:
        i = i + 1
        if '#' == l[0]:
            continue
        errCode = l.split()
        if 2 == len(errCode):
            if -1 == value:
                print("没有配置起始错误码!")
                assert(-1 != value)
            code, msg = errCode
            value = value + 1
        elif 3 == len(errCode):
            code, msg, value = errCode
            value = int(value)
        else:
            print("配置文件[" + fileName + "]有误, 第" + str(i) + "行")
            assert False
        errList.append(ErrCode(code, msg, value))
    # 增加防冲突分割线
    file = open(fileName, "w")
    i = None
    cut_off = '#' * 20 + "在分割线后增加" + '#' * 20 + '\n'
    try:
        i = lines.index(cut_off)
    except ValueError:
        lines.append(cut_off)
    else:
        lines.pop(i)
        lines.append(cut_off)
    file.writelines(lines)

    return errList


def readErrs(srcErrFiles):
    if 0 == len(srcErrFiles):
        srcFiles = os.listdir("etc")
        print("srcFiles")
        for file in srcFiles:
            print file.split(".")[-1]
            if file.split(".")[-1] == ".err":
                srcErrFiles.append("etc/"+file)

    errList = []
    print(srcErrFiles)
    for srcErrFile in srcErrFiles:
        errList += readFile(srcErrFile)
    return errList


def checkErrorRange(cf):
    class ErrorRange:
        def __init__(self, b, e):
            self.b = b
            self.e = e

        def __str__(self):
            return str(self.b) + " " + str(self.e)

    # 检测每个项目的错误码范围是否有重合
    errorRangeDict = defaultdict(list)
    for section in cf.sections():
        i = 0
        b = "begin" + str(i)
        e = "end" + str(i)
        while cf.has_option(section, b) and cf.has_option(section, e):
            errorRangeDict[section].append(ErrorRange(cf.getint(section, b), cf.getint(section, e)))
            i = i+1
            b = "begin" + str(i)
            e = "end" + str(i)
    errorRangeLists = errorRangeDict.values()
    errorRangeList = []
    for l in errorRangeLists:
        errorRangeList += l
    # for i in range(0, len(errorRangeList)):
    #     print errorRangeList[i].b, errorRangeList[i].e

    for i in range(0, len(errorRangeList)):
        assert(errorRangeList[i].b < errorRangeList[i].e)
        for j in range(i+1, len(errorRangeList)):
            if (errorRangeList[j].b <= errorRangeList[i].b <= errorRangeList[j].e) \
            or (errorRangeList[j].b <= errorRangeList[i].e <= errorRangeList[j].e) \
            or (errorRangeList[i].b <= errorRangeList[j].b <= errorRangeList[i].e):
                print("项目错误码范围重叠")
                assert False

    # 检测每个项目是否超过所规则的错误码范围
    srcFiles = os.listdir("etc")
    srcErrFiles = []
    for file in srcFiles:
        if file.split(".")[-1] == ".err":
            srcErrFiles.append("etc/" + file)

    print(srcErrFiles)
    for srcErrFile in srcErrFiles:
        section = os.path.basename(srcErrFile).split(".")[0]
        if not cf.has_section(section):
            print("请先给项目[" + section + "]配置错误码范围")
            assert False
        errList = readFile(srcErrFile)
        for err in errList:
            for errRange in errorRangeDict[section]:
                if not errRange.b <= err.value <= errRange.e:
                    print("错误码[" + section + "][" + err.code + "]超过范围")
                    assert False


def gitSync(gitAddList):
    # 同步git
    strAdd = "git add " + " ".join(gitAddList)
    if 0 != os.system(strAdd):
        assert False
    prog = subprocess.Popen(["git", "commit", "-m\"更新错误码\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (outstr, errstr) = prog.communicate()
    print("out:", outstr, "err:", errstr)
    print("retcode:", prog.returncode)
    if 0 == prog.returncode:
        if 0 != os.system("git push"):
            assert False
        return
    print("find:", errstr.find("Your branch is up to date"))
    if -1 != outstr.find("Your branch is up to date"):
        return
    else:
        assert False


def genErrors(srcErrFiles, dstDirs, dstLanguages, gitAddList):
    assert(len(dstDirs) and len(dstLanguages))
    assert(os.path.exists(configFile))
    # 先同步git
    git_pull()
    cf.read(configFile)
    # 检查错误码范围是否有重叠
    checkErrorRange(cf)
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
    gitSync(gitAddList)

