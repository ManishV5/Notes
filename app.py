
from flask import Flask, flash, render_template, request
from .helpers import lookup


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("query"):
            return render_template("index.html")
        query = request.form.get("query")
        result = lookup(query)
        return render_template("result.html", result=result)


    else:
        return render_template("index.html")
