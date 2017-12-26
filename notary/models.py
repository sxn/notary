from abc import ABC, abstractmethod

from notary import LICENSE_DIR


class License(ABC):
    """An abstract base class for all licenses.

    :param author: Name of the entity granting the license (if it needs one).
    :param year: The year to be written to the license (if it needs one).

    Any class that extends this one needs to provide the following params:
    :param name: The human-readable name of the license.
    :param path: Instance of :class:`pathlib.Path <pathlib.Path>` representing the location
    of the license file.

    Classes that allow setting a author or a year also additionally need to specify:
    :attr author_placeholder: What (exactly) in the license file should be replaced
    by :param:`author`
    :attr year_placeholder: What (exactly) in the license file should be replaced
    by :param:`year`
    """

    author_placeholder = None
    year_placeholder = None

    def __init__(self, author=None, year=None):
        self._author = author
        self._year = year

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def path(self):
        pass

    @property
    def author(self):
        return self._author

    @property
    def year(self):
        return self._year

    @property
    def content(self):
        with self.path.open("r") as f:
            content = f.read()

        if self.author_placeholder:
            content = content.replace(self.author_placeholder, self.author, 1)

        if self.year_placeholder:
            content = content.replace(self.year_placeholder, str(self.year), 1)

        return content


class AGPL3(License):
    name = "GNU Affero General Public License version 3"
    path = LICENSE_DIR.joinpath("agpl-3.0.md")


class Apache(License):
    name = "Apache License 2.0"
    path = LICENSE_DIR.joinpath("apache-2.0.md")
    author_placeholder = "[name of copyright owner]"
    year_placeholder = "[yyyy]"


class GPL3(License):
    path = LICENSE_DIR.joinpath("gpl-3.0.md")
    name = "GNU General Public License v3.0"


class LGPL3(License):
    name = "GNU Lesser General Public License v3.0"
    path = LICENSE_DIR.joinpath("lgpl-3.0.md")


class MIT(License):
    name = "MIT License"
    path = LICENSE_DIR.joinpath("mit.md")
    author_placeholder = "[fullname]"
    year_placeholder = "[year]"


class MPL(License):
    name = "Mozilla Public License Version 2.0"
    path = LICENSE_DIR.joinpath("mpl-2.0.md")


class Unlicense(License):
    name = "The Unlicense"
    path = LICENSE_DIR.joinpath("unlicense.md")


LICENSES = [
    AGPL3,
    Apache,
    GPL3,
    LGPL3,
    MIT,
    MPL,
    Unlicense,
]
