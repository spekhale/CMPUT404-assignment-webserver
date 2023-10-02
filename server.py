#  coding: utf-8 
import socketserver, os
from urllib import request

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        print("Started...") #just checking if server started properly

        self.data = self.request.recv(1024).strip() #receiving clean/readable data upto 1024 bytes

        #print ("Got a request of: %s\n" % self.data) #printing the data received

        #self.request.sendall(bytearray("OK",'utf-8')) #sending data to client, if successful

        location = " "

        HTTP_method, self.HTTP_url, HTTP_version = readable_data(self.data) #store the method, url, version

        if HTTP_method == "GET":
            
            if self.HTTP_url[-4:] != ".css":
                if self.HTTP_url[-10:] != "index.html":
                    if self.HTTP_url[-1] == "/": #requesting a dir
                        self.HTTP_url = self.HTTP_url + "index.html"
                    else: #requesting a file
                        self.handle_301error(location)
                        return
            
            location = "./www" + self.HTTP_url
                
        #check for other methods POST, PUT, DELETE, etc
        else:
            self.handle_405error()
            return
            

        if ".html" in self.HTTP_url:
            self.handle_file_location(location, "text/html")
        elif ".css" in self.HTTP_url:
            self.handle_file_location(location, "text/css")
        #else:
            #self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed",'utf-8'))
            #return

    def handle_file_location(self, location, content_type):
        #check if correct path
        if os.path.exists(location):
            filename = open(location, "r")
            fileinfo = filename.read()
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" +content_type +"\r\n"  +"\r\n\r\n"+fileinfo,'utf-8'))
            return
            

        else: 
            self.handle_404error()
            return

    def handle_301error(self, location):
        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + self.HTTP_url +'/' +"\r\n\r\n301 Moved Permanently",'utf-8'))

    def handle_405error(self):
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed",'utf-8'))

    def handle_404error(self):
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n404 Not Found",'utf-8'))


    
        
    



def readable_data(data):
    python_data_string = data.decode("utf-8")
    final_data = python_data_string.split("\r\n")[0]
    HTTP_method, HTTP_url, HTTP_version = final_data.split(" ")
    return HTTP_method, HTTP_url, HTTP_version


            
    
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
