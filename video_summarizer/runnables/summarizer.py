from langchain.schema.runnable import Runnable
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from ..helpers import suppress_stdout
from langchain_core.prompts import ChatPromptTemplate
from ..common import VideoSummary, global_console, VideoDescriptor, VideoMetadata
import json

load_dotenv()

class SummarizerRunnable(Runnable):

    def __init__(self):
        self.llm_client = ChatGroq(
            model_name="llama-3.3-70b-versatile"
        )

    def invoke(self, input: VideoDescriptor, *args) -> VideoDescriptor:
        global_console.log("Generating summary")
        self.summarize_content(input)
        self.translate_metadata(input)
        return input

    def summarize_content(self, descriptor: VideoDescriptor) -> None:

        with suppress_stdout():

            base_path = os.path.dirname(__file__)
            file_path = os.path.abspath(os.path.join(base_path, "..", "prompts/summarization.md"))

            with open(file_path) as f:
                system_prompt = f.read()

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            chain = prompt | self.llm_client
            result = chain.invoke(
                {
                    "json_schema": json.dumps(VideoSummary.model_json_schema(), indent=2),
                    "output_language": descriptor.target_language,
                    "input": descriptor.transcription
                }
            )

            sanitized_content = result.content \
                .replace("\n", "") \
                .replace("  ", " ") \
                .replace("```", "") \
                .replace("json{", "{")

            summary_object = VideoSummary.model_validate_json(sanitized_content, strict=False)
            descriptor.summary = summary_object.summary
            descriptor.highlights = summary_object.highlights
            descriptor.steps = summary_object.steps

    def translate_metadata(self, descriptor: VideoDescriptor) -> None:

        with suppress_stdout():

            base_path = os.path.dirname(__file__)
            file_path = os.path.abspath(os.path.join(base_path, "..", "prompts/metadata_translation.md"))

            with open(file_path) as f:
                system_prompt = f.read()

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])

            chain = prompt | self.llm_client
            result = chain.invoke(
                {
                    "json_schema": json.dumps(VideoMetadata.model_json_schema(), indent=2),
                    "output_language": descriptor.target_language,
                    "input": {
                        "title": descriptor.title,
                        "categories": descriptor.categories
                    }
                }
            )

            sanitized_content = result.content \
                .replace("\n", "") \
                .replace("  ", " ") \
                .replace("```", "") \
                .replace("json{", "{")

            metadata_object = VideoMetadata.model_validate_json(sanitized_content, strict=False)
            descriptor.title = metadata_object.title
            descriptor.categories = metadata_object.categories