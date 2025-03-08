import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    print("Audio Devices:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        print(f"{i+1}. {device_name}")

    p.terminate()

def get_first_input_device():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        if device_info.get('maxInputChannels') > 0:
            p.terminate()
            return device_name

    p.terminate()

if __name__ == "__main__":
    print(get_first_input_device())