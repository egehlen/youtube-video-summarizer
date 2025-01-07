from typing import List
from pydantic import BaseModel
from rich.console import Console

global_console = Console()

class VideoDescriptor:
    title: str
    channel: str
    url: str
    audio_file: str
    summary: str
    highlights: List[str]
    steps: List[str]
    transcription: str

    def __init__(self, title, channel, url, file):
        self.title = title
        self.channel = channel
        self.url = url
        self.audio_file = file

class VideoSummary(BaseModel):
    summary: str
    highlights: List[str]
    steps: List[str]
    transcription: str