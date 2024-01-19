from flask import(Blueprint, render_template, request, redirect, url_for)
from web.def_eventData import digitize_data
import web.def_DB

bp = Blueprint("login", __name__)
@bp.route("/login",methods=("GET", "POST"))
def login_form():
    error_message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data = digitize_data(username,password)
        # ログイン情報の検証（独自のプログラムによるチェック）
        if data == "失敗":
            return render_template('login.html', error_message='ログイン情報が間違っています。もう一度試してください.')

        # ログイン成功の場合、event_list()にリダイレクト
        return redirect(url_for('calender.event_calendar'))
        #return redirect(url_for('login.index'))

    return render_template('login.html', error_message=error_message)

@bp.route("/index")
def index():
    print(web.def_DB.get_data())
    #for char in data:
    #   print(f'''日時:{char["日付"]}|{char["時間"]}アーティスト名:{char["アーティスト"]}会場:{char["会場"]}業務内容:{char["業務内容"]}予約状態:{char["予約状態"]}''')