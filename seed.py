"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Rating, Movie, Category, MovieCategory
from datetime import datetime

from model import connect_to_db, db
from server import app

MOVIE_CATEGORIES = {5: 1,
                    6: 2,
                    7: 3,
                    8: 4,
                    9: 5,
                    10: 6,
                    11: 7,
                    12: 8,
                    13: 9,
                    14: 10,
                    15: 11,
                    16: 12,
                    17: 13,
                    18: 14,
                    19: 15,
                    20: 16,
                    21: 17,
                    22: 18, 
                    23: 19
                    }


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def create_categories():
    """Create movie categories table"""

    print "Categories"
    Category.query.delete()

    categories = ['Unknown', 'Action', 'Adventure', 'Animation', 'Children',
                    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                    'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance',
                    'Sci-Fi', 'Thriller', 'War', 'Western'
                    ]

    for category in categories:
        db.session.add(Category(category=category))

    db.session.commit()



def load_movies():
    """Load movies from u.item into database and record movie categories."""

    print 'Movies'

    Movie.query.delete()

    for row in open('seed_data/u.item'):
        movie_info = row.rstrip().split('|')

        movie_id, title, released_at, blank, imdb_url = movie_info[:5]

        if released_at:
            released_at = datetime.strptime(released_at, "%d-%b-%Y")
        else:
            released_at = None

        title = title[:-7]

        movie = Movie(movie_id=movie_id, title=title, released_at=released_at, 
                    imdb_url=imdb_url)

        db.session.add(movie)
        db.session.commit()
        # Create categories for each movie:
        for i in range(5, len(movie_info)):
            if movie_info[i] == '1':
                category_id = MOVIE_CATEGORIES[i]
                db.session.add(MovieCategory(category_id=category_id, 
                                                movie_id=movie_id))
                db.session.commit()



def load_ratings():
    """Load ratings from u.data into database."""

    print 'Ratings'

    Rating.query.delete()

    for row in open('seed_data/u.data'):
        user_id, movie_id, score, timestamp = row.rstrip().split('\t')
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    create_categories()
    load_movies()
    load_ratings()
    set_val_user_id()
