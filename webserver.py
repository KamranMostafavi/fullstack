# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer

hola = False

if hola:
    class WebServerHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path.endswith("/hello"):
                self.send_response(200)  # success returned
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>Hello!</body></html>"  # contents which is a html page returned
                self.wfile.write(message.encode(encoding='UTF-8'))  # need to convert to byte stream to work in python3
                print(message)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body> &#161 Hola ! <a href= '/hello' > Back to hello <a/> </body></html>"
                self.wfile.write(message.encode(encoding='UTF-8'))
                print(message)
                return
            else:
                # here if path was not correct
                self.send_error(404, 'File Not Found: %s' % self.path)


    def main():
        try:
            # port for http to communicate over
            port = 8080
            # specify the port and handler for localhost
            server = HTTPServer(('', port), WebServerHandler)
            print("Web Server running on port %s" % port)
            # run server
            server.serve_forever()
        except KeyboardInterrupt:
            # if keyboard interrupt then kill the server by closing the socket
            print(" ^C entered, stopping web server....")
            server.socket.close()


    if __name__ == '__main__':
        main()

import cgi  # common gateway interface used by POST for forms


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2><input name="message" type="text" >
                            <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='UTF-8'))
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2><input name="message" type="text" >
                            <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='UTF-8'))
                print(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)  # indicates successful post
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print("1")
            # parse the contents of the form passed in the header into a dictionary
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes (pdict['boundary'], "utf-8")
            print("2")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')  # get the value of message in the form
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like me to say?</h2><input name="message" type="text" >
                        <input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='UTF-8'))
            print(output)
        except:
            pass


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
