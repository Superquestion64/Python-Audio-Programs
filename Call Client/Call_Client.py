# Created by Charles Vega
# Last Modified December 16, 2021
# This program is effectively a client side voice call application
# It will create a client that records audio and sends it to a server computer in real time
# The client can only connect to the server computer, but it can receive audio data to play from the server
# Recorded audio from the client's default input device is sent to the server's default output device
# Users must signal for this program to terminate by entering any value
# Dependencies: PyAudio

import pyaudio
import socket
import threading
import concurrent.futures
import time

# NOTE: FOR THIS PROGRAM TO WORK ADDR MUST BE DEFINED
# Define SERVER_IP as IP address of the server
# If on a shared local network with the server use the IPV4 address of the server to replace SERVER_IP
# Otherwise the public IP address of the server should replace SERVER_IP

# NOTE: The client can only connect if the server is accepting clients, and all firewalls are turned off

# FILL IN THE SERVER'S IP ADDRESS BELOW

SERVER_IP = "192.168.1.6"
ADDR = (SERVER_IP, 7777)

# Create the client and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to the server...")
client.connect(ADDR)
print("Connection successful")
# The client will not run until the server sends a message
msg = client.recv(100)
print(msg.decode("utf-8"))

# This flag will only let the client enter one voice call
allow_connection = True
# 2048 bytes of data is sent at a time, frames_per_buffer * 2
MSG_LENGTH = 2048

# Will record audio indefinitely until told to terminate
# Recorded audio is sent to the server, and passed to the other client
# @pa is a PyAudio object
# @device_info has the user's audio device information
# @terminate is an event to terminate the voice call
def send_audio(pa, device_info, terminate):
    stream_in = pa.open(
        # Sampling frequency
        rate=44100,
        # Mono sound
        channels=2,
        # 16 bit format, each word is 2 bytes
        format=pyaudio.paInt16,
        input=True,
        # Default device will be used for recording
        input_device_index=device_info["defaultInputDevice"],
        frames_per_buffer=1024
    )
    print("Sending audio to the server...")
    # Will loop until the user signals for the program to terminate
    while not terminate.is_set():
        try:
            # Record audio and send it to the server
            client.send(stream_in.read(stream_in._frames_per_buffer))
        except socket.error:
            print("AUDIO SEND ERORR")
            terminate.set()
            break
    # End audio recording and deallocate audio resources
    # Disconnect from the audio server
    print("Ending Connection with Server")
    client.close()
    stream_in.stop_stream()
    stream_in.close()
    print("Audio Recording Finished")

# Will play audio sent from the other client
# @pa is a PyAudio object
# @device_info has the user's audio device information
# @terminate is an event to terminate the voice call
def receive_audio(pa, device_info, terminate):
    stream_out = pa.open(
        # Set the sample format and length
        format=pyaudio.paInt16,
        channels=2,
        # Set the sampling rate
        rate=44100,
        output=True,
        # Play to the user's default output device
        output_device_index=device_info["defaultOutputDevice"],
        # Set the buffer length to 1024
        frames_per_buffer=1024
    )
    print("Receiving audio from the server...")
    # Will loop until the server or client disconnects
    while not terminate.is_set():
        # Play the audio sent by the server
        try:
            stream_out.write(client.recv(MSG_LENGTH))
        except socket.error:
            print("AUDIO RECEIVE ERROR")
            terminate.set()
            break
    # End audio playback and deallocate audio resources
    stream_out.stop_stream()
    stream_out.close()
    print("Audio Playback Finished")

# Waits for user input, then sets terminate to true
# @terminate is an event shared between each thread to end the voice call
def user_input(terminate):
    # Wait 2 seconds
    time.sleep(2)
    # Request user signal to terminate
    print("Voice call succesfully created")
    input("At any point press enter to leave the voice call ")
    # Set terminate to true
    terminate.set()

# This function is only allowed to run once, this is moderated by the bool, connected
# The start function will wait until there is another client to voice call with
def start():
    global allow_connection
    if (allow_connection):
        # This function will only run once
        allow_connection = False
        print("Waiting for a response from the server...")
        # The voice call cannot be started until the second client connects
        # The server will know when this happens
        # When disconnected from the server, the client will no longer try to make a voice call
        connected = True
        msg = client.recv(100)
        msg = msg.decode("utf-8")
        if (msg != "DISCONNECTED"):
            print(msg)
            connected = False
            # Initiate a PyAudio object
            pa = pyaudio.PyAudio()
            # Save the information of the user's default audio devices
            device_info = pa.get_default_host_api_info()
            # Event which tells every thread to end
            terminate = threading.Event()
            # Create three threads
            # First thread thread sends recorded audio to the server intended for the other client
            # Second thread plays audio from the server passed by the other client
            # Third thread will tell all threads to terminate when given input
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Record
                executor.submit(send_audio, pa, device_info, terminate)
                # Play
                executor.submit(receive_audio, pa, device_info, terminate)
                # Terminate
                executor.submit(user_input, terminate)
            pa.terminate()
        else:
            print("Disconnected from the server, a voice call couldn't be made")

if __name__ == '__main__':
	if (SERVER_IP == ""):
		print("Please add the server's IP Address in the code for this program to work")
	else:
		start()
