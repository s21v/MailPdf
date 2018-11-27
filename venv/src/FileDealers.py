import os
import shutil
import zipfile
import re
import DateCalendar

'''
    文件的拷贝与压缩
'''
# 文件复制
_baseSrcDir = u"\\\\192.168.0.160\\backup\\数字报备份\\{0:4d}{1:0>2d}"
_baseSrcFile = 'gab\\{3:0>2d}B{3:0>2d}B{0:4d}{1:0>2d}{2:0>2d}C.pdf'
_baseSrcFileBak = 'gab\\{3:0>2d}B{3:0>2d}B{0:4d}{1:0>2d}{2:0>2d}B.pdf'
_baseDstDir = u'D:\\\\工作需要\\山东周刊\\{0:4d}{1:0>2d}\\{0:4d}{1:0>2d}{2:0>2d}'
# 待压缩目录路径模板
_baseZipInputDir = u'D:\\\\工作需要\\山东周刊\\{0:4d}{1:0>2d}'
# 压缩文件名模板
_baseZipOutputFile = u'D:\\\\工作需要\\山东周刊\\山东周刊{0:4d}年{1:d}月pdf文件汇总.zip'


def copyFile(year, mon):
    '''
    复制文件 源地址：baseSrcDir, 目标地址：baseDstDir
    :param year: 年
    :param mon: 月
    :return:
    '''
    srcFilePathList = matchInMonth(year, mon)
    for path in srcFilePathList:
        day = int(path[-2:])
        for banmian in range(5, 9):
            srcFile = os.path.join(path, _baseSrcFile.format(year, mon, day, banmian))
            dstDir = _baseDstDir.format(year, mon, day)
            # 若源文件不存在，退出
            if os.path.exists(srcFile) is False:
                print("文件不存在: " + srcFile)
                print("转用备用连接。。。")
                srcFile = os.path.join(path, _baseSrcFileBak.format(year, mon, day, banmian))
                if os.path.exists(srcFile) is False:
                    print("备用连接，文件不存在: " + srcFile)
                    return
            # 若目标文件夹不存在，创建
            if os.path.exists(dstDir) is False:
                os.makedirs(dstDir)
            try:
                shutil.copy(srcFile, dstDir)
            except Exception as e:
                print("{}文件复制过程出错:\n{}".format(srcFile, e))


def zipDir(year, mon):
    # 待压缩目录
    zipInputDir = _baseZipInputDir.format(year, mon)
    # 压缩文件
    zipOutputFile = _baseZipOutputFile.format(year, mon)
    zipFile = zipfile.ZipFile(zipOutputFile, 'w')
    # 遍历待压缩目录
    try:
        for (root, dirs, files) in os.walk(zipInputDir):
            if len(dirs) == 0 and len(files) != 0:
                for file in files:
                    zipFile.write(root + os.sep + file, root.split('\\')[-1] + os.sep + file)   #第二个参数是文件在压缩包中的显示名称
        return zipOutputFile
    except Exception as e:
        print("压缩文件过程中出错：" + e)
        return None
    finally:
        zipFile.close()


def matchInMonth(year, month):
    # 正则表达式
    basePatternStr = '{0:4d}-?{1:0>2d}-?{2:0>2d}'  # YYYYMMDD 或者 YYYY-MM-DD 0向左填充
    # 当月周二的日期
    tuesdayList = DateCalendar.getAllTuesday(year, month)
    # 当月文档路径
    srcDir = _baseSrcDir.format(year, month)
    # 循环计数
    count = 0
    # 列表索引
    index = 0
    # 按照修改时间排序的文件夹目录列表
    dirList = sorted(os.listdir(srcDir), key=lambda x: os.path.getmtime(os.path.join(srcDir, x)))
    resultList = list()
    for item in dirList:
        count = count + 1
        # 带匹配正则表达式的字符串：pdf文件所在文件夹名
        wait2Matched = item.split('\\')[-1]
        # 格式化正则表达式
        patternStr = basePatternStr.format(year, month, tuesdayList[index])
        # 是否匹配
        if re.match(patternStr, item) is not None:
            print("匹配的：" + item)
            resultList.append(os.path.join(srcDir, item))
            index = index + 1
            if index == len(tuesdayList):
                break
    print("循环次数：%d" % count)
    return resultList


def matchInYear(year):
    for month in range(1, 13):
        matchInMonth(year, month)


def main():
    copyFile(2017, 6)


if __name__ == '__main__':
    main()
