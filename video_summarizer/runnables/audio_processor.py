from langchain.schema.runnable import Runnable
import uuid
import subprocess
from ..common import VideoDescriptor, global_console
from ..helpers import remove_file

class AudioProcessorRunnable(Runnable):

    def invoke(self, input: VideoDescriptor, *args) -> VideoDescriptor:
        global_console.log("Processing audio")
        input.audio_file = self.process_audio(input.audio_file)
        return input

    @staticmethod
    def process_audio(file_path) -> str:
        command = "ffmpeg \
                    -i {input_file} \
                    -ar 16000 \
                    -ac 1 \
                    -map 0:a: \
                    {output_file}"

        file_id = uuid.uuid4()
        output_file = f"output/{file_id}.mp3"

        subprocess.call(
            command.format(input_file=file_path, output_file=output_file),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

        remove_file(file_path)
        return output_file
