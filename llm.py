from dotenv import load_dotenv
import os
from helpers import Helpers
from groq import Groq
import json
from common import VideoSummary

load_dotenv()

class LLMService:

    def __init__(self, progress):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.progress = progress
        self.helpers = Helpers()

    def get_content(self, file_path):
        transcription = self.transcribe_audio(file_path)
        return self.summarize_content(transcription)

    def transcribe_audio(self, file_path):
        print("Transcribing audio :: Step 3/4")

        with self.helpers.suppress_stdout():
            with open(file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(file_path, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    temperature=0.0
                )
                return transcription.text
            
    def summarize_content(self, transcription):
        print("Summarizing content :: Step 4/4")

        with self.helpers.suppress_stdout():
            with open('system_prompt.md') as f: system_prompt = f.read()

            system_prompt = system_prompt.format(
                json_schema=json.dumps(VideoSummary.model_json_schema(), indent=2),
                output_language='Brazilian Portuguese'
            )

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": transcription,
                    }
                ],
                temperature=0,
                response_format={"type": "json_object"},
                model="llama3-70b-8192",
                stream=False,
            )
            return chat_completion.choices[0].message.content