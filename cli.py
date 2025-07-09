"""
Tiny helper so reviewers can test quickly:

$ python cli.py "Write a haiku"
or
$ python cli.py "Explain AI" --nostream
"""

import requests, sys

API_URL = "http://localhost:8000"


def ask(prompt: str, stream: bool = True):
    """Send a prompt to /generate and print the response."""
    resp = requests.post(f"{API_URL}/generate",
                         json={"prompt": prompt},
                         stream=stream)
    if not stream:
        print(resp.json())
        return

    for chunk in resp.iter_content(chunk_size=None):
        sys.stdout.write(chunk.decode())
        sys.stdout.flush()
    print()  # final newline

if __name__ == "__main__":
    input = input()
    ask(input)
