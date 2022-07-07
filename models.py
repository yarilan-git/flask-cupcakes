"""Models for Cupcakes."""

from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    __tablename__ = 'cupcake'

    id      = db.Column(db.Integer, primary_key = True, autoincrement = True)
    flavor    = db.Column(db.Text, nullable=False)
    size      = db.Column(db.Text, nullable=False)
    rating    = db.Column(db.Float, nullable=False)
    image    = db.Column(db.Text,  default='https://tinyurl.com/demo-cupcake')

    @classmethod
    def read_all_cupcakes(self):
        return Cupcake.query.all()
    
    def read_cupcake_info(id):
        return Cupcake.query.get_or_404(id)

    def delete(id):
        return Cupcake.query.filter_by(id=id).delete()

    def serialize(self):
        return {
                'id':     self.id,
                'flavor': self.flavor,
                'size':   self.size,
                'rating': self.rating,
                'image': self.image
                }

    def __repr__(self):
        return f"id: {self.id}, flavor: {self.flavor}, size: {self.size},   rating: {self.rating}, image: {self.image}"


    