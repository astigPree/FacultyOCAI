import typing as tp


class AIMouth :
    """ This where the A.I. Speak """

    import pyttsx3
    # import logging
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="[%(lineno)d] [%(asctime)s] -- %(name)s  %(levelname)s: %(message)s",
    # logging.getLogger("pyttsx3").setLevel(logging.INFO)

    __speaker = pyttsx3.init()
    male_voice = None
    female_voice = None

    def __init__(self, rate=None, volume=1.0, gender='male') :
        self.male_voice = self.__speaker.getProperty('voices')[0].id
        self.female_voice = self.__speaker.getProperty('voices')[1].id

        if rate :
            self.__speaker.setProperty('rate', rate)
        self.__speaker.setProperty('volume', volume)
        if gender == 'male' :
            self.__speaker.setProperty('voice', self.male_voice)
        else :
            self.__speaker.setProperty('voice', self.female_voice)

    # -----> Speaker Activities
    def talk(self, sentence: str) :
        print(f'Speaking : {sentence}')
        self.__speaker.say(sentence)
        self.__speaker.runAndWait()


class AIEar :
    """ This where the A.I. Listen """

    KHZT = 16_000  # 16_000 'If increasing the buffer size doesn't resolve the issue, you can try reducing the sample rate (sampling frequency) when opening the audio stream. Lowering the sample rate decreases the amount of data captured per second, which can help prevent input overflow.'
    frames_per_buffer = 8_192  # 8192 'One way to mitigate input overflow issues is to increase the size of the input buffer (frames_per_buffer) when opening the audio stream. A larger buffer can handle more audio data and reduce the chances of overflow. For example, you can set frames_per_buffer to a larger value, such as 8192 or 16384.'
    stream_read = int(frames_per_buffer / 2)
    channel = 1

    maximumRecordLoop = 50

    def __init__(self) :
        from vosk import Model, KaldiRecognizer
        from pyaudio import paInt16, PyAudio

        self.fil_model = Model(model_name="vosk-model-tl-ph-generic-0.6")
        self.fil_recognizer = KaldiRecognizer(self.fil_model, self.KHZT)

        self.mic = PyAudio()
        self.stream = self.mic.open(format=paInt16, rate=16000, channels=self.channel, input=True,
                                    frames_per_buffer=self.frames_per_buffer)

    def closeMicrophone(self) :
        if self.stream and self.mic :
            self.stream.close()
            self.mic.terminate()

    def captureVoice(self, waiting_time=None , holder = None) -> tp.Union[str, None] :
        """This functions might return empty string and to not get stuck it has a maximum loop to read stream"""
        self.stream.start_stream()
        text = ""

        for _ in range(self.maximumRecordLoop if not waiting_time else waiting_time) :
            data = self.stream.read(num_frames=self.stream_read, exception_on_overflow=False)
            if holder: # Use to stop the recording
                if holder.stop_all_running:
                    return None
            if self.fil_recognizer.AcceptWaveform(data) :
                text = self.fil_recognizer.Result()[14 :-3]
                print(f"Filipino Text : {text}")
                if len(text) : break

        if len(text) :
            self.stream.stop_stream()
            return text.replace("<unk>", "")
        else :
            print("[!] OSError: [Errno -9981] Input overflowed")
            self.stream.stop_stream()
            return None


if __name__ == "__main__" :
    pass
