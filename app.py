import pyaudio
import wave

# Specify the audio file path
audio_file = "test_audio.wav"

# Open the audio file
wf = wave.open(audio_file, 'rb')

# Create a PyAudio object
p = pyaudio.PyAudio()

# Find the index of the Virtual Audio Cable (VAC) output device
vac_device_index = None
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if 'Virtual Audio Cable' in dev_info['name']:
        vac_device_index = i
        break

if vac_device_index is None:
    raise Exception("Virtual Audio Cable not found. Make sure VAC is installed and set up.")

# Open a stream to the virtual audio device
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                output_device_index=vac_device_index)

# Play the audio in chunks
chunk = 1024
data = wf.readframes(chunk)

while data:
    stream.write(data)
    data = wf.readframes(chunk)

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()

wf.close()
