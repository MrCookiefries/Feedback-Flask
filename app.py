from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "AGkajgea9i3kjaj45KDjskg"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """registers a user"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.register(data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username/email already taken.")
            return render_template(
                "register.html",
                form=form,
                submit="Register"
            )
        flash("User successfully created.")
        session["username"] = user.username
        return redirect(f"/users/{user.username}")
    return render_template(
        "register.html",
        form=form,
        submit="Register"
    )

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """logs in a user"""
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash("Logged in successfully.")
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        form.username.errors.append("Incorrect username/password.")
    return render_template(
        "login.html",
        form=form,
        submit="Login"
    )

@app.route("/logout")
def logout_user():
    """logs out a user"""
    if "username" not in session:
        flash("You're not logged in yet.")
        return redirect("/login")
    flash("Logged out successfully.")
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>")
def user_info(username):
    """shows details about a user"""
    if "username" not in session or username != session["username"]:
        flash(f"You have to be logged in as {username} to view this information.")
        return redirect("/")
    user = User.query.get_or_404(username)
    return render_template(
        "user.html",
        user=user,
        all_feedback=user.feedback
    )

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """deletes a user's account"""
    if "username" not in session or username != session["username"]:
        flash(f"You have to be logged in as {username} to delete their account.")
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    flash("Successfully deleted your account.")
    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def user_add_feedback(username):
    """adds feedback for a user"""
    if "username" not in session or username != session["username"]:
        flash(f"You have to be logged in as {username} to add feedback as them.")
        return redirect("/")
    user = User.query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        data["username"] = user.username
        feedback = Feedback(**data)
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback successfully created.")
        return redirect(f"/users/{username}")
    return render_template(
        "add-feedback.html",
        form=form,
        submit="Add Feedback"
    )

@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def user_update_feedback(id):
    """updates the user feedback"""
    feedback = Feedback.query.get_or_404(id)
    if "username" not in session or feedback.username != session["username"]:
        flash(f"You have to be logged in as {feedback.username} to edit feedback as them.")
        return redirect("/")
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash("Feedback successfully updated.")
        return redirect(f"/users/{feedback.username}")
    return render_template(
        "update-feedback.html",
        form=form,
        submit="Save"
    )

@app.route("/feedback/<int:id>/delete", methods=["POST"])
def user_delete_feedback(id):
    """deletes a user's feedback"""
    feedback = Feedback.query.get_or_404(id)
    if "username" not in session or feedback.username != session["username"]:
        flash(f"You have to be logged in as {feedback.username} to delete their feedback.")
        return redirect("/")
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback deleted successfully.")
    return redirect(f"/users/{feedback.username}")

