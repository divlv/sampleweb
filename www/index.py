import os
import datetime
from flask import url_for
from flask import Blueprint, render_template
from flask import Flask
from flask_cors import CORS
from flask_restplus import Resource, Api, fields

PATH_TO_TEMPLATES = "./tpl/"

app = Flask(__name__)


# Default web page Blueprint START #############################################

default_web = Blueprint(
    "default_web", __name__, url_prefix="", template_folder=PATH_TO_TEMPLATES
)


@default_web.context_processor
def year_for_templates():
    return {"this_year": datetime.datetime.now().year}


@default_web.route("/")
def home_page():
    return render_template("layout.html", bodyhtml="main")


# <Error pages>
@default_web.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@default_web.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500


app.register_blueprint(default_web)
# Default web page Blueprint FINISH #############################################


# REST API Blueprint START ######################################################
swagger = Blueprint("swagger", __name__, url_prefix="/api")

# Sometimes we need to build HTTPS url for swagger documentation (e.g. in managed environments like Azure Application Service)
# In this case we need to check any environment variables from this environment (e.g. WEBSITE_HOSTNAME for Azure)
# if so - we need to [auto]build HTTPS url:
if os.environ.get("WEBSITE_RESOURCE_GROUP"):

    @property
    def specs_url(self):
        return url_for(self.endpoint("specs"), _external=True, _scheme="https")

    Api.specs_url = specs_url


api = Api(
    swagger,
    version="1.0",
    title="Sample web REST service",
    description="Access to the stored data, if any.",
    default="Services",
    default_label="All available services list:",
)


class HealthCheck(Resource):
    def get(self):
        """
        REST Service health check
        """
        return {
            "status": "Sample REST service is up",
            "build": "Build number here",
            "serverTime": str(datetime.datetime.now()),
            "tag": "#GTO",
        }


api.add_resource(HealthCheck, "/health")

app.register_blueprint(swagger)
# REST API Blueprint FINISH ######################################################


# Uncomment this line, if running in Development environment
# i.e. not with Gunicorn
# (For this demo-project - using the Development server)
#
# Despite the fact that we may be in a managed environment (e.g. Azure App Service) with HTTPS by default,
# leave the port as 80 here:
app.run(host="0.0.0.0", port="80", threaded=True)
