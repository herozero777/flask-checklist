import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def validate(form_var, msg="person"):
    valid = True
    message = ""
    if form_var == "":
        valid = False
        message += "Error!, Enter the name of the " + msg
    elif form_var is not None and not form_var.isalpha():
        valid = False
        message += "Error!, Please use only alphabets for the name"

    if valid:
        message = "Success!"

    return valid, message


@app.route("/", methods=["GET", "POST"])
def index():
    valid = True
    message = ""
    if request.method == "POST":
        # Validate & Handling the input form
        add_given_treat_ppl = request.form.get("add_given_treat_ppl")
        valid, message = validate(add_given_treat_ppl, "people who have given treat")

        add_pending_treat_ppl = request.form.get("add_pending_treat_ppl")
        valid, message = validate(add_pending_treat_ppl, "people who've to give treat")

        rm_given_treat_ppl = request.form.get("rm_given_treat_ppl")
        valid, message = validate(rm_given_treat_ppl, "people who have given treat")

        rm_pending_treat_ppl = request.form.get("rm_pending_treat_ppl")
        valid, message = validate(rm_pending_treat_ppl, "people who've to give treat")

        # Check if there is a need to add or remove data from the database
        if valid:
            if add_given_treat_ppl:
                db.execute("INSERT INTO treat_given_ppl (person) VALUES (:name)",
                    {"name": add_given_treat_ppl})
            elif add_pending_treat_ppl:
                db.execute("INSERT INTO treat_pending_ppl (person) VALUES (:name)",
                    {"name": add_pending_treat_ppl})
            elif rm_given_treat_ppl:
                db.execute("DELETE FROM treat_given_ppl WHERE person = (:name)",
                    {"name": rm_given_treat_ppl})
            elif rm_pending_treat_ppl:
                db.execute("DELETE FROM treat_pending_ppl WHERE person = (:name)",
                    {"name": rm_pending_treat_ppl})
            else:
                message = "Some unknown error occurred in the valid if statement."
            db.commit()

    # Get data from database of the current people
    treat_given_ppl = db.execute("SELECT * FROM treat_given_ppl").fetchall()

    treat_pending_ppl = db.execute("SELECT * FROM treat_pending_ppl").fetchall()

    return render_template("index.html", treat_given_ppl=treat_given_ppl, treat_pending_ppl=treat_pending_ppl,
                           message=message)


# @app.route("/")
# def index():
#     flights = db.execute("SELECT * FROM flights").fetchall()
#     return render_template("index.html", flights=flights)
#
# @app.route("/book", methods=["POST"])
# def book():
#     """Book a flight."""
#
#     # Get form information.
#     name = request.form.get("name")
#     try:
#         flight_id = int(request.form.get("flight_id"))
#     except ValueError:
#         return render_template("error.html", message="Invalid flight number.")
#
#     # Make sure flight exists.
#     if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
#         return render_template("error.html", message="No such flight with that id.")
#     db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
#             {"name": name, "flight_id": flight_id})
#     db.commit()
#     return render_template("success.html")
#
# @app.route("/flights")
# def flights():
#     """Lists all flights."""
#     flights = db.execute("SELECT * FROM flights").fetchall()
#     return render_template("flights.html", flights=flights)
#
# @app.route("/flights/<int:flight_id>")
# def flight(flight_id):
#     """Lists details about a single flight."""
#
#     # Make sure flight exists.
#     flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
#     if flight is None:
#         return render_template("error.html", message="No such flight.")
#
#     # Get all passengers.
#     passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
#                             {"flight_id": flight_id}).fetchall()
#     return render_template("flight.html", flight=flight, passengers=passengers)