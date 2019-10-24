from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3

import os

file_path = os.path.abspath(os.getcwd())+"\database.db"
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Models goes here 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    about = db.Column(db.String)
    release_date = db.Column(db.String)
    def __str__(self, name, author, about, release_date):
        return self.name, self.author, self.about, self.release_date

# Marshmallow serilaziation
class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'about', 'release_date')

book_schema = BookSchema()
book_schemas = BookSchema(many=True)



# Resources goes here
class Booklist(Resource):
    def get(self):
        books = Book.query.all()
        return book_schemas.dump(books)
class BookOne(Resource):
    def get(self, id):
        book = Book.query.get(id)
        return book_schema.dump(book)
#resource routes
api.add_resource(Booklist, '/books')
api.add_resource(BookOne, '/books/<int:id>')

if __name__ == '__main__':
    app.run()
