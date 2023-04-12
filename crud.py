"""CRUD operations"""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user"""

    user = User(email=email, password=password)

    return user

def get_users():
    """Return a list of all users in the database"""
    
    return User.query.all()

def get_user_by_id(user_id):
    """Return a user given its id"""
    
    return User.query.get(user_id)
    
def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie"""

    movie = Movie(title=title, 
                overview=overview, 
                release_date=release_date, 
                poster_path=poster_path)
    
    return movie

def get_movies():
    """Return a list of all movies in the database"""
    
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return a movie given its id"""
    
    return Movie.query.get(movie_id)
    
def create_rating(user, movie, score):
    """Create and return a new rating"""
    
    rating = Rating(user=user,
                    movie=movie,
                    score=score)

    return rating
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)