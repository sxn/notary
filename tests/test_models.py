import pytest
from notary.models import License, MIT, Apache


def test_license_is_abstract():
    with pytest.raises(TypeError, message="Expected :class:`License` to be abstract.") as excinfo:
        License()

    excinfo.match("abstract methods name, path")


@pytest.mark.parametrize(
    "cls, author, year, expected", [
        (MIT, "John Smith", 2015, "Copyright (c) 2015 John Smith"),
        (MIT, "Acme Inc", 2010, "Copyright (c) 2010 Acme Inc"),
        (Apache, "John Smith", 2015, "Copyright 2015 John Smith"),
        (Apache, "Acme Inc", 2010, "Copyright 2010 Acme Inc"),
    ]
)
def test_author_and_year_in_license(cls, author, year, expected):
    lic = cls(author=author, year=year)
    assert expected in lic.content
