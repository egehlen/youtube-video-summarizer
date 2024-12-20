from helpers import Helpers
import uuid
import yt_dlp
import subprocess
import os
from common import VideoMetadata

class FileService:

    def __init__(self, progress):
        self.helpers = Helpers()
        self.progress = progress

    def get_video_metadata(self, url):
        metadata, raw_audio_file = self.download_audio(url)
        processed_audio_file = self.preprocess_file(raw_audio_file)
        metadata.audio_file = processed_audio_file
        self.remove_file(raw_audio_file)
        return metadata

    def download_audio(self, url):
        print("Extracting audio :: Step 1/4")

        with self.helpers.suppress_stdout():
            file_id = uuid.uuid4()
            file_path = 'output/{}.mp3'.format(file_id) 

            with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': file_path}) as video:
                info_dict = video.extract_info(url, download=False)
                video.download(url)
                
                metadata = VideoMetadata(
                    title=info_dict['title'], 
                    channel=info_dict['channel'], 
                    url=info_dict['webpage_url'],
                    audio_file=file_path
                )
                
                return metadata, file_path
            
    def preprocess_file(self, file_path):
        print("Processing audio :: Step 2/4")

        # Perform a downsampling of the audio
        command = "ffmpeg \
                    -i {input_file} \
                    -ar 16000 \
                    -ac 1 \
                    -map 0:a: \
                    {output_file}"
        
        file_id = uuid.uuid4()
        output_file = 'output/{}.mp3'.format(file_id)
        subprocess.call(
            command.format(input_file=file_path, output_file=output_file),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        return output_file

    def remove_file(self, file_path):
        os.remove(file_path)