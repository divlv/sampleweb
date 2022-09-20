from flask import render_template, make_response, abort, Response
import time
import datetime
import re
import ssl
from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Resource, Api, fields

PATH_TO_TEMPLATES = "./tpl/"

app = Flask(__name__, template_folder=PATH_TO_TEMPLATES)


# api = Api(
#     app,
#     version="1.0",
#     title="Sample web REST service",
#     doc="/api/",
#     description="Access to the stored data, if any.",
#     default="Services",
#     default_label="All available services list:",
# )


# class HealthCheck(Resource):
#     def get(self):
#         """
#         REST Service health check
#         """
#         return {
#             "status": "Sample REST service is up",
#             "build": "Build number here",
#             "serverTime": str(datetime.datetime.now()),
#             "tag": "#GTO",
#         }


# api.add_resource(HealthCheck, "/health")


# class HomePage(Resource):
#     def get(self):
#         headers = {"Content-Type": "text/html"}
#         print("home page!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         return make_response(
#             render_template("layout.html", bodyhtml="main"), 200, headers
#         )


# api.add_resource(HomePage, "/")


@app.context_processor
def year_for_templates():
    return {"this_year": datetime.datetime.now().year}


@app.route("/")
def home_page():
    return render_template("layout.html", bodyhtml="main")


# <Error pages>
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500


# </Error pages>


# Uncomment this line, if running in Development environment
# i.e. not with Gunicorn
app.run(host="0.0.0.0", port="80", threaded=True)
