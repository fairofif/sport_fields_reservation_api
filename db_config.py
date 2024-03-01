from appflask import app
from flaskext.mysql import MySQL
from dotenv import load_dotenv
load_dotenv()
import os


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USER_")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASSWORD_")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME_")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST_")
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_SOCKET'] = "/tmp/mysql.sock"
mysql.init_app(app)
