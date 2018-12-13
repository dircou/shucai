from flask import Flask, request, render_template, redirect, url_for
import sqlite3, os, datetime
from pyecharts import Line, Bar, Page
# https://pyecharts.readthedocs.io/en/latest/zh-cn/API%E7%AF%87/

app = Flask(__name__)
cont = None
dname = None
lst = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new/')
def new1():
    global cont
    today = datetime.date.today().replace(day=1)
    food_name = ''
    start_date = today
    stop_date = ''
    cont = db_select(food_name, start_date, stop_date)
    page, count, content = page_effect(cont, 1)
    return render_template('shucai.html', page=page, datebase=content, count=count)

@app.route('/new/<int:post_id>', methods=['GET', 'POST'])
def new(post_id):
    global cont
    form = request.form
    if len(form) != 0:
        food_name = form.get('food_name')
        start_date = form.get('start_date')
        stop_date = form.get('stop_date')
        cont = db_select(food_name,start_date,stop_date)
        page, count, content = page_effect(cont, post_id)
        print(cont)
    elif cont:
        page, count, content = page_effect(cont,post_id)
    else:
        page=None
        content=None
        count = None
    return render_template('shucai.html', page=page, datebase=content, count=count)

@app.route('/legend')
def legend(title,lst):
    line = Line(title)
    name,low,age,hight,date = [],[],[],[],[]
    if len(lst) <= 2:
        pass
    elif dname == "所有菜类":# 判断是否是同一类型！
        for i in lst:
            name.append(i[0])
            age.append(i[2])
            date.append(i[4])

    else:
        for i in lst:
            low.append(i[1])
            age.append(i[2])
            hight.append(i[3])
            date.append(i[4])
        line.add('最低价', date, low)
        line.add('平均价',date, age)
        line.add('最高价', date, hight)
        line.render()

def db_select(food_name,start_date,stop_date):
    # 获取提交的表单数据！
    # form = request.form
    global dname, lst

    # 如果相关项为空，则进行默认值配置！
    if food_name == '':
        dname = "所有菜类"
    else:
        dname = food_name
    if start_date == '':
        start_date = '1970-01-01'
    if stop_date == '':
        stop_date = str(datetime.datetime.now().date())

    path = os.path.join(os.getcwd(), 'ShuCai.db')
    if os.path.isfile(path):
        print(path)
    else:
        print("无文件")
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    # Between按日期段时间搜索　order by按日期进行排序　desc为降序,默认升序！
    if food_name == '':
        cur.execute('select name, lowest, average, highest, date from shucai '
                    'where date Between ? and ? order by date desc;', (start_date, stop_date))
    else:
        cur.execute('select name, lowest, average, highest, date from shucai '
                    'where name=? and date Between ? and ? order by date desc;', (food_name, start_date, stop_date))
    datebase = cur.fetchall()
    cur.close()
    conn.close()
    lst = datebase

    return datebase

def page_effect(datebase,page_id):
    # datebase:记录总数 page_id:当前第几页！
    count = len(datebase)
    if count > 20:# 判断总记录数是否大于每页显示的数量！
        page = count // 20
        if count % 20 > 0:# 获取总页数
            page += 1
        if page_id <= page:
            a = page_id * 20
            if count - a >= 20:
                content = datebase[a - 20:a]
            else:
                content = datebase[a - 20:]
    else:
        page = None
        content = datebase
    return page, count, content

if __name__ == "__main__":
    app.run(debug=True)