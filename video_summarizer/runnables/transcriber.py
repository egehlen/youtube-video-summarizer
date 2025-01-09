from langchain.schema.runnable import Runnable
from dotenv import load_dotenv
import os
from groq import Groq
from ..helpers import suppress_stdout
from ..common import global_console, VideoDescriptor

load_dotenv()

class TranscriberRunnable(Runnable):

    def __init__(self):
        self.llm_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def invoke(self, input: VideoDescriptor, *args) -> VideoDescriptor:
        global_console.log("Transcribing")
        self.transcribe_audio(input)
        return input

    def transcribe_audio(self, descriptor: VideoDescriptor) -> None:

        with suppress_stdout():

            with open(descriptor.processed_audio_file, "rb") as file:

                response = self.llm_client.audio.transcriptions.create(
                    file=(descriptor.processed_audio_file, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    temperature=0.0
                )

                descriptor.transcription = response.text