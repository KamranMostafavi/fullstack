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

    def setObjective2Output(self, output, session):
        '''

        :param output: html output message where list of restaurants needs to be appended to
        :param session: the ORM session
        :return: output: modified output html message containing the list of restaurants in the db file
        '''
        output += "<h1>List of Restaurants in the database!</h1>"

        for row in session.query(Restaurant).all():
            output += row.name + "<br>" + "<a href= # > Edit <a/><br><a href= # > Delete <a/><br>"

        return output
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                engine = create_engine(
                    'sqlite:///restaurantmenu.db')  # indicate dbase file to use and create an object for
                Base.metadata.bind = engine  # bind the base model to the engine (maps class definitions to corresponding tables in db file)
                DBSession = sessionmaker(
                    bind=engine)  # session contains work to be done by the engine prior to committing.
                session = DBSession()  # an instance of the DBSession creates a staging session to create db commands.

                # display contents of the Restaurant table
                output = ""
                output += "<html><body>"
                output = self.setObjective2Output(output, session)
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='UTF-8'))
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
