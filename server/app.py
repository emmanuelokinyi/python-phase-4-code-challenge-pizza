from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False


migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    return make_response(jsonify(restaurants), 200)

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def handle_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if not restaurant:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

    if request.method == 'GET':
        return make_response(jsonify(restaurant.to_dict()), 200)

    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(jsonify({}), 204)

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
    return make_response(jsonify(pizzas), 200)

@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def handle_restaurant_pizzas():
    if request.method == 'GET':
        restaurant_pizzas = [rp.to_dict() for rp in RestaurantPizza.query.all()]
        return make_response(jsonify(restaurant_pizzas), 200)

    elif request.method == 'POST':
        data = request.get_json()
        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return make_response(jsonify(restaurant_pizza.to_dict()), 201)
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
