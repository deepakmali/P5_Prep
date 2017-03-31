from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += """
                            Hello There!!!
                          """    
                output += """
                          <form method="POST" enctype="multipart/form-data" action="/hello">
                                <h2> What would you like me to say? </h2>
                                <input name="message" type="text" >
                                <input type="submit" value="Okay">
                          </form>
                          """
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ""
                output = "<html><body>"
                output += """
                            Hola amigos!!! <a href="/hello"> back to hello</a>
                          """    
                output += """
                          <form method="POST" enctype="multipart/form-data" action="/hello">
                                <h2> What would you like me to say? </h2>
                                <input name="message" type="text" >
                                <input type="submit" value="Okay">
                          </form>
                          """
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error("404 Not found")

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this!!: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += """
                          <form method="POST" enctype="multipart/form-data" action="/hello">
                                <h2> What would you like me to say? </h2>
                                <input name="message" type="text" >
                                <input type="submit" value="Okay">
                          </form>
                          """
                output += "</body></html>"
                self.wfile.write(output)

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