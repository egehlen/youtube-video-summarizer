from rich.box import SIMPLE

from .helpers import validate_url
from .common import global_console
from .runnables.audio_processor import AudioProcessorRunnable
from .runnables.display_output import DisplayOutputRunnable
from .runnables.downloader import DownloaderRunnable
from .runnables.summarizer import SummarizerRunnable
from .runnables.transcriber import TranscriberRunnable

def video_summarizer():
    global_console.print("Video URL: ", style="bold yellow")
    #url = input()
    url = "https://youtube.com/shorts/StysjXb9isQ?si=ikC1aTZWv3eu_tiL"
    print(url)

    if not validate_url(url):
        print("Invalid url.")
    else:
        pipeline = DownloaderRunnable() | AudioProcessorRunnable() | TranscriberRunnable() | SummarizerRunnable() | DisplayOutputRunnable()

        with global_console.status("[bold green]Processing summarization...") as status:
            pipeline.invoke(input=url)

def test():
    from rich.console import Console
    from rich.table import Table

    table = Table(box=SIMPLE)

    table.add_column("Released", justify="left", style="cyan")
    table.add_row("Dec 16, 2016 Rogue One: A Star Wars Story $1,332,439,889 Dec 16, 2016 Rogue One: A Star Wars Story $1,332,439,889")

    console = Console()
    console.print(table)

if __name__ == "__main__":
    video_summarizer()