from langchain.schema.runnable import Runnable
import yt_dlp
import uuid
from ..helpers import suppress_stdout
from ..common import VideoMetadata

class DownloaderRunnable(Runnable):

    def invoke(self, input, *args) -> VideoMetadata:
        return self.download_audio(input)

    @staticmethod
    def download_audio(url) -> VideoMetadata:
        with suppress_stdout():
            file_id = uuid.uuid4()
            file_path = f"output/{file_id}.mp3" 

            with yt_dlp.YoutubeDL({"extract_audio": True, "format": "bestaudio", "outtmpl": file_path}) as video:
                info_dict = video.extract_info(url, download=False)
                video.download(url)
                
                metadata = VideoMetadata(
                    title=info_dict["title"], 
                    channel=info_dict["channel"], 
                    url=info_dict["webpage_url"],
                    audio_file=file_path
                )
                
                return metadata