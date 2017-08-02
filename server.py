"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/register')
def display_registration_form():
    """ User registration form. """

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def process_registration_form():
    """ Process registration form. """

    user_email = request.form.get("email")
    user_password = request.form.get("password")

    # Cross match user email with existing emails in User table DB
    # Check if email in DB. If not, add email to DB. Either way, redirects to homepage.
    if User.query.filter_by(email=user_email).first():
        print "email exists!"  # SHOW IN TERMINAL IF EMAIL EXISTS
        return redirect('/')
    else:
        sql = """ INSERT INTO users (email, password) VALUES (:email, :password) """
        db.session.execute(sql, {'email': user_email, 'password': user_password})
        db.session.commit()
        return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
