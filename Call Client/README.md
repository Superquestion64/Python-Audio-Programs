# Join a Voice Call in Python
Call_Client.py will attempt to connect to a server using Python's socket library. When two clients connect to the same server a voice call is established between the two clients
- Call_Client.py should be run on the client computer, the client will attempt to connect to the server
- Once connected, the server will wait for another client to connect 
- When two clients are connected the server exchanges audio data between the clients, forming a voice call
- Multiple pairs of clients are able to connect to the server and form voice calls
- Call_Client.py is run by simply using: <br>
*'python Call_Client.py'* <br>

**Note:** This program is dependent on PyAudio and the IP address of the server **must** be provided in Call_Client.py. All firewalls should also be disabled