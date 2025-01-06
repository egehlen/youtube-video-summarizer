from langchain.schema.runnable import RunnableSequence
from .helpers import validate_url
from .runnables.audio_processor import AudioProcessorRunnable
from .runnables.display_output import DisplayOutputRunnable
from .runnables.downloader import DownloaderRunnable
from .runnables.summarizer import SummarizerRunnable
from .runnables.transcriber import TranscriberRunnable

def video_summarizer():
    url = "https://youtube.com/shorts/StysjXb9isQ?si=ikC1aTZWv3eu_tiL" #input("Video URL: ")

    if not validate_url(url):
        print("Invalid url.")
    else:
        pipeline = DownloaderRunnable() | AudioProcessorRunnable() | TranscriberRunnable() | SummarizerRunnable() | DisplayOutputRunnable()
        pipeline.invoke(input=url)

if __name__ == "__main__":
    video_summarizer()