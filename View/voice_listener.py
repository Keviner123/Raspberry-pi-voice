import audioop
import math
import wave
import pyaudio

from BLL.google_speech_to_text_client import GoogleSpeechToTextClient


class VoiceListener:
    def __init__(self) -> None:
        self.googlespeechtotextclient = GoogleSpeechToTextClient("login.json")

    def start_recording(self):

        # Set the silence threshold value (in dB)
        THRESHOLD = 40

        # Set the chunk size and recording duration
        CHUNK_SIZE = 1024
        RECORD_DURATION = 10  # in seconds

        # Set the PyAudio parameters
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        # Create the PyAudio object
        audio = pyaudio.PyAudio()

        # Open the default input device for recording
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

        # Initialize variables for the output file and the silence counter
        output_file = wave.open('output.wav', 'wb')
        output_file.setnchannels(1)
        output_file.setsampwidth(audio.get_sample_size(FORMAT))
        output_file.setframerate(RATE)

        silence_counter = 0

        # Record audio until there is silence
        while silence_counter < 50:  # adjust this value to set the minimum silence duration in frames
            # Read a chunk of audio data from the input stream
            data = stream.read(CHUNK_SIZE)

            # Compute the RMS amplitude of the audio data (in dB)
            rms = audioop.rms(data, 2)
            db = 20 * math.log10(rms) if rms > 0 else 0

            # Write the audio data to the output file
            output_file.writeframes(data)

            # Check if the audio is silent
            if db < THRESHOLD:
                silence_counter += 1
            else:
                silence_counter = 0

            # Log the dB value
            print(f"dB: {db:.2f}")


        # Close the output file and the input stream
        output_file.close()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        return True
    def transcribe(self) -> str:
        return self.googlespeechtotextclient.transcribe_audio_file("output.wav")