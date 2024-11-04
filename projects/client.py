#!/usr/bin/python3
#Colin Myers
#CSC 328
#Fall 2023 Semester
#Project 5

import sys
import socket

#Function Name: receive_packets
#description:   creates a socket, connects to the server, receives 
#               word packets, decodes word packets into words, and 
#               prints the words
#parameters:    host - input - the host ip address for connecting to the server
#               port - input - the port number for connecting to the server
def receive_packets(host, port):
    try:
        #create socket and connect to server
        psocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        psocket.connect((host, port))

        while True:
            x = psocket.recv(1)
            if len(x) != 0: #check that there are still word packets to be read
                lengthBytes = psocket.recv(1) + x
                if lengthBytes == 0:
                    print("received empty lengthBytes. connection closed by the server")
                    pass

                #convert to little endian
                packetLength = int.from_bytes(lengthBytes, byteorder='little')
                word_buffer = b""
                while len(word_buffer) < packetLength:
                    data = psocket.recv(packetLength - len(word_buffer))#grab bytes from socket
                    if not data:
                        print("received empty data. connection closed unexpectedly")
                        break
                    word_buffer += data

                word = word_buffer.decode('utf-8')#decode from little endian into a string

                print(word)
            else:
                break

        psocket.close() #close the socket

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: <client_exec> <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    receive_packets(host, port)
