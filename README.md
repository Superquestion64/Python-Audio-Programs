# PyAudio: Audio Programs in Python
Listed are several folders containing Python programs that utlize the default audio devices of a user
- Audio Player: Can play .wav files to the user's default audio device
- Audio Recorder: Records audio from the user's default input device and saves it as a .wav file
- Call Client: Will try to connect to a server which connects the client with another in a voice call
- Call Server: Connects clients with each other forming wireless voice calls
- **Note** A voice call can only be made when one computer is active as the server, and two clients connect to the server. Ideally three computers should be used, but nothing prevents one user from acting as a server and two clients
- Sync Audio: Can be used as a program to test if PyAudio is working correctly

## Dependencies
All of the programs are dependent on PyAudio, detailed installation is provided below

## PyAudio Installation
PyAudio cannot be installed using 'pip install PyAudio' for modern python versions as it has not been updated.
To install PyAudio the proper wheel file must be manually downloaded for your computer architecture and python version
- The wheel file can be found at https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Once the correct wheel file is downloaded, simply run: <br> <br>
**pip install c:\Users\username\Downloads\wheel_file_name**

