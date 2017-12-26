import re
from pathlib import Path

from notary.models import LICENSES as SUPPORTED_LICENSES


def guess_license(name):
    """Returns a list of classes that extend the :class:`License` abstract base class.
    :param name: If a string is sent, it checks if it's a substring of any of the supported
    licenses. If it is, all matches will be returned. Otherwise, all supported licenses
    are returned.
    """

    if not isinstance(name, str):
        return SUPPORTED_LICENSES
    else:
        name = name.lower()

    probable = []
    likely = []
    for cls in SUPPORTED_LICENSES:
        if name in cls.name.lower() or name in cls.__name__.lower():
            probable.append(cls)
        else:
            likely.append(cls)

    if probable:
        return probable

    return likely


def find_license_files(folder=None):
    """Returns a list of :class:`Path <Path>` objects representing existing LICENSE files
    in the specified directory or the current folder, if none was specified.
    :param folder: String or instance of :class:`Path`
    """
    if isinstance(folder, str):
        folder = Path(folder)

    if folder is None:
        folder = Path(".")

    rule = re.compile("(?i)license(\.[a-zA-Z]*)?")
    return [path for path in folder.glob("*") if path.is_file() and rule.match(path.name)]
