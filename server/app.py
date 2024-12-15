#!/usr/bin/env python3

# Import necessary modules
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

# Set up the Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Set up Flask-RESTful for handling routes
api = Api(app)

# Define a class for handling all plants (GET and POST routes)
class Plants(Resource):
    def get(self):
        # Get all plants from the database
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        # Get the data from the request body
        data = request.get_json()

        # Create a new plant instance
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )

        # Add the new plant to the database
        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

# Add the route for Plants
api.add_resource(Plants, '/plants')


# Define a class for handling individual plants (GET, PATCH, DELETE routes)
class PlantByID(Resource):
    def get(self, id):
        # Get a single plant by ID
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            # If the plant is not found, return a 404 error
            return make_response(jsonify({"error": "Plant not found"}), 404)
        return make_response(jsonify(plant.to_dict()), 200)

    def patch(self, id):
        # Get the plant to update by ID
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        # Get the updated data from the request body
        data = request.get_json()

        # Update the plant's "is_in_stock" status if it is in the data
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]

        # Save the changes to the database
        db.session.commit()

        # Return the updated plant as JSON
        return make_response(jsonify(plant.to_dict()), 200)

    def delete(self, id):
        # Get the plant to delete by ID
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        # Remove the plant from the database
        db.session.delete(plant)
        db.session.commit()

        # Return an empty response with a 204 status code
        return make_response('', 204)

# Add the route for individual plants
api.add_resource(PlantByID, '/plants/<int:id>')


# Run the Flask application
if __name__ == '__main__':
    app.run(port=5555, debug=True)