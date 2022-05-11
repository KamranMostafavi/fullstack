#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)         #success returned
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello!</body></html>"   #contents which is a html page returned
            self.wfile.write(message.encode(encoding='UTF-8'))  #need to convert to byte stream to work in python3
            print (message)
            return
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body> &#161 Hola ! <a href= '/hello' > Back to hello <a/> </body></html>"
            self.wfile.write(message.encode(encoding='UTF-8'))
            print (message)
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
        print ("Web Server running on port %s" % port)
        #run server
        server.serve_forever()
    except KeyboardInterrupt:
        #if keyboard interrupt then kill the server by closing the socket
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()