from flask import(Blueprint, render_template, request, redirect, url_for)
from web.event_def import data_get

bp = Blueprint("login", __name__)
@bp.route("/login",methods=("GET", "POST"))
def login_form():
    error_message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ログイン情報の検証（独自のプログラムによるチェック）
        if data_get(username,password) == "失敗":
            return render_template('login.html', error_message='ログイン情報が間違っています。もう一度試してください.')

        # ログイン成功の場合、event_list()にリダイレクト
        #return redirect(url_for('event_list'))
        return render_template('login.html', error_message="エベントだお")

    return render_template('login.html', error_message=error_message)
