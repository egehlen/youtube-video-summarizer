from langchain.schema.runnable import Runnable
import yt_dlp
import uuid
from ..helpers import suppress_stdout
from ..common import VideoDescriptor, global_console

class DownloaderRunnable(Runnable):

    def invoke(self, input, *args) -> VideoDescriptor:
        global_console.log("Extracting audio")
        return self.download_audio(input)

    @staticmethod
    def download_audio(url) -> VideoDescriptor:
        with suppress_stdout():
            file_id = uuid.uuid4()
            file_path = f"output/{file_id}.mp3" 

            with yt_dlp.YoutubeDL({"extract_audio": True, "format": "bestaudio", "outtmpl": file_path}) as video:
                info_dict = video.extract_info(url, download=False)
                video.download(url)

                return VideoDescriptor(
                    info_dict["title"],
                    info_dict["channel"],
                    info_dict["webpage_url"],
                    file_path
                )