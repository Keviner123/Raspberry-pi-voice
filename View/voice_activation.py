import audioop
import math
import threading
import time
import struct
import wave
import pvporcupine
import pyaudio

from BLL.SoundFilePlayer import SoundFilePlayer

class VoiceActivation:
    def __init__(self, activation_sound: str, access_key: str) -> None:
        self.sound_file_player_controller = SoundFilePlayer()
        self.activation_sound = activation_sound
        self.access_key = access_key

        self.wait_for_hotwords()
    # def Answer(self):
    #     self.sound_file_player_controller.PlayMp3(self.activationSound)

    #     # Set the silence threshold value (in dB)
    #     THRESHOLD = 60

    #     # Set the chunk size and recording duration
    #     CHUNK_SIZE = 1024
    #     RECORD_DURATION = 10  # in seconds

    #     # Set the PyAudio parameters
    #     FORMAT = pyaudio.paInt16
    #     CHANNELS = 1
    #     RATE = 44100

    #     # Create the PyAudio object
    #     audio = pyaudio.PyAudio()

    #     # Open the default input device for recording
    #     stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    #     # Initialize variables for the output file and the silence counter
    #     output_file = wave.open('output.wav', 'wb')
    #     output_file.setnchannels(1)
    #     output_file.setsampwidth(audio.get_sample_size(FORMAT))
    #     output_file.setframerate(RATE)

    #     silence_counter = 0

    #     # Record audio until there is silence
    #     while silence_counter < 50:  # adjust this value to set the minimum silence duration in frames
    #         # Read a chunk of audio data from the input stream
    #         data = stream.read(CHUNK_SIZE)

    #         # Compute the RMS amplitude of the audio data (in dB)
    #         rms = audioop.rms(data, 2)
    #         db = 20 * math.log10(rms) if rms > 0 else 0

    #         # Write the audio data to the output file
    #         output_file.writeframes(data)

    #         # Check if the audio is silent
    #         if db < THRESHOLD:
    #             silence_counter += 1
    #         else:
    #             silence_counter = 0

    #         # Log the dB value
    #         print(f"dB: {db:.2f}")


    #     # Close the output file and the input stream
    #     output_file.close()
    #     stream.stop_stream()
    #     stream.close()
    #     audio.terminate()

    def wait_for_hotwords(self):
        porcupine = None
        python_audio = None
        audio_stream = None

        porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=['art-o-ditto_en_raspberry-pi_v2_1_0.ppn', 'r-too-d-too_en_raspberry-pi_v2_1_0.ppn'])
        python_audio = pyaudio.PyAudio()

        audio_stream = python_audio.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=1024
        )

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("keyword detected")

                # threading.Thread(target=self.Answer).start()


        # finally:
        #     if porcupine is not None:
        #         porcupine.delete()

        #     if audio_stream is not None:
        #         audio_stream.close()
        #     if pa is not None:
        #         pa.terminate()
