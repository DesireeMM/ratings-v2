"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#create a user class
class User(db.Model):
    """User on our movie ratings app"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="user")

    @classmethod
    def create(cls, email, password):
        """Create and return a new user"""

        return cls(email=email, password=password)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
#create a movie class
class Movie(db.Model):
    """Movie on our movie ratings app"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="movie")

    @classmethod
    def create(cls, title, overview, release_date, poster_path):
        """Create and return a new movie"""

        return cls(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    def __repr__(self):
        return f'<Movie movie_id={self.movie_id} title={self.title}>'
    
#create a rating class
class Rating(db.Model):
    """Rating on our movie ratings app"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    movie = db.relationship("Movie", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    @classmethod
    def create(cls, user, movie, score):
        """Create and return a new rating"""

        return cls(user=user, movie=movie, score=score)

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
