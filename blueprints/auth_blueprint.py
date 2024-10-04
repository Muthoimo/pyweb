from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash


auth_views = Blueprint("auth", __name__)


@auth_views.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    # define aplication logic for homepage.
    if request.method == "POST":
        uploaded_file = request.files["picture"]
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # save file to server
        uploaded_file.save(f"/home/kinyua/src/{uploaded_file.filename}")

        # databse to register new user.
        new_user = {
            "username": username,
            "email": email,
            "password": password,
            "profile_pic": f"/static/profile_pic/{uploaded_file.filename}",
        }

        try:
            from models.database import user

            check_email = user.find_one({"email": request.form.get("email")})
            check_username = user.find_one({"username": request.form.get("username")})

            if check_email or check_username:
                flash("Credentials Already in use!", "error")
                return redirect("/register")

            new_user = user.insert_one(new_user)
            return redirect("/login")

        except Exception as e:
            print(e)
            flash("Error occured during registration. Try again later!", "error")
            return redirect("/register")

    # When it's a GET request we sent the html form
    return render_template("register.html")


@auth_views.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")  # .

    if request.method == "POST":
        from models.database import user, User

        # Get username and password from the form
        username = request.form.get("username")
        user_password = request.form.get("password")

        # Retrieve user from the database with username
        find_user = user.find_one({"username": username})

        # Return error if user is not in the database.
        if find_user is None:
            flash("Ivalid Login Credentials", "error")
            return redirect("/register")

        # If found compare user password with the one in the database.
        is_valid_password = check_password_hash(
            find_user.get("password"), user_password
        )
        if not is_valid_password:
            flash("Invalid password for this username", "error")
            return redirect("/login")

        # This is to enable the Flask-Login Extension kick in.
        log_user = User(find_user.get("username"), str(find_user.get("_id")))

        login_user(log_user)
        # Then return the user to the index page after sucess
        return redirect("/")

    return render_template("login.html")


# Create Sign Out Route which we'll create a button for.
@auth_views.route("/logout", strict_slashes=False)
@login_required
def logout():
    # We wrap the logout function with @login_required decorator
    # So that only logged in users should be able to 'log out'.
    logout_user()
    return redirect("/")
