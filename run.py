from flask import Flask,render_template,request,session,redirect,url_for
from backend.models import db

app = None

def setup_app():
    app = Flask(__name__)
    app.secret_key = "Jai_Baba_Ki_Maahal" 
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quiz.sqlite3" #having all database 
    db.init_app(app)   #flask connected to db
    app.app_context().push()#direct access
    app.debug=True
    print("xyz")
    

#call the app
setup_app()

from backend.controllers import *

if __name__=="__main__":
    app.run()