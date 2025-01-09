from typing import List
from pydantic import BaseModel
from rich.console import Console

global_console = Console()

supported_languages = {
    "pt-br" : "Brazilian Portuguese",
    "en" : "English"
}

class VideoDescriptor:
    title: str
    channel: str
    url: str
    raw_audio_file: str
    processed_audio_file: str
    duration: str
    categories: List[str]
    summary: str
    highlights: List[str]
    steps: List[str]
    transcription: str
    target_language: str

    def __init__(self, url, language):
        self.url = url
        self.target_language = language

class VideoSummary(BaseModel):
    summary: str
    highlights: List[str]
    steps: List[str]

class VideoMetadata(BaseModel):
    title: str
    categories: str