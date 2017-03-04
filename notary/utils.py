import re
from functools import lru_cache
from pathlib import Path

from notary.models import licenses


def levenshtein(s1, s2):
    """Calculates the Levenshtein distance between two strings. Shamelessly stolen from
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                j + 1
            ] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def guess_license(name, **kwargs):
    probable = []
    likely = []
    for lic in licenses:
        if name.lower() in lic.name.lower() or name.lower() in lic.__name__.lower():
            probable.append(lic(**kwargs))
            continue

        likely.append(lic(**kwargs))

    if probable:
        return probable

    return likely


@lru_cache(maxsize=32)
def find_license_files():
    """Returns a list of :class:`Path <Path>` objects representing existing LICENSE files
    in the current directory.
    """
    rule = re.compile('(?i)license(\.[a-zA-Z]*)?')
    return [
        path for path in Path('.').glob('*') if path.is_file() and rule.match(path.name)
    ]
