from langchain.schema.runnable import Runnable
from dotenv import load_dotenv
import os
from groq import Groq
from ..helpers import suppress_stdout

load_dotenv()

class TranscriberRunnable(Runnable):

    def __init__(self):
        self.llm_client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def invoke(self, input, *args) -> str:
        return self.transcribe_audio(input)

    def transcribe_audio(self, file_path) -> str:
        with suppress_stdout():
            with open(file_path, "rb") as file:
                response = self.llm_client.audio.transcriptions.create(
                    file=(file_path, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    temperature=0.0
                )

                return response.text