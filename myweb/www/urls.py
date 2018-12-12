from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new/<int:post_id>', methods=['GET', 'POST'])
def new(post_id):
    form = request.form
    if not form:
        cont = db_select(form)

    print('form',form)
    if len(cont) > 20:
        page = len(cont) // 20
        if len(cont) % 20 > 0:
            page += 1
        if post_id <= page:
            a = post_id * 20
            if len(cont) - a >= 20:
                conter = cont[a - 20:a]
            else:
                conter = cont[a - 20:]
    else:
        page = 1
        conter = cont

    return render_template('shucai.html', page=page, datebase=conter)


def db_select(form):
    import sqlite3, os, datetime
    # 获取提交的表单数据！
    # form = request.form
    # 提取名称、日期
    food_name = form.get('food_name')
    start_date = form.get('start_date')
    stop_date = form.get('stop_date')
    # 如果相关项为空，则进行默认值配置！
    if food_name == '':
        pass
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
    if food_name == '':
        cur.execute('select name, lowest, average, highest, date from shucai '
                    'where date Between ? and ? ', (start_date, stop_date))
    else:
        cur.execute('select name, lowest, average, highest, date from shucai '
                    'where name=? and date Between ? and ? ', (food_name, start_date, stop_date))
    datebase = cur.fetchall()
    cur.close()
    conn.close()
    return datebase

if __name__ == "__main__":
    app.run()