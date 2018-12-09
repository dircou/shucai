import sqlite3,os,sys
from datetime import date as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyecharts import Bar

# class MyClass(object):
#
#     def __init__(self):
#         self.db_file = 'E:\\dircou\\python\\ShuCai\\ShuCai.db'
#         if os.path.isfile(self.db_file):
#             self.conn = None
#             self.cur = None
#         else:
#             print("目标数据库不存在！")
#             return
#         print(self.conn,self.cur)
#
#     def ConnDb(self):
#         self.conn = sqlite3.connect(self.db_file)
#         self.cur = self.conn.cursor()
#         print("连接数据库成功！")
#
#     def CloseDb(self):
#         self.cur.close()
#         self.conn.close()
#         print("关闭数据库成功！")
#
#     def SelectDb(self,name='',start='2018-01-01',stop=''):
#         # info为要查询的条件，共有name date ,其中date分StartDate与StopDate;
#         # 默认设置：
#         db_file = 'E:\\dircou\\python\\ShuCai\\ShuCai.db'
#         if os.path.isfile(db_file):
#             conn = sqlite3.connect(db_file)
#             cur = conn.cursor()
#         else:
#             print("目标数据库不存在！")
#             return
#
#         if stop == '':
#             stop = dt.now().date()
#         if name == '':
#             cur.execute('select name, lowest, average, highest, date from shucai'
#                         ' where date Between ? and ? ', (start, stop))
#         else:
#             cur.execute('select name, lowest, average, highest, date from shucai'
#                         ' where name=? and date Between ? and ? ', (name, start, stop))
#         datebase = cur.fetchall()
#         cur.close()
#         conn.close()
#         return datebase

def SelectDb(name='',start='2018-01-01',stop=''):
    # info为要查询的条件，共有name date ,其中date分StartDate与StopDate;
    # 连接数据库
    db_file = 'E:\\dircou\\python\\ShuCai\\ShuCai.db'
    if os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
    else:
        print("目标数据库不存在！")
        return

    # 默认设置：
    if stop == '':
        stop = dt.today()
    if name == '':
        cur.execute('select name, lowest, average, highest, date from shucai'
                    ' where date Between ? and ? ', (start, stop))
    else:
        cur.execute('select name, lowest, average, highest, date from shucai'
                    ' where name=? and date Between ? and ? ', (name, start, stop))
    datebase = cur.fetchall()
    cur.close()
    conn.close()
    return datebase


# 查询一个月的　香菜　价格
datebase = SelectDb('香菜','2017-11-01','2017-11-30')
if datebase == None:
    print("查询失败！")
    sys.exit()
    # try:
    #     sys.exit()
    # except:
    #     print(123456)

print("合计：{} 条".format(len(datebase)))
# 配套使用sorted AND lambda进行数据嵌套排序！
# https://www.polarxiong.com/archives/Python-%E4%BD%BF%E7%94%A8lambda%E5%BA%94%E5%AF%B9%E5%90%84%E7%A7%8D%E5%A4
# %8D%E6%9D%82%E6%83%85%E5%86%B5%E7%9A%84%E6%8E%92%E5%BA%8F-%E5%8C%85%E6%8B%AClist%E5%B5%8C%E5%A5%97dict.html
datebase = sorted(datebase, key=lambda k:k[4])
print(datebase)
date,low,average,highest = [],[],[],[]
for i in datebase:
    low.append(i[1])
    average.append(i[2])
    highest.append(i[3])
    date.append(i[4][8:]) #切片，只取 日

# attr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
# v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
bar = Bar("折线表", "precipitation and evaporation one year")
bar.add("最低价", date, low, mark_line=["average"], mark_point=["max", "min"])
bar.add("均价", date, average, mark_line=["average"], mark_point=["max", "min"])
bar.add("最高价", date, highest, mark_line=["average"], mark_point=["max", "min"])
bar.render()
print(os.getcwd())
# print(len(attr),len(v1),len(v2))


# 图表形式开始！
# plt.rcParams['savefig.dpi'] = 200 #图片像素
# plt.rcParams['figure.dpi'] = 300 #分辨率
# zhfont = mpl.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\msyh.ttf') # 设置中文字体
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.set_xticklabels(date,rotation=45) # 设置刻度文字倾斜
# fig.suptitle('香菜\n2018-11-01 2018-11-30', fontsize = 14, fontweight='bold',fontproperties=zhfont)
# # fig.suptitle('figure title demo', fontsize = 14, fontweight='bold')
# plt.ylabel("价格",fontproperties=zhfont)
# plt.xlabel("日期",fontproperties=zhfont)
# plt.ylim(0.5,1.6)
# plt.plot(date,low,label='low')
# plt.plot(date,average,label='average')
# plt.plot(date,highest,label='hightest')
#
# plt.legend() # 显示标注
# plt.grid() # 显示网格
# plt.show()
#直接保存为文件，可不要上面的plt.show()
# plt.savefig("D:\\text.png")