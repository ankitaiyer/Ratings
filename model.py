from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

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
        movie_ratings.append((movie.name, r.rating))
    return movie_ratings



def main():


    if __name__ == "__main__":
        main()

