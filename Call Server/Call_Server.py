# Created by Charles Vega
# Last Modified December 16, 2021
# This boots up the computer as a server
# The server will wait for pairs of clients who wish to join a voice call
# For every two clients who connect to the server, a new voice call is made
# Users must signal for the server to stop accepting new clients by entering any value

import socket
import threading
import concurrent.futures
import time

# 2048 bytes of data is sent at a time
MSG_LENGTH = 2048
# Create a socket object for internet streaming through IPV4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# (IPV4 address, free port number)
SERVER = (socket.gethostbyname(socket.gethostname()), 7777)
server.bind(SERVER)

# Waits for user input, then sets terminate to true
# @terminate is an event shared between each thread to end the program
def user_input(terminate):
    # Wait 1 second
    time.sleep(1)
    # Request user signal to terminate
    input("At any point press enter to stop accepting new connections \n")
    # Set terminate to true
    terminate.set()

# exchange_audio will always be called by two threads at a time
# In one thread audio from connection1 gets sent to connection2
# In the other, audio from connection2 gets sent to connection1
# When either client disconnects or the server wishes to terminate, both connections will close automatically
# @connection1 and connection2 are two seperate clients who wish to join in a voice call
# @address indicates the IP address of a thread's connection1
# @terminate will tell this function to close
def exchange_audio(connection1, connection2, address, terminate):
    print(f"Receiving audio from {address}")
    # Will loop until terminate is true
    while not terminate.is_set():
        try:
            audio_data = connection1.recv(MSG_LENGTH)
            try:
                connection2.send(audio_data)
            except socket.error:
                print("Audio send error")
                break
        except socket.error:
            print(f"Connection lost with {address}")
            break
    # End connection with client once voice call finishes
    connection1.close()
    print(f"Ending connection with {address}")


# This will connect to a client and return their address and connection
def getClient():
    # connected determines if a successful connection has been made
    connected = False
    # Wait for a first client to successfully connect
    while not connected:
        connection, address = server.accept()
        connected = True
        try:
            connection.send(bytes(
                "Your friend should be connecting to the server soon!", "utf-8"))
        except socket.error:
            print("Failed to connect to the client")
            connected = False
    return connection, address

# This function will synchronize the given clients for a voice call
# @connection1 and connection2 are two seperate clients who wish to join in a voice call
# @address1 and address2 indicates the IP addresses of the clients
def syncClients(connection1, connection2, address1, address2):
    # For every attempted send we initiate a try and except statement
    # If a client abruptly connects we close connection with them and their partner
    try:
        connection1.send(
            bytes("Your friend is ready to chat! Your voice call should start soon!", "utf-8"))
        try:
            connection2.send(bytes("Your friend is ready to chat! Your voice call should start soon!", "utf-8"))
            time.sleep(1)
        except socket.error:
            print(f"Connection abruptly terminated with {address2}")
            print(f"Closing connection with {address2}")
            connection2.close()
            try:
                connection1.send(bytes("DISCONNECTED", "utf-8"))
            except socket.error:
                print(f"Connection abruptly terminated with {address1}")
            print(f"Closing connection with {address1}")
            connection1.close()
    except socket.error:
        print(f"Connection abruptly terminated with {address1}")
        print(f"Closing connection with {address1}")
        connection1.close()
        try:
            connection2.send(bytes("DISCONNECTED", "utf-8"))
        except socket.error:
            print(f"Connection abruptly terminated with {address2}")
        print(f"Closing connection with {address2}")
        connection2.close()

# Main runner function of the server
# Will wait for two clients at a time then join them in a voice call
# Each voice call will create a pair of threads
# The first thread will receive audio from one client then send it to the other
# The second thread will perform the same task as the first thread but in reverse direction
def start():
    print("Starting the server...")
    # Open the server for connections
    server.listen()
    print(f"Server is accepting clients on {SERVER}")
    # Event which tells all threads to stop
    terminate = threading.Event()
    print("Waiting for the first client to connect...")
    connection1, address1 = getClient()
    print(f"Connection successful with {address1}")
    print("Waiting for the second client to connect...")
    connection2, address2 = getClient()
    print(f"Connection successful with {address2}")
    syncClients(connection1, connection2, address1, address2)
    # Create threads to exchange audio between clients
    # 1 to 1 voice calls are created indefinitely until terminate is set
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Exchange audio data between the clients, creating a call
        executor.submit(exchange_audio, connection1,
                        connection2, address1, terminate)
        executor.submit(exchange_audio, connection2,
                        connection1, address2, terminate)
        # Terminate
        executor.submit(user_input, terminate)
        # This loop will create new 1 to 1 voice calls
        while not terminate.is_set():
            # Wait for a new client
            print("Waiting for two new clients...")
            connection1, address1 = getClient()
            print(f"Connection successful with {address1}")
            # Wait for the second client to connect
            print("Waiting for the second client to connect...")
            connection2, address2 = getClient()
            print(f"Connection successful with {address2}")
            syncClients(connection1, connection2, address1, address2)
            # Exchange audio data between the clients, creating a call
            executor.submit(exchange_audio, connection1,
                            connection2, address1, terminate)
            executor.submit(exchange_audio, connection2,
                            connection1, address2, terminate)

if __name__ == "__main__":
    start()
