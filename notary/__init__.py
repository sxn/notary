from pathlib import Path

from .cli import cli

BASE_DIR = Path(__file__).parent

if __name__ == '__main__':
    cli()
