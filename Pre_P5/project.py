from flask import Flask, render_template
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def display_restaurants():
    restaurants = session.query(Restaurant).all()
    render_template('restaurant.html', restaurants=restaurants)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)