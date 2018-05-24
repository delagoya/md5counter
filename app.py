from chalice import Chalice, Response
import boto3
import os
from chalicelib import db
app = Chalice(app_name='md5counter')

_DB = None
def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DDBMd5Counter(
            boto3.resource('dynamodb').Table(os.environ['APP_TABLE_NAME'])
        )
    return _DB

@app.route('/')
def index():
    success = get_app_db().get_success()
    error = get_app_db().get_error()
    return {"success": success, "error": error}

@app.route("/success")
def success():
    # increment success counter
    r = get_app_db().incr_success()
    return {"success": r}

@app.route("/error")
def error():
    # increment error counter
    return {"error": get_app_db().incr_error()}

@app.route("/reset")
def reset():
    get_app_db().reset_counters()
    return index()
