from langchain.schema.runnable import Runnable
import uuid
import subprocess
from ..common import VideoDescriptor, global_console

class AudioProcessorRunnable(Runnable):

    def invoke(self, input: VideoDescriptor, *args) -> VideoDescriptor:
        global_console.log("Processing audio")
        self.process_audio(input)
        return input

    @staticmethod
    def process_audio(descriptor: VideoDescriptor) -> None:
        command = "ffmpeg \
                    -i {input_file} \
                    -ar 16000 \
                    -ac 1 \
                    -map 0:a: \
                    {output_file}"

        file_id = uuid.uuid4()
        output_file = f"output/{file_id}.mp3"

        subprocess.call(
            command.format(input_file=descriptor.raw_audio_file, output_file=output_file),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

        descriptor.processed_audio_file = output_file
