from flask import Flask, render_template, request
from gevent.pywsgi import WSGIServer
import settings as settings


app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


@app.route("/")
def home():
    data = {
        "type": None,
        "results": []
    }
    if "url" in request.args and request.args["url"] != "":
        data["type"] = "url"
    elif "longitude" in request.args:
        data["type"] = "location"
    return render_template("home.html", data=data)


http_server = WSGIServer(("", settings.PORT), app)
http_server.serve_forever()
