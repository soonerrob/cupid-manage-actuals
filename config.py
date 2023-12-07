import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('FLASK_ENV') == 'development'
SECRET_KEY = os.getenv("APP_SECRET_KEY")
BOOTSTRAP_BTN_STYLE = 'primary'  # default to 'secondary'

# Raw ODBC connection string
ODBC_CONNECTION_STRING = (
    "DRIVER=" + os.getenv("ODBC_CONNECTION_DRIVER") + ";"
    "SERVER=" + os.getenv("ODBC_CONNECTION_SERVER") + ";"
    "DATABASE=" + os.getenv("ODBC_CONNECTION_DATABASE") + ";"
    "UID=" + os.getenv("ODBC_CONNECTION_UID") + ";"
    "PWD=" + os.getenv("ODBC_CONNECTION_PWD")
)
