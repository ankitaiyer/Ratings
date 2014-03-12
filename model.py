from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
import correlation

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

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
                for r in other_ratings ]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
#        top_user = similarities[0]
#        return top_user[1].rating * top_user[0]
        print similarities 
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator


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
#   check to see if a rating exists for this user and movie
    current_rating = session.query(Ratings).filter_by(movie_id=movieid, user_id=userid).first()
#   if we don't find a rating for this user and movie, add the user/movie to the table
    if not current_rating:
        current_rating = Ratings(user_id=userid, movie_id=movieid)
#   whether or not the record previously existed, add/update the rating for the user/movie
#   this saves us from recycling a lot of code
    current_rating.rating = rating

    try:
        session.add(current_rating)
        session.commit()
    except:
        print "OOps, database gave an error"
#        print "RATING", rating
        return None
    
    return current_rating

def getUserID(email):
    user = session.query(User).filter_by(email="c.com").one()
    return user.id

def main():


    if __name__ == "__main__":
        main()

