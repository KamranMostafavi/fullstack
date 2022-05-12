# needed to implement the webserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi  # common gateway interface used by POST for forms

# needed to access the ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# needed to access the objects needed to access the tables
from database_setup import Base, Restaurant, MenuItem


import cgi  # common gateway interface used by POST for forms

class webServerHandler(BaseHTTPRequestHandler):

    def getOrmSession(self):
        engine = create_engine(
            'sqlite:///restaurantmenu.db')  # indicate dbase file to use and create an object for
        Base.metadata.bind = engine  # bind the base model to the engine (maps class definitions to corresponding tables in db file)
        DBSession = sessionmaker(
            bind=engine)  # session contains work to be done by the engine prior to committing.
        session = DBSession()  # an instance of the DBSession creates a staging session to create db commands.
        return session

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):

                def setObjective3Output(output, session):
                    '''

                    :param output: html output message where list of restaurants needs to be appended to
                    :param session: the ORM session
                    :return: output: modified output html message containing the list of restaurants in the db file
                    '''
                    output += "<h1><a href = /restaurants/new > Make a new restaurant<a/></h1>"

                    for row in session.query(Restaurant).all():
                        output += row.name + "<br>" + "<a href= /restaurants/" + str(row.id) + "/edit> Edit <a/><br><a href= /restaurants/" + str(row.id) + "/delete> Delete <a/><br>"

                    return output

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = self.getOrmSession()

                # display contents of the Restaurant table
                output = ""
                output += "<html><body>"
                output = setObjective3Output(output, session)
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='UTF-8'))
                return

            if self.path.endswith("/restaurants/new"):
                def setObjective3Output(output, session):
                    '''

                    :param output: html output message where list of restaurants needs to be appended to
                    :param session: the ORM session
                    :return: output: modified output html message containing the list of restaurants in the db file
                    '''

                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                                <h1>Make a new restaurant</h1><input name="name" type="text" >
                                <input type="submit" value="Submit"> </form>'''
                    return output

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = self.getOrmSession()

                # display contents of the Restaurant table
                output = ""
                output += "<html><body>"
                output = setObjective3Output(output, session)
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='UTF-8'))
                return

            if self.path.endswith("/edit"):
                def setObjective4Output(output, restaurantName):
                    '''

                    :param output: html output message where list of restaurants needs to be appended to
                    :param session: the ORM session
                    :return: output: modified output html message containing the list of restaurants in the db file
                    '''

                    output += "<form method='POST' enctype='multipart/form-data' action=''><h1>"
                    output += restaurantName
                    output += '''</h1><input name="name" type="text" >
                                <input type="submit" value="Submit"> </form>'''
                    return output


                id=self.path.split("/")[-2]

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = self.getOrmSession()

                myRestaurant = session.query(Restaurant).get(id)
                restaurantName = myRestaurant.name

                output = ""
                output += "<html><body>"
                output=setObjective4Output(output,restaurantName)
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='UTF-8'))

                print (myRestaurant.name)
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)  # indicates successful post
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')    # after post is complete go back to this page
                self.end_headers()
                # parse the contents of the form passed in the header into a dictionary
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes (pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurantsName = fields.get('name')  # get the value of message in the form

                session = self.getOrmSession()

                # create a new restaurant in the database
                myFirstRestaurant = Restaurant(name=newRestaurantsName[0])
                session.add(myFirstRestaurant)  # add myFirstRestuarant to the staging zone
                session.commit()  # commit so it is writtent the database file
                return

            if self.path.endswith("/edit"):
                id=self.path.split("/")[-2]

                self.send_response(301)  # indicates successful post
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')    # after post is complete go back to this page
                self.end_headers()
                # parse the contents of the form passed in the header into a dictionary
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes (pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurantsName = fields.get('name')  # get the value of message in the form

                session = self.getOrmSession()

                myRestaurant = session.query(Restaurant).get(id)
                myRestaurant.name=newRestaurantsName[0]
                session.add(myRestaurant)
                session.commit()
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
