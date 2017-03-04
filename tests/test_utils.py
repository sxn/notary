from pathlib import Path
import pytest

from notary import utils
from notary.models import (
    AGPL3, Apache, GPL3, LGPL3, MIT, MPL, Unlicense, LICENSES as SUPPORTED_LICENSES
)


@pytest.mark.parametrize(
    "name, expected",
    [('gibberish', SUPPORTED_LICENSES), ('mit', [MIT]), ('m', [MIT, MPL]),
     ('gpl', [AGPL3, GPL3, LGPL3]), ('apache', [Apache]), ('a', [AGPL3, Apache, GPL3, LGPL3, MPL]),
     ('', SUPPORTED_LICENSES), (None, SUPPORTED_LICENSES)]
)
def test_guess_license(name, expected):
    guesses = utils.guess_license(name)
    assert guesses == expected


@pytest.mark.parametrize(
    "folder, expected_count, expected_files",
    [('tests/no_licenses', 0, []),
     ('tests/some_licenses', 4, list(Path('tests/some_licenses').glob('*')))]
)
def test_find_license_files(folder, expected_count, expected_files):
    paths = utils.find_license_files(folder)
    assert len(paths) == expected_count
    assert paths == expected_files
