from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
    jsonify,
)
from flask_caching import Cache
from functools import wraps
from App.forms.register_form import RegistrationForm
from App.forms.login_form import LoginForm
from App.handlers.register.register_handler import RegisterHandler
from App.handlers.login.login_handler import LoginHandler
from App.handlers.stats_aggregator.stats_aggregator import StatsPolygonAggregator
from App.database_py_files.db_connector import DBConnector
from App.database_py_files.sql_file_reader_runtime import SqlFileRuntimeReader
from App.conf_file_reader.conf_json_reader import ConfJsonReader
from App.database_py_files.db_connection_manager import DBConnectionManager

# todo documentation
# todo add readme and tests

conf_json_reader = ConfJsonReader("/myApp/App/config_files/flask_config.json")
flask_config = conf_json_reader.get_config("config")
app = Flask(__name__)
app.config.from_mapping(flask_config)
cache = Cache(app)
conf_json_reader = ConfJsonReader("/myApp/App/config_files/db_credentials_config.json")
db_connector = DBConnector(conf_json_reader, DBConnectionManager)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm(request.form)
    db_connection = None

    try:
        db_connection = db_connector.connect()
        if request.method == "POST" and form.validate():
            RegisterHandler(form, db_connection.get_cursor()).register_user()
            flash("Thanks for registering!", "success")
            return redirect(url_for("index"))
        return render_template("register.html", form=form)

    except:
        flash("ERROR!".format(form.email.data), "danger")
        return render_template("register.html", form=form)

    finally:
        db_connection.close_connection()


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm(request.form)
    db_connection = None

    try:
        db_connection = db_connector.connect()

        if request.method == "POST" and form.validate():

            login_handler = LoginHandler(db_connection.get_cursor())
            logged_in = login_handler.login()
            if logged_in:
                session["logged_in"] = True
                flash("You are now logged in", "success")
                return redirect(url_for("index"))

            else:
                flash("Wrong email/password", "danger")
                return render_template("login.html"), 401

        return render_template("login.html")

    except:
        flash("ERROR!".format(form.email.data), "danger")
        return render_template("login.html", form=form), 401

    finally:
        db_connection.close_connection()


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["logged_in"]:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", "danger")
            return redirect(url_for("login"))

    return wrap


@app.route("/logout/")
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("index"))


@app.route("/postal_codes/")
@cache.cached()
@is_logged_in
def collect_features():
    db_connection = None

    try:
        db_connection = db_connector.connect()

        sql_file_reader = SqlFileRuntimeReader()
        (
            get_geojson_collected_polygon_query,
            get_aggregated_turnover_all_polygons_query,
        ) = sql_file_reader.read_select_collected_geom_queries()

        stats_polygon_aggregator = StatsPolygonAggregator(
            db_connection.get_cursor(),
            get_geojson_collected_polygon_query,
            get_aggregated_turnover_all_polygons_query,
        )
        geojson = stats_polygon_aggregator.get_geojson_aggregated_stats()
        if geojson:
            return jsonify(geojson)
        return render_template("404.html"), 404

    finally:
        db_connection.close_connection()

@app.route("/postal_codes/<string:postal_code>")
@is_logged_in
def get_postal_code_stats(postal_code):

    db_connection = None

    try:
        db_connection = db_connector.connect()
        sql_file_reader = SqlFileRuntimeReader()
        (
            get_geojson_single_polygon_query,
            get_aggregated_turnover_single_polygon_query,
        ) = sql_file_reader.read_select_single_geom_queries()

        stats_polygon_aggregator = StatsPolygonAggregator(
            db_connection.get_cursor(),
            get_geojson_single_polygon_query,
            get_aggregated_turnover_single_polygon_query,
            postal_code,
        )
        geojson = stats_polygon_aggregator.get_geojson_aggregated_stats()
        if geojson:
            return jsonify(geojson)
        return render_template("404.html"), 404

    finally:
        db_connection.close_connection()




if __name__ == "__main__":
    app.run()
