#!/usr/bin/env python3

from app import app
from models import db, Plant

def seed_data():
    with app.app_context():
        db.create_all()  # Ensure tables are created

        # Clear existing data
        Plant.query.delete()

        # Add sample data
        plants = [
            Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
            Plant(name="Snake Plant", image="./images/snake.jpg", price=18.00, is_in_stock=True),
        ]

        db.session.bulk_save_objects(plants)
        db.session.commit()

        print("Database seeded!")

if __name__ == "__main__":
    seed_data()