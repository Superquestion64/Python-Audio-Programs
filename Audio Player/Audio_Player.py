# Created by Charles Vega
# Last Modified December 16, 2021
# This program will play a wav file given by the user
# The wav file needs to be located in the same directory as this program
# Users must input the file name
# Dependencies: PyAudio, wave

import pyaudio
import wave

def play(file_name):
    # Make sure the user is reading a wav file
    if (file_name[-4:] != ".wav"):
        wf = wave.open(file_name + ".wav", "rb")
    else:
        wf = wave.open(file_name, "rb")
    pa = pyaudio.PyAudio()
    # Save the information of the user's default devices
    device_info = pa.get_default_host_api_info()
    stream_out = pa.open(
        # Set the sample format and length
        format = pa.get_format_from_width(wf.getsampwidth()),
        # Get the number of output channels
        channels = wf.getnchannels(),
        # Get the sampling rate
        rate = wf.getframerate(),
        output = True,
        # Play to the user's default output device
        output_device_index = device_info["defaultOutputDevice"],
        # Set the buffer length to 1024
        frames_per_buffer = 1024
    )
    data = wf.readframes(1024)
    # Will loop until there is no more remaining audio
    print("Playing Audio...")
    while len(data) > 0:
        # Play the audio file
        stream_out.write(data)
        data = wf.readframes(1024)
    # End audio playback and deallocate audio resources
    stream_out.stop_stream()
    stream_out.close()
    pa.terminate()
	
if __name__ == "__main__":
	play(input("Enter the name of the audio file: "))
