# Created by Charles Vega
# Last Modified December 16, 2021
# This program will record audio from a user's default input device
# The recorded audio gets stored in a wav file within this program's directory
# Users must input the amount of seconds to be recorded and the desired file name
# Dependencies: PyAudio, wave

import pyaudio
import wave

def record(seconds):
    pa = pyaudio.PyAudio()
    # Save the information of the user's default devices
    device_info = pa.get_default_host_api_info()
    stream_in = pa.open(
        # Sampling frequency
        rate = 44100,
        # Mono sound
        channels = 1,
        # 16 bit format, each word is 2 bytes
        format = pyaudio.paInt16,
        input = True,
        # Default device will be used for recording
        input_device_index = device_info["defaultInputDevice"],
        frames_per_buffer = 1024
    )
    print("Recording in progress...")
    # Begin audio recording
    input_audio = stream_in.read(seconds * 44100)
    # End audio recording and deallocate audio resources
    stream_in.stop_stream()
    stream_in.close()
    pa.terminate()

    # Wav file creation
    file_name = input("Name your file: ")
    # Make sure the user creates a wav file
    if (file_name[-4:] != ".wav"):
        wf = wave.open(file_name + ".wav", "wb")
    else:
        wf = wave.open(file_name, "wb")
    # Mono sound
    wf.setnchannels(1)
    # 2 byte words
    wf.setsampwidth(2)
    wf.setframerate(44100)
    # Create the wav file with the above properties and input audio
    wf.writeframes(input_audio)
    wf.close()
	
if __name__ == '__main__':
	record(int(input("Seconds to be recorded: ")))
