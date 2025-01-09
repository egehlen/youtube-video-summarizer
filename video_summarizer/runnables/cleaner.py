from langchain.schema.runnable import Runnable
from ..common import VideoDescriptor
from ..helpers import remove_file

class CleanerRunnable(Runnable):

    def invoke(self, input: VideoDescriptor, *args) -> None:
        try:
            remove_file(input.raw_audio_file)
            remove_file(input.processed_audio_file)
        except:
            print(input)
            print("Something went wrong while removing the audio files :(")