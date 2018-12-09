from flask import Flask, render_template,request
from models import User
import sqlite3, os
import datetime

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/style')
def style_css():
    return render_template("style.css")

@app.route('/user')
def reque_user(user_id):
    User = None
    if int(user_id) == 1:
        User = (1,"时间苦短，我用Python")
    return render_template('reque_user.html', User, title="Dircou Python")

@app.route('/shucai')
def get_shucai():
    return render_template('shucai.html')

@app.route('/date', methods=['POST'])
def post_date():
    form = request.form
    print(form)
    food_name = form.get('food_name').strip()
    # food_name = food_name.strip()
    print(type(food_name),type(form.get('food_name')),len(food_name))
    start_date = form.get('start_date').strip()
    stop_date = form.get('stop_date').strip()
    print(food_name,start_date,stop_date)
    if food_name == '':
        pass
    if start_date == '':
        start_date = '1970-01-01'
    if stop_date == '':
        stop_date = str(datetime.datetime.now().date())

    print(food_name,start_date,stop_date)
    path = os.path.join(os.getcwd(),'ShuCai.db')
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
    return render_template('shucai.html', datebase=datebase)

@app.route('/render')
def get_zst():
    return render_template('render.html')

if __name__ == "__main__":
    app.run()