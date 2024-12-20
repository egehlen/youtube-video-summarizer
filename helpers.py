from contextlib import contextmanager
import sys
import os
import json
from urllib.parse import urlparse

class Helpers:

    @contextmanager
    def suppress_stdout(self):
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:  
                yield
            finally:
                sys.stdout = old_stdout

    def validate_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except AttributeError:
            return False
        
    def display_output(self, info, content):
        try:
            content_json = json.loads(content)
            term_size = os.get_terminal_size()
            
            print('-' * term_size.columns)
            print()
            print(' # Informações:')
            print(f" Título: {info.title}")
            print(f" Canal: {info.channel}")
            print(f" URL: {info.url}")
            print()
            print('-' * term_size.columns)
            print()
            print(" # Resumo:")
            print()
            print(content_json['summary'])
            print()
            print('-' * term_size.columns)
            print()
            print(" # Destaques:")
            print()

            for highlight in content_json['highlights']:
                print(f"   * {highlight}")

            print()
            print('-' * term_size.columns)
        except:
            print("An error ocurred.")