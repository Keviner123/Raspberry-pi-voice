import pvporcupine

# AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
access_key = "KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA=="

handle = pvporcupine.create(
    access_key=access_key,
    keyword_paths=['robot_en_raspberry-pi_v2_1_0.ppn'])