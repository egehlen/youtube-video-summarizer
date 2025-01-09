from video_summarizer.common import supported_languages
from contextlib import contextmanager
import sys
import os
from urllib.parse import urlparse
import argparse

argument_parser = argparse.ArgumentParser()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

def remove_file(file_path: str) -> None:
    os.remove(file_path)

def get_target_language() -> str:
    default_language = supported_languages["en"]

    try:
        argument_parser.add_argument("--translate-to")
        args = argument_parser.parse_args()
        return supported_languages[args.language] or default_language
    except:
        print("There was an error retrieving the argument \"--translate-to\"")
        return default_language