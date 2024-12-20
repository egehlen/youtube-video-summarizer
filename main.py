from helpers import Helpers
from file import FileService
from llm import LLMService

def main():
    helpers = Helpers()
    url = "https://youtube.com/shorts/StysjXb9isQ?si=ikC1aTZWv3eu_tiL" #input("Video URL: ")

    if helpers.validate_url(url):
        fileService = FileService(None)
        llmService = LLMService(None)

        metadata = fileService.get_video_metadata(url)
        content = llmService.get_content(metadata.audio_file)
        fileService.remove_file(metadata.audio_file)
        helpers.display_output(metadata, content)
    else:
        print("Invalid url.")

main()