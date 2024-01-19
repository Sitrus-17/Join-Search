from flask import Flask
import web.def_DB

def custom_len(s):
    return len(s)

def create_app():
    app = Flask(__name__)

    web.def_DB.init_db()
    
    
    from . import login, calender
    app.register_blueprint(login.bp)
    app.register_blueprint(calender.bp)
    
    return app
