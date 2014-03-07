from flask import Flask, render_template, redirect, request, flash, url_for, session
import model
#from urlparse import urlparse

app = Flask(__name__)
app.secret_key = "thisispainful"

@app.route("/")
def index():
    # if session.get("email"):
    #     return redirect(url_for("main_menu"))
    # else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    emailform = request.form.get("email")
    passwordform = request.form.get("password")

    email = model.authenticate(emailform, hash(passwordform))
    if email != None:
        flash("User authenticated!")
        session['email'] = email
    else:
        flash("Password incorrect, please try again.")
    return redirect(url_for("main_menu"))

@app.route("/main_menu")
def main_menu():
    return render_template("main_menu.html")

@app.route("/register")
def register():
    return render_template("register.html")
    
@app.route("/register", methods=["POST"])
def registerUser():
    emailform = request.form.get("email")
    passwordform = request.form.get("password")
    ageform = request.form.get("age")
    zipcodeform = request.form.get("zipcode")
    model.register_user(emailform,passwordform,ageform,zipcodeform)
    return redirect(url_for("index"))

@app.route("/clear_session")
def session_clear():
    session.clear()
    return redirect(url_for("index"))


@app.route("/users")
def list_users():
    user_list = model.session.query(model.User).all()
    return render_template("user_list.html", user_list=user_list)

if __name__ == "__main__":
    app.run(debug = True)