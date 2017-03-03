import datetime
from abc import ABC, abstractmethod

from notary import LICENSE_DIR


class License(ABC):
    """An abstract base class for all licenses.

    :param licensor: Name of the entity granting the license (if it needs one).
    :param year: The year to be written to the license (if it needs one).

    Any class that extends this one needs to provide the following params:
    :param name: The human-readable name of the license.
    :param path: Instance of :class:`pathlib.Path <pathlib.Path>` representing the location
    of the license file.

    Classes that allow setting a licensor or a year also additionally need to specify:
    :attr licensor_placeholder: What (exactly) in the license file should be replaced
    by :param:`licensor`
    :attr year_placeholder: What (exactly) in the license file should be replaced
    by :param:`year`
    """

    licensor_placeholder = None
    year_placeholder = None

    def __init__(self, licensor=None, year=None):
        self._licensor = licensor
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
    def licensor(self):
        return self._licensor

    @property
    def year(self):
        """Returns the year provided at instantiation, if available. If one was not
        provided even though :attr:`year_placeholder` is set, it returns the current year.
        Otherwise it returns :param:`_year`, that is, 'None'.
        """
        if self._year:
            return self._year
        if self.year_placeholder:
            return datetime.datetime.now().year

        return self._year

    @property
    def content(self):
        with self.path.open('r') as f:
            content = f.read()

        if self.licensor_placeholder:
            content = content.replace(self.licensor_placeholder, self.licensor, 1)
        if self.year_placeholder:
            content = content.replace(self.year_placeholder, str(self.year), 1)

        return content


class AGPL3(License):
    name = 'GNU Affero General Public License version 3'
    path = LICENSE_DIR.joinpath('agpl-3.0')


class Apache(License):
    name = 'Apache License 2.0'
    path = LICENSE_DIR.joinpath('apache-2.0.md')
    licensor_placeholder = '{name of copyright owner}'
    year_placeholder = '{yyyy}'


class GPL3(License):
    name = 'GNU General Public License v3.0'
    path = LICENSE_DIR.joinpath('gpl-3.0.md')


class LGPL3(License):
    name = 'GNU Lesser General Public License v3.0'
    path = LICENSE_DIR.joinpath('lgpl-3.0.md')


class MIT(License):
    name = 'MIT License'
    path = LICENSE_DIR.joinpath('mit.md')
    licensor_placeholder = '[fullname]'
    year_placeholder = '[year]'


class MPL(License):
    name = 'Mozilla Public License Version 2.0'
    path = LICENSE_DIR.joinpath('mpl-2.0.md')


class Unlicense(License):
    name = 'The Unlicense'
    path = LICENSE_DIR.joinpath('unlicense.md')


licenses = [
    AGPL3,
    Apache,
    GPL3,
    LGPL3,
    MIT,
    MPL,
    Unlicense,
]
