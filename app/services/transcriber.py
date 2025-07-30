import os

from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)


class Transcriber(DeepgramClient):

    def __init__(self, filepath: str, *, options: PrerecordedOptions = None):
        load_dotenv()
        api_key = os.environ.get("DEEPGRAM_API_KEY")
        if api_key:
            super().__init__(api_key)
        else:
            raise EnvironmentError(
                "Environment variable 'undefined DEEPGRAM_API_KEY'")

        self.filepath = filepath
        self.options = PrerecordedOptions(model="nova-3", smart_format=True)
        self.payload: FileSource = {
            "buffer": self.__buffer_data
        }

    @property
    def __detect_file_extension(self) -> str:
        if os.path.isfile(self.filepath) & os.path.exists(self.filepath):
            _, ext = os.path.splitext(os.path.basename(self.filepath))
            return ext
        else:
            raise FileNotFoundError("The file does not exist")

    @property
    def __buffer_data(self) -> bytes:
        try:
            with open(self.filepath, "rb") as file:
                return file.read()
        except (FileNotFoundError, IOError) as error:
            raise error

    def transcribe(self):
        if self.__detect_file_extension == ".wav":
            response = self.listen.rest.v("1").transcribe_file(
                self.payload, self.options)
            name, _ = os.path.splitext(os.path.basename(self.filepath))
            path = os.path.join("generated", name + ".txt")
            transcript = response.to_dict()["results"]["channels"][0]["alternatives"][0]["transcript"]
            with open(path, "w") as file:
                file.write(transcript)
            return {
                "transcript": transcript,
                "filename": name + ".txt"
            }
        else:
            raise Exception("file with a format different from .wav")
