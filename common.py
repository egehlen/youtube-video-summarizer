from typing import List
from pydantic import BaseModel

class VideoMetadata:
    def __init__(self, title, channel, url, audio_file):
        self.title = title
        self.channel = channel
        self.url = url
        self.audio_file = audio_file

class VideoSummary(BaseModel):
    summary: str
    highlights: List[str]