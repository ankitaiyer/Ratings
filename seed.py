import model
import csv
#session
def load_users(session):
    # use u.user
    filename = "seed_data/u.user"
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in reader:
            temp_user = model.User(id = row[0], email="", password="", age=row[1], zipcode=row[4])
            session.add(temp_user)
    session.commit()
    # user id | age | gender | occupation | zip code

def load_movies(session):
    # use u.item
    filename = "seed_data/u.item"
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in reader:
            title = row[1][:-6]
            title = title.decode("latin-1")
            print "ROW IS ", title
            temp_movie = model.Movies(id = row[0], name=title, released_at=row[2], imdb_url=row[4])
            session.add(temp_movie)
    session.commit()

#movie id | movie title | release date | video release date |
#    id = Column(Integer, primary_key=True)
#    name = Column(String(64), nullable=True)
#    released_at = Column(String(64), nullable=True)
#    imdb_url = Column(String(64), nullable=True)

def load_ratings(session):
    # use u.data
    filename = "seed_data/u.data"
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            temp_rating = model.Ratings(user_id=row[0], movie_id=row[1], rating=row[2])
            session.add(temp_rating)
    session.commit()
    # user id | item id | rating | timestamp
    # id, movie id, userid, rating


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)

#load_users(s)
load_movies(s)
#load_ratings(s)