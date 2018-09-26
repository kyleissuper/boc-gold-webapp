from flask import Flask, render_template, request
from gevent.pywsgi import WSGIServer
import helpers as helpers
import settings as settings


app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
db = helpers.get_data()


@app.route("/")
def home():
    data = {
        "type": None,
        "results": []
    }
    if "search" in request.args and request.args["search"] != "":
        data["type"] = "search"
        data["results"] = helpers.search_by_string(db, request.args["search"], "name")
    elif "url" in request.args and request.args["url"] != "":
        data["type"] = "url"
        data["results"] = helpers.search_by_string(db, request.args["url"], "url")
    elif "lat" in request.args:
        data["type"] = "location"
        data["results"] = helpers.search_by_location(db, float(request.args["lat"]), float(request.args["lng"]))
    return render_template("home.html", data=data)


http_server = WSGIServer(("", settings.PORT), app)
http_server.serve_forever()
