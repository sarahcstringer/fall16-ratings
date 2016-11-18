"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from model import connect_to_db, db, User, Rating, Movie, Category, MovieCategory

from sqlalchemy.sql import func

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage."""
    print dir(request.headers)
    print request.headers
    return render_template('homepage.html')

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template('user_list.html', users=users)

@app.route('/users/<id>')
def show_user_details(id):

    user = User.query.get(id)

    return render_template('user_details.html', user=user)

@app.route('/movie/<id>')
def show_movie_details(id):

    movie = Movie.query.get(id)
    avg_rating = db.session.query(func.avg(Rating.score)).filter(
                                                Rating.movie_id==id).one()
    # print avg_rating

    return render_template('movie_details.html', movie=movie, 
                            avg_rating=avg_rating)


@app.route('/movies')
def movie_list():
    """Show list of movies"""

    movies = Movie.query.order_by(Movie.title).all()
    
    return render_template('movie_list.html', movies=movies)


@app.route('/signup')
def add_user():
    """Add user to database"""

    email = request.form.get('email')

    try:
        user = User.query.filter_by(email=email).one()
        return jsonify({'result': 'bad_username'})

    except:
        password = request.form.get('password')
        zipcode = request.form.get('zip')
        dob = request.form.get('dob')
        # age = 
        user = User(email=email, password=password, zipcode=zipcode,
                    )

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0')
