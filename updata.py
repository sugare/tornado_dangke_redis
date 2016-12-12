#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-12-1 下午7:07
# @Author  : sugare
# @Site    : 
# @File    : updata.py
# @Software: PyCharm
import os
import redis
import xlrd
import xlwt

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

def upUsers(r):         # 上传用户
    data = xlrd.open_workbook(r'static/data/users.xls')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in (range(1, nrows + 1)):
        r.hset(int(table.row_values(i - 1)[0]), 'user', table.row_values(i - 1)[2])
        r.hset(int(table.row_values(i - 1)[0]), 'single', 0)
        r.hset(int(table.row_values(i - 1)[0]), 'multi', 0)
        r.hset(int(table.row_values(i - 1)[0]), 'judge', 0)
        r.hset(int(table.row_values(i - 1)[0]), 'total', 0)


def upQuestionChoice(r):
    data = xlrd.open_workbook(r'static/data/question.xlsx')
    table = data.sheet_by_index(0)
    # nrows = table.nrows
    for i in range(1,151):
        if i < 61:
            r.hset('s'+ str(i), 'q', table.row_values(i-1)[0])
            r.hset('s'+ str(i), 'A', table.row_values(i-1)[1])
            r.hset('s'+ str(i), 'B', table.row_values(i-1)[2])
            r.hset('s'+ str(i), 'C', table.row_values(i-1)[3])
            r.hset('s'+ str(i), 'D', table.row_values(i-1)[4])
            r.hset('s'+ str(i), 'AN', table.row_values(i-1)[5])

        elif i > 120:
            r.hset('j' + str(i - 120), 'q', table.row_values(i - 1)[0])
            r.hset('j' + str(i - 120), 'AN', table.row_values(i - 1)[5])

        else:
            r.hset('m'+ str(i-60), 'q', table.row_values(i-1)[0])
            r.hset('m'+ str(i-60), 'A', table.row_values(i-1)[1])
            r.hset('m'+ str(i-60), 'B', table.row_values(i-1)[2])
            r.hset('m'+ str(i-60), 'C', table.row_values(i-1)[3])
            r.hset('m'+ str(i-60), 'D', table.row_values(i-1)[4])
            r.hset('m'+ str(i-60), 'AN', table.row_values(i-1)[5])


def upSurvey(r):
    data = xlrd.open_workbook(r'static/data/fujia.xls')
    table = data.sheet_by_index(0)
    for i in range(6, 11):
        r.hset('i' + str(i-5), 'q', table.row_values(i - 1)[1])
        r.hset('i' + str(i-5), 'A', 0)
        r.hset('i' + str(i-5), 'B', 0)
        r.hset('i' + str(i-5), 'C', 0)
        r.hset('i' + str(i-5), 'D', 0)
        r.hset('i' + str(i-5), 'E', 0)


def downloadMask(r):     # 下载成绩单
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('results', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('investigation', cell_overwrite_ok=True)
    sheet2.write(0, 0, u'问题\选项')
    sheet2.write(0, 1, u'A.非常满意')
    sheet2.write(0, 2, u'B.满意')
    sheet2.write(0, 3, u'C.比较满意')
    sheet2.write(0, 4, u'D.一般')
    sheet2.write(0, 5, u'E.不满意')

    for i in range(1, 6):
        a = r.hgetall('i'+str(i))
        sheet2.write(i, 0, a['q'].decode('utf8'))
        sheet2.write(i, 1, a['A'])
        sheet2.write(i, 2, a['B'])
        sheet2.write(i, 3, a['C'])
        sheet2.write(i, 4, a['D'])
        sheet2.write(i, 5, a['E'])

    sheet1.write(0, 0, u'考号')
    sheet1.write(0, 1, u'姓名')
    sheet1.write(0, 2, u'单选')
    sheet1.write(0, 3, u'多选')
    sheet1.write(0, 4, u'判断')
    sheet1.write(0, 5, u'总分')
    sc = r.keys(pattern='2*')
    n = 0

    for i in sc:
        n += 1
        sheet1.write(n, 0, i)
        sheet1.write(n, 1, r.hget(i, 'user').decode('utf8'))
        sheet1.write(n, 2, r.hget(i, 'single'))
        sheet1.write(n, 3, r.hget(i, 'multi'))
        sheet1.write(n, 4, r.hget(i, 'judge'))
        sheet1.write(n, 5, r.hget(i, 'total'))
    workbook.save(r'%s/static/data/mask1.xls' % (os.path.dirname(__file__)))


if __name__ == '__main__':
    upUsers(r)
    upSurvey(r)
    upQuestionChoice(r)
