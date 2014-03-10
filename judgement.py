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

@app.route("/user_list")
def list_users():
    user_list = model.session.query(model.User).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/movie_list")
def list_movies():
    movie_list = model.session.query(model.Movies).all()
    return render_template("movie_list.html", movie_list=movie_list)


@app.route("/users/<userid>")
def user_details(userid):
    movie_ratings = model.getUserMovieRatings(userid)
    return render_template("user_profile.html", userid=userid, movie_ratings=movie_ratings)

@app.route("/movies/<movieid>")
def movie_details(movieid):
    author_id = session.get("email")
    print author_id
    movie_ratings = model.getRatingsForMovie(movieid)
    return render_template("movie_profile.html", movieid=movieid, movie_ratings=movie_ratings, author_id=author_id)  

@app.route("/movies/<movieid>", methods=['POST'])
def movie_details_rate(movieid):
    author_id = session.get("email")
    userid = model.getUserID(author_id)
    rating = request.form.get("rating")
    model.addEditRating(userid, movieid,rating)
#    return redirect("/movies/<movieid>")
#    return redirect(url_for("movie_details"), movieid=movieid)
#    return render_template("movie_profile.html", movieid=movieid)
    return redirect(url_for("main_menu"))

if __name__ == "__main__":
    app.run(debug = True)