"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):

        return '<User id={}>'.format(self.user_id)


# Put your Movie and Rating model classes here.

class Movie(db.Model):
    """Movie in ratings website."""

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):

        return '<Movie id={} title={}>'.format(self.movie_id, self.title)
    

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(30))

    movies = db.relationship('Movie', secondary='movie_categories',
                                backref='categories')

    def __repr__(self):

        return '<Category: {}>'.format(self.category)

class MovieCategory(db.Model):

    __tablename__ = 'movie_categories'

    movie_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, 
                            db.ForeignKey('categories.id'),
                            nullable=False)
    movie_id = db.Column(db.Integer, 
                            db.ForeignKey('movies.movie_id'),
                            nullable=False)


class Rating(db.Model):

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, nullable=False)

    movie = db.relationship('Movie', backref=db.backref('ratings',
                                    order_by=rating_id))

    user = db.relationship('User', backref=db.backref('ratings',
                                    order_by=rating_id))

    def __repr__(self):

        return '<Rating rating_id={} movie_id={} user_id={} score={}>'.format(
                        self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratingsfall16'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
