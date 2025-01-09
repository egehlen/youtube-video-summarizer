from langchain.schema.runnable import Runnable
import yt_dlp
import uuid
from ..helpers import suppress_stdout
from ..common import VideoDescriptor, global_console

class DownloaderRunnable(Runnable):

    def invoke(self, input: VideoDescriptor, *args) -> VideoDescriptor:
        global_console.log("Extracting audio")
        self.download_audio(input)
        return input

    @staticmethod
    def download_audio(descriptor: VideoDescriptor) -> None:

        with suppress_stdout():

            file_id = uuid.uuid4()
            file_path = f"video_summarizer/output/{file_id}.mp3"

            with yt_dlp.YoutubeDL({"extract_audio": True, "format": "bestaudio", "outtmpl": file_path}) as video:

                info_dict = video.extract_info(descriptor.url, download=False)
                video.download(descriptor.url)

                descriptor.title = info_dict["title"],
                descriptor.channel = info_dict["channel"],
                descriptor.raw_audio_file = file_path,
                descriptor.duration = info_dict["duration_string"],
                descriptor.categories = info_dict["categories"]

                if type(descriptor.title) is tuple or type(descriptor.title) is tuple[str]:
                    descriptor.title = "".join(descriptor.title)

                if type(descriptor.channel) is tuple or type(descriptor.channel) is tuple[str]:
                    descriptor.channel = "".join(descriptor.channel)

                if type(descriptor.raw_audio_file) is tuple or type(descriptor.raw_audio_file) is tuple[str]:
                    descriptor.raw_audio_file = "".join(descriptor.raw_audio_file)

                if type(descriptor.duration) is tuple or type(descriptor.duration) is tuple[str]:
                    descriptor.duration = "".join(descriptor.duration)