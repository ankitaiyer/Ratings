from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))
#NoResultFound = None

#ENGINE = None
#Session = None

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)


class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    released_at = Column(String(64), nullable=True)
    imdb_url = Column(String(64), nullable=True)


class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    user = relationship("User", 
            backref=backref("ratings", order_by=id))

    movie = relationship("Movies", 
            backref=backref("ratings", order_by=id))
#    timestamp = Column(Integer, nullable=True)

### End class declarations

def authenticate(emailform, passwordform):
    user = session.query(User).filter_by(email=emailform).first()
    if int(user.password) == int(passwordform):
        return user.email
    else:
        return "Auth failed"

def register_user(emailform, passwordform, ageform, zipcodeform):
    print emailform
    temp_user = User(email=emailform, password=hash(passwordform), age=ageform, zipcode=zipcodeform)
    print temp_user.email
    session.add(temp_user)
    session.commit()

def getUserMovieRatings(userid):
    u = session.query(User).get(userid)
    ratings = session.query(Ratings).filter_by(user_id=u.id).all()
    #movies = session.query(Movies).filter_by(movie_id=ratings.movie_id)
    movies = []
    movie_ratings = []
    for r in ratings:
        movie = session.query(Movies).get(r.movie_id)
        movies.append(movie)
        movie_ratings.append((movie.name, r.rating, movie.id))
    return movie_ratings

def getRatingsForMovie(movieid):
    m = session.query(Movies).get(movieid)
    ratings = session.query(Ratings).filter_by(movie_id=m.id).all()
    user_ratings = []
    for r in ratings:
        user = session.query(User).get(r.movie_id)
       # users.append(user)
        user_ratings.append((r.user_id, r.rating, m.name, user.zipcode))
    return user_ratings

def addEditRating(userid,movieid,rating):
#    print rating
    try:
        current_rating = session.query(Ratings).filter_by(movie_id=movieid, user_id=userid).one()
        current_rating.rating = rating
        session.commit()
    except NoResultFound:
#        print "RATING", rating
        temp_rating = Ratings(user_id=userid, movie_id=movieid, rating=rating)
        session.add(temp_rating)
        session.commit()

def getUserID(email):
    user = session.query(User).filter_by(email="c.com").one()
    return user.id

def main():


    if __name__ == "__main__":
        main()

