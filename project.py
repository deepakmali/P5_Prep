from flask import Flask, render_template
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurant_id = session.query(Restaurant).first()
    # return restaurant_id.name
    menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id.id)
    # output = ''
    # for item in menuItems:
    #     output += item.name 
    #     output += '<br>'
    #     output += item.price
    #     output += '<br>'
    #     output += item.description
    #     output += '<br><br>'
    # print output
    # session.close()
    # return output
    return render_template("menu.html", restaurant=restaurant_id,
                           items=menuItems)

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0', port=8000)