from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

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
    movie_id = Column(Integer)
    user_id = Column(Integer)
    rating = Column(Integer)
#    timestamp = Column(Integer, nullable=True)



### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()
# any time you need a session later, you can just do 'session = Session()'


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()

