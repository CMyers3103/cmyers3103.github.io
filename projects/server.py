#!/usr/bin/python3
#Colin Myers
#CSC 328
#Fall 2023
#Project 6

import sys
import socket
import random

#function name: make_wordpackets
#description: generates a random number and makes that number of word packets and returns the count of word packets and the array containing the word packets
#parameters: none
#return values: random_number - the count of how many word packets were randomly generated
#               wordpackets - the array containing the generated wordpackets
def make_wordpackets():
    words = ["apple", "banana", "cherry", "date", "fig", "grape", "honey", "ice", "juice", "kiwi", "lemon", "mango", "nut", "olive", "pear", "potato", "raisin", "strawberry", "tangerine", "watermelon"]

    random_number = random.randint(1, 10)
    count = 0
    wordpackets = []
    while count < random_number:
        random_word = words[random.randint(0, 19)]
        wordbytes = random_word.encode('utf-8')
        wordlength = len(wordbytes).to_bytes(2, 'big')
        wordpacket = wordlength + wordbytes
        index = 0
        wordpackets.append(wordpacket)
        index = index + 1
        count = count + 1
    return (random_number, wordpackets)

#function name: socket_bind
#descriptions: makes a socket, binds the socket, listens for connections, and calls the infinite loop
#parameters: port - input - the port that the socket is bound to
def socket_bind(port):
    try:
        address = '127.0.0.1'
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((address, port))
        server_socket.listen(5)
        print("Socket bound to " + address + ":" + str(port))
        loopstuff(server_socket)

    except Exception as e:
        print("Error: " + str(e))

#function name: loopstuff
#description: an infinite loop that waits for a connection from a client and calls the function to generate wordpackets. it then sends the generated wordpackets to the client and closes the client connection
def loopstuff(server_socket):
    while True:
        print("Waiting for connection")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from " + str(client_address))
        random_numb, wordpacketsarray = make_wordpackets()
        counter = 0
        while counter < random_numb:
            try:
                client_socket.send(wordpacketsarray[counter])
            except Exception as e:
                print("Error in send: " + str(e))
            counter = counter + 1
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: <server_exec> <port>")
        sys.exit(1)

    port = int(sys.argv[1])


    socket_bind(port)
