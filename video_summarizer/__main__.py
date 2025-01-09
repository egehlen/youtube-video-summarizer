from rich.prompt import Prompt
from video_summarizer.runnables.cleaner import CleanerRunnable
from .helpers import validate_url, get_target_language
from .common import global_console, VideoDescriptor
from .runnables.audio_processor import AudioProcessorRunnable
from .runnables.display_output import DisplayOutputRunnable
from .runnables.downloader import DownloaderRunnable
from .runnables.summarizer import SummarizerRunnable
from .runnables.transcriber import TranscriberRunnable

def video_summarizer():
    url = Prompt.ask("Video URL")

    if not validate_url(url):
        print("Invalid url.")
    else:
        target_language = get_target_language()
        descriptor = VideoDescriptor(url, target_language)

        pipeline = \
            DownloaderRunnable() \
            | AudioProcessorRunnable() \
            | TranscriberRunnable() \
            | SummarizerRunnable() \
            | DisplayOutputRunnable() \
            | CleanerRunnable()

        with global_console.status("[bold green]Processing summarization...") as status:
            pipeline.invoke(input=descriptor)

if __name__ == "__main__":
    video_summarizer()