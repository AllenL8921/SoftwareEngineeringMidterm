from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create blueprint
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # Compare the entered password with the saved password to the corresponding email
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("Email does not exist.", category="error")

    # You can pass variables to the html templates
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    # When user is submitting the method is POST
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        # Define errors
        elif len(email) < 4:
            flash("Email is not valid.", category="error")
        elif len(firstName) < 2:
            flash("First Name is too Short.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Passwords is too short.", category="error")
        else:
            new_user = User(
                email=email,
                firstName=firstName,
                password=generate_password_hash(password1, method="pbkdf2:sha256"),
            )

            # add user to database
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(user, remember=True)

            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/checkout")
def checkout():
    return render_template("checkout.html", user=current_user)
