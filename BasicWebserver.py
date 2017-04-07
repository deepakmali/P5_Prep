from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def getDbSession():
    engine = create_engine("sqlite:///restaurantmenu.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # cursor = session.cursor()
    return session


def closeSession(session, commit=True):
    if commit:
        session.commit()
    else:
        session.rollback()
    session.close()


def create_restaurant(restaurant):
    session = getDbSession()
    session.add(restaurant)
    closeSession(session=session)
    return

def getRestaurant(id):
    session = getDbSession()
    restaurant = session.query(Restaurant).get(int(id))
    return restaurant


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                session = getDbSession()
                restaurants = session.query(Restaurant.name, Restaurant.id).all()
                restaurant_list = ""
                for restaurant in restaurants:
                    restaurant_list += """<h3>%s</h3> <label name=id hidden> %s </label> 
                                        <a href="/restaurants/%s/edit">Edit</a><br>
                                        <a href="/restaurants/id/delete">Delete</a>
                                        """ % (restaurant.name, restaurant.id, restaurant.id )
                output = ""
                output += "<html><body>"
                output += """
                            <h1>List of Restaurants</h1>
                          """    
                output += restaurant_list
                output += "</body></html>"

                closeSession(session, commit=False)
                self.wfile.write(output)
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output = "<html><body>"
                output += "<h2>Add the new Restaurant</h2>"    
                output += """
                          <form method="POST" enctype="multipart/form-data" action="/restaurants/new">
                                <h2> Enter the Restaurant Name: </h2>
                                <input name="restaurant_name" type="text" >
                                <input type="submit" value="Create">
                          </form>
                          """
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                restaurant_id = getRestaurant(int(self.path.split('/')[2]))

                output = ""
                output += "<html><body>"
                output +=  """
                          <form method="POST" enctype="multipart/form-data" action="/restaurants/%s/edit">
                                <h2> Edit the Restaurant Name: </h2>
                                <input name="restaurant_name" type="text" value = "%s" >
                                <input type="submit" value="Update">
                          </form>
                          """ % (restaurant_id.id, restaurant_id.name)
                output += "</body></html>"
                self.wfile.write(output)


        except IOError:
            self.send_error("404 Not found")

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant_name')
                    restaurant = Restaurant(name=restaurant_name[0])
                    create_restaurant(restaurant=restaurant)
                    output = ""
                    output += "<html><body>"
                    # output += "<h2> Okay, how about this!!: </h2>"
                    output += """<h1>Added "%s" to the Restaurant Table. </h1>""" % restaurant_name[0]

                    output += """ Clicke <a href="/restaurants">here</a> to go back to main page.
                              """
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith('/edit'):                
                restaurant_id = self.path.split('/')[2]
                restaurant = getRestaurant(int(restaurant_id))
                print restaurant.name
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('restaurant_name')
                    print restaurant_name
                    restaurant.name = restaurant_name[0]
                    print restaurant.name
                    create_restaurant(restaurant=restaurant)
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()


        except Exception as e:
            raise e


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        print "Server is running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "User chose to stop the server"
        server.socket.close()


if __name__ == '__main__':
    main()