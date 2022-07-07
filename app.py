"""Flask app for Cupcakes"""
from flask  import Flask, render_template, request, flash, jsonify, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
import requests


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_list_and_form():
    """ Render the main page, which includes the cupcake from
        and a space to show a list or existing cupcakes. The 
        list itself is loaded via Javascript that uses API calls. """
    return render_template('index.html', title="Cupcakes")

@app.route('/api/cupcakes')
def get_all_cupcakes():
    """ API to read all cupcakes from the db """
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.read_all_cupcakes()]
    return jsonify({'cupcakes': all_cupcakes})

@app.route('/api/cupcakes/<int:id>')
def get_cupcake_info(id):
    """ API to read a single cupcake from the db """
    cupcake = Cupcake.serialize(Cupcake.read_cupcake_info(id))
    return jsonify({'cupcake': cupcake})

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """ Add a cupcake to the db """
    print(f"f: {request.json['flavor']} s: {request.json['size']} r: {request.json['rating']} i: {request.json['image']}")
    new_cupcake = Cupcake(flavor=request.json['flavor'],
                          size=request.json['size'],
                          rating=request.json['rating'], 
                          image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    return (get_cupcake_info(new_cupcake.id), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """ Update a cupcake in the db """
        cupcake=Cupcake.read_cupcake_info(id)
        cupcake.flavor = request.json.get('flavor', cupcake.flavor)
        cupcake.size=request.json.get('size', cupcake.size)
        cupcake.rating=request.json.get('rating', cupcake.rating)
        cupcake.image=request.json.get('image', cupcake.image)
        # db.session.add(cupcake)
        db.session.commit()
        return (get_cupcake_info(cupcake.id), 200)


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """ Delete a cupcake from the db """
        cupcake=Cupcake.read_cupcake_info(id)
        Cupcake.delete(id)
        db.session.commit()
        return jsonify({'message': 'Deleted'})


