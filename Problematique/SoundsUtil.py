import pyaudio
import traceback

def playSound(wave_stream):
    audio = pyaudio.PyAudio()
    chunk = 1024
    stream = audio.open(format=audio.get_format_from_width(wave_stream.getsampwidth()),
                        channels=wave_stream.getnchannels(),
                        rate=wave_stream.getframerate(),
                        output=True)
    data = wave_stream.readframes(chunk)
    # Playback
    while data:
        stream.write(data)
        data = wave_stream.readframes(chunk)

    wave_stream.rewind()
    stream.stop_stream()
    stream.close()
    audio.terminate()


def recordSound(wave_stream, file_name):
    try:
        raise FutureWarning('Base Excpetion: Function not yet implemented...')
    except FutureWarning:
        traceback.print_exc()

