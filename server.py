"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/login', methods=["POST"])
def page_login():
    """Handle user login"""
    user_email = request.form.get("email")
    user_password = request.form.get("password")

    user = crud.get_user_by_email(user_email)
    if user.password == user_password:
        session["user_id"] = user.user_id
        session["logged_in_email"] = user.email
        flash(f"Logged in {user.email}!")
    else:
        flash("Password incorrect. Try again.")
    
    return redirect("/")

@app.route('/movies')
def view_movies():
    """View all movies"""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def view_users():
    """View all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route("/users", methods=["POST"])
def create_new_account():
    """Create a new user account"""
    user_email = request.form.get("email")
    user_password = request.form.get("password")

    if crud.get_user_by_email(user_email):
        flash("Email already taken. Please try again.")
        
    else:
        new_user = User.create(user_email, user_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully. Please log in.")

    return redirect("/")

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details on a particular user"""

    user = crud.get_user_by_id(user_id)
   


    return render_template('user_details.html', user=user)

@app.route('/update-ratings', methods=["POST"])
def update_rating():
    """Update a user's rating for a particular movie"""

    rating_id = request.json["rating_id"]
    new_score = request.json["new_score"]

    crud.update_rating(rating_id, new_score)

    return {
        "success": True,
        "status": f"You have changed the rating to {new_score}."
    }

    # user_id = request.form.get("user_id")
    # rating_id = request.form.get("movie")
    # new_score = request.form.get("new-score")

    # crud.update_rating(rating_id, new_score)

    # return redirect(f'/users/{user_id}')

@app.route('/movies/<movie_id>/ratings', methods=["POST"])
def add_rating(movie_id):
    """Add a user's movie rating to the database"""

    logged_in_email = session.get("logged_in_email")

    user = crud.get_user_by_id(session.get("user_id"))
    movie = crud.get_movie_by_id(movie_id)
    score = int(request.form.get("rating"))

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not score:
        flash("Error: you didn't enter a score for your rating.")
    elif score not in range(1, 6):
        flash("Error: invalid rating. Please choose between 1 and 5.")
    else:
        rating = crud.create_rating(user, movie, score)
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {score} out of 5.")

    return redirect(f"/movies/{movie_id}")

@app.route('/logout')
def logout():
    """Log out."""
    user = session.get("logged_in_email")
    session.clear()
    flash(f"Logged out {user}.")

    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
