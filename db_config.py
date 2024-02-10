from appflask import app
from flaskext.mysql import MySQL
from dotenv import load_dotenv
load_dotenv()
import os


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST")
mysql.init_app(app)