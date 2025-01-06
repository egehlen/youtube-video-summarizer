from langchain.schema.runnable import Runnable
import uuid
import subprocess
from ..common import VideoMetadata


class AudioProcessorRunnable(Runnable):
    def invoke(self, input: VideoMetadata, *args) -> str:
        audio_file_path = input.audio_file
        return self.process_audio(audio_file_path)

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

        return output_file
