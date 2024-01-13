#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
A simple Web server.
GET requests must name a specific file,
since it does not assume an index.html.
"""

import socket
import threading


def handler(conn_socket: socket.socket, address: tuple[str, int]) -> None:
    """
    Handles the part of the client work-flow that is client-dependent,
    and thus may be delayed by the user, blocking program flow.
    """
    try:
        # Receives the request message from the client
        request_msg = conn_socket.recv(1024)
        # print("Request message: ", request_msg,"\r\n")
        # r=request_msg.decode()
        # print("The decoded message is: ", r)

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        # Read file off disk, to send
        # Store the content of the requested file in a temporary buffer
        object_path = request_msg.decode().split()[1][1:]

        x = open(object_path)
        content = x.read()
        # print('content: ',content)

        # Send the HTTP response header line to the connection socket

        conn_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")

        # Send the content of the requested file to the connection socket

        conn_socket.send(content.encode())

    except IOError:
        # Send HTTP response message for file not found (404)

        conn_socket.send(b"HTTP/1.1 404 File not found \r\n\r\n")

        # Open file, store the content of the requested file in a temporary >

        unknown_file = open("web_files/not_found.html", "r")
        err_buffer = unknown_file.read()

        # Send the content of the requested file to the connection socket
        conn_socket.send(err_buffer.encode())

    except:
        print("Bad request")
    finally:
        conn_socket.close()


def main() -> None:
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_port = 6789

    # Bind the socket to server address and server port
    server_socket.bind(("", server_port))

    # Listen to at most 2 connection at a time
    # Server should be up and running and listening to the incoming connections
    server_socket.listen(2)

    threads = []
    try:
        while True:
            print("ready!")
            # Set up a new connection from the client
            c, addr = server_socket.accept()
            print("Got connection from: ", addr)
            # call handler here, start any threads needed

            new_thread = threading.Thread(target=handler, args=(c, addr))
            new_thread.start()

            # Just to keep track of threads
            threads.append(new_thread)

            print(threads)

    except Exception as e:
        print("Exception occured (maybe you killed the server)")
        print(e)
    except:
        print("Exception occured (maybe you killed the server)")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
