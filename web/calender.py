from flask import(Blueprint, render_template, request, redirect, url_for)
import datetime
import web.def_DB
import sqlite3

bp = Blueprint("calender", __name__)

@bp.route("/event-list",methods=("GET", "POST"))
def event_calendar():
    if request.method == 'POST':
        # POSTリクエストから年と月を取得
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))
        industry = None
        reservation = None

        # 'prev' または 'next' ボタンが押されたかに応じて月を更新
        if 'prev' in request.form:
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        elif 'next' in request.form:
            month += 1
            if month > 12:
                month = 1
                year += 1
        elif 'action' in request.form:
            industry = request.form.getlist('industry[]')
            reservation = request.form.getlist('reservation[]')
            print(month,year,industry,reservation)

    else:
        # GETリクエストの場合は現在の年月を使用
 
        # データベースに接続
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # 最も古い日付を取得
        c.execute("SELECT MIN(date) FROM events")
        oldest_date_str = c.fetchone()[0]

        # 日付の文字列をdatetimeオブジェクトに変換
        oldest_date = datetime.datetime.strptime(oldest_date_str, '%Y-%m-%d')

        # 年と月を抽出
        year = oldest_date.year
        month = oldest_date.month
        print(f"最も古いデータの年: {year}, 月: {month}")

        conn.close()

        industry = None
        reservation = None

    data_count_month = web.def_DB.count_events(year,month,industry,reservation)

    first_day = datetime.date(year, month, 1)
    first_noday_count = first_day.weekday() + 1

    N = 29 if month == 2 and year % 4 == 0 else 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
    last_day = datetime.date(year, month, N)
    last_noday_count = 6 if last_day.weekday() == 6 else 5 - last_day.weekday()
    
    data_count_month.insert(0,first_noday_count)
    data_count_month.append(last_noday_count)

    return render_template('calendar.html', data=data_count_month, year=year, month=month, industry=industry, reservation=reservation)

@bp.route("/event_list/<int:year>/<int:month>/<int:day>")
def show_event(year,month,day):
    industry = request.args.getlist('industry')
    reservation = request.args.getlist('reservation')
    data = web.def_DB.get_data(year, month, day, industry, reservation)
    print(f"データ{data}")
    return render_template('show_event.html', data=data)

