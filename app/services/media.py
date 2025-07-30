import os

import librosa
import soundfile as sf
from moviepy import AudioFileClip, VideoFileClip

from .transcriber import Transcriber
from models.enums import Extension


class Audio(AudioFileClip):

    def __init__(self, filepath: str):
        if os.path.exists(filepath) & os.path.isfile(filepath):
            self.filepath = filepath
            super().__init__(filename=filepath)
        else:
            raise FileNotFoundError("The file does not exist")

    @property
    def __convert_to_wav_format(self) -> str:
        y, sr = librosa.load(self.filepath, sr=None)
        output = os.path.splitext(os.path.basename(self.filepath))[0] + Extension.WAV.value
        path = os.path.join("temp", output)
        sf.write(path, y, sr)
        return path

    def transcribe_file(self):
        wav = self.__convert_to_wav_format
        return Transcriber(wav).transcribe()


class Video(VideoFileClip):

    def __init__(self, filepath: str):
        if os.path.exists(filepath) & os.path.isfile(filepath):
            self.filepath = filepath
            super().__init__(filename=filepath)
        else:
            raise FileNotFoundError("The file does not exist")

    @property
    def __extract_audio(self) -> str:
        name, _ = os.path.splitext(os.path.basename(self.filepath))
        output_path = os.path.join("temp", name + Extension.WAV.value)
        self.audio.write_audiofile(output_path)
        return output_path

    def transcribe_file(self):
        wav = self.__extract_audio
        return Transcriber(wav).transcribe()
