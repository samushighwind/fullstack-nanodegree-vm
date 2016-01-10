# server libraries
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# sql ORM libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# classes from our ORM schema
from database_setup import Base, Restaurant, MenuItem

# other libraries
import textwrap
import re


# set up ORM
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_restaurant_div(restaurant):
    restaurant_id = restaurant.id
    id_attr = "restaurant_%s" % restaurant_id
    name = restaurant.name
    edit_address = "/restaurants/%s/edit" % restaurant_id
    delete_address = "/restaurants/%s/delete" % restaurant_id
    return textwrap.dedent("""\
        <div id="%s" class="restaurant">
            <div class="restaurant_name">%s</div>
            <div class="restaurant_edit"><a href="%s">Edit</a></div>
            <div class="restaurant_delete"><a href="%s">Delete</a></div>
        </div>""" % (id_attr, name, edit_address, delete_address)
    )


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/restaurants":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                restaurant_divs = map(get_restaurant_div, restaurants)
                output = ""
                output += "<html><body>"
                output += textwrap.dedent("""\
                    <div><a href="/restaurants/new">
                    Make a new restaurant here
                    </a></div>"""
                )
                output += "".join(restaurant_divs)
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path == "/restaurants/new":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += textwrap.dedent("""\
                    <form method="POST"
                          enctype="multipart/form-data"
                          action="/restaurants/new">
                        <h1>Make a New Restaurant</h1>
                        <input name="new_restaurant" type="text">
                        <input type="submit" value="Create">
                    </form>"""
                )
                output += "</body></html>"
                self.wfile.write(output)
                return

            if re.match('^\/restaurants\/[0-9]+\/edit$', self.path):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                restaurant_id = int(self.path.split("/")[2])
                restaurant = session.query(Restaurant) \
                                    .filter_by(id=restaurant_id) \
                                    .one()
                name = restaurant.name
                output = ""
                output += "<html><body>"
                output += textwrap.dedent("""\
                    <form method="POST"
                          enctype="multipart/form-data"
                          action="/restaurants/%s/edit">
                        <h2>%s</h2>
                        <input
                            name="new_restaurant_name"
                            type="text"
                            placeholder="%s">
                        <input type="submit" value="Rename">
                    </form>""" % (restaurant_id, name, name)
                )
                output += "</body></html>"
                self.wfile.write(output)
                return

            if re.match('^\/restaurants\/[0-9]+\/delete$', self.path):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                restaurant_id = int(self.path.split("/")[2])
                restaurant = session.query(Restaurant) \
                                    .filter_by(id=restaurant_id) \
                                    .one()
                name = restaurant.name
                output = ""
                output += "<html><body>"
                output += textwrap.dedent("""\
                    <form method="POST"
                          enctype="multipart/form-data"
                          action="/restaurants/%s/delete">
                        <h1>Are you sure you want to delete %s?</h1>
                        <input type="submit" value="Delete">
                    </form>""" % (restaurant_id, name)
                )
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path == "/restaurants/new":
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader("content-type")
                )
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get("new_restaurant")[0]
                    new_restaurant = Restaurant(name=new_restaurant_name)
                    session.add(new_restaurant)
                    session.commit()
                
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/restaurants")
                self.end_headers()
                return

            if re.match('^\/restaurants\/[0-9]+\/edit$', self.path):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader("content-type")
                )
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get("new_restaurant_name")[0]
                    restaurant_id = int(self.path.split("/")[2])
                    restaurant = session.query(Restaurant) \
                                        .filter_by(id=restaurant_id) \
                                        .one()
                    restaurant.name = new_name
                    session.add(restaurant)
                    session.commit()
                
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/restaurants")
                self.end_headers()
                return

            if re.match('^\/restaurants\/[0-9]+\/delete$', self.path):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader("content-type")
                )
                if ctype == "multipart/form-data":
                    restaurant_id = int(self.path.split("/")[2])
                    restaurant = session.query(Restaurant) \
                                        .filter_by(id=restaurant_id) \
                                        .one()
                    session.delete(restaurant)
                    session.commit()
                
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/restaurants")
                self.end_headers()
                return

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(("",port), WebserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("\n" + "^C entered, stopping web server...")
        server.socket.close()


if __name__ == "__main__":
    main()
