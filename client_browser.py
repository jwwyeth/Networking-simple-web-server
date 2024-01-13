#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Run with the following command line parameters:
python3 client_browser.py <hostname> <port> <file>

Examples:
$ python3 client_browser.py info.cern.ch 80 "" # defaults to index.html
$ python3 client_browser.py localhost 6789 "hello_world.html"
"""

import sys
import socket

if len(sys.argv) != 4:
    server_hostname = "localhost"
    server_ip = "127.0.0.1"
    server_port = 6789
    file_name = "web_files/hello_world.html"
else:
    # do your arg parsing here.
    # Hint, you may need to get an IP from a hostname.
    server_hostname = sys.argv[1]
    server_ip = socket.gethostbyname(server_hostname)
    server_port = int(sys.argv[2])
    file_name = sys.argv[3]


try:
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client_socket.connect((server_hostname, server_port))
    # make your GET request here
    Get_request = f"GET /{file_name} HTTP/1.1\r\nHost: {server_hostname}\r\n\r\n"
    # print(Get_request)
    client_socket.send(Get_request.encode())

    # parse the return data here.
    # Hint: a loop helps to make sure you got all the data.
    # Just print what's returned from the server.

    # we make a list called info that will recieve all of the info that is recieved from the server
    # we then join it togehter into bytes to then be decoded and readable in a final print statement
    info = []
    while True:
        returned_info = client_socket.recv(1024)
        if not returned_info:
            break
        info.append(returned_info)
    readable_info = b"".join(info)
    print(readable_info.decode())

except Exception as e:
    print("Exception was: ", e)

finally:
    client_socket.close()
