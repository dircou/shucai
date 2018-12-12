import sqlite3
import os
import datetime

class db_sql(object):
    def db_select(self,form):
        # 获取提交的表单数据！
        # form = request.form
        # 提取名称、日期
        food_name = form.get('food_name').strip()
        start_date = form.get('start_date').strip()
        stop_date = form.get('stop_date').strip()
        print(food_name, start_date, stop_date)
        # 如果相关项为空，则进行默认值配置！
        if food_name == '':
            pass
        if start_date == '':
            start_date = '1970-01-01'
        if stop_date == '':
            stop_date = str(datetime.datetime.now().date())

        print(food_name, start_date, stop_date)
        path = os.path.join(os.getcwd(), 'ShuCai.db')
        if os.path.isfile(path):
            print(path)
        else:
            print("无文件")
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        if food_name == '':
            cur.execute('select name, lowest, average, highest, date from shucai '
                        'where date Between ? and ? ', (start_date, stop_date))
        else:
            cur.execute('select name, lowest, average, highest, date from shucai '
                        'where name=? and date Between ? and ? ', (food_name, start_date, stop_date))
        datebase = cur.fetchall()
        cur.close()
        conn.close()
        print(datebase)
        return datebase