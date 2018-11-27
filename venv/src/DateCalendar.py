import calendar
import time
import datetime
import FileDealers


def getAllTuesdayInPreviousMonth():
    '''
    获得之前一个月周二的日期
    :return: 当前抓取的年份、月份、周二的日期列表
    '''
    # 获得当前本地时间
    localtime = time.localtime(time.time())
    currentYear = localtime.tm_year
    currentMonth = localtime.tm_mon
    # 获得之前月份中所有星期二的日期
    if currentMonth == 1:
        previousMonth = 12
        previousYear = currentYear - 1
    else :
        previousMonth = currentMonth - 1
        previousYear = currentYear
    return previousYear, previousMonth, getAllTuesday(previousYear, previousMonth)


def getAllTuesday(year, month):
    '''
    获得指定年、月中的所有周二日期
    :param year: 年
    :param month: 月（1-12）
    :return: 日期列表
    '''
    tuesdays = []
    for dayList in calendar.monthcalendar(year, month):
        if dayList[1] != 0:
            tuesdays.append(dayList[1])
    print(tuesdays)
    return tuesdays


def main():
    for dayList in calendar.monthcalendar(2018, 2):
        print(dayList)
    print(calendar.month(2018, 2))
    # getAllTuesday(2018, 2)
    # getAllTuesdayInPreviousMonth()


if __name__ == '__main__':
    main()
