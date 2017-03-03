from pathlib import Path

BASE_DIR = Path(__file__).parent
LICENSE_DIR = BASE_DIR.joinpath("licenses")
LICENSE_FILE = Path.cwd().joinpath('LICENSE')

from .cli import cli
from . import models
from . import utils
