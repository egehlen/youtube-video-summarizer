from langchain.schema.runnable import Runnable
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from ..helpers import suppress_stdout
from langchain_core.prompts import ChatPromptTemplate
from ..common import VideoSummary
import json
from langchain.schema.runnable import RunnableSequence

load_dotenv()

class SummarizerRunnable(Runnable):

    def __init__(self):
        self.llm_client = ChatGroq(
            model="llama-3.3-70b-versatile"
        )

    def invoke(self, input, *args) -> str:
        return self.summarize_content(input)

    def summarize_content(self, transcription) -> str:

        with suppress_stdout():

            base_path = os.path.dirname(__file__)
            file_path = os.path.abspath(os.path.join(base_path, "..", "system_prompt.md"))

            with open(file_path) as f: system_prompt = f.read()

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            chain = prompt | self.llm_client
            result = chain.invoke(
                {
                    "json_schema": json.dumps(VideoSummary.model_json_schema(), indent=2),
                    "output_language": "Brazilian Portuguese",
                    "input": transcription
                }
            )

            return result.content