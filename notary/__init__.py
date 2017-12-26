from pathlib import Path

BASE_DIR = Path(__file__).parent
LICENSE_DIR = BASE_DIR.joinpath("licenses")
LICENSE_FILE = Path(".").joinpath("LICENSE")

from . import cli
from . import models
from . import utils
