import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import relationship

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()

class Movies(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  movie_name = Column(String, unique=True)
  price = Column(Integer)

  def __init__(self, movie_name, price):
    self.movie_name = movie_name
    self.price = price

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'movie_name': self.movie_name,
      'price': self.price,
    }

class Rents(db.Model):
  __tablename__ = 'rents'
  id = db.Column(db.Integer, primary_key=True)
  movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'))
  charges = db.Column(Integer)
  movie = relationship("Movies", cascade="all,delete", backref="movie")

  def __init__(self, movie_id, charges):
    self.movie_id = movie_id
    self.charges = charges

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'movie_id': self.movie_id,
      'charges': self.charges,
      'movie': self.movie.format()
    }