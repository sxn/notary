import re
import sys
from functools import lru_cache
from pathlib import Path

import click
from crayons import green, yellow

from notary import LICENSE_FILE
import notary.utils as utils


@lru_cache(maxsize=32)
def find_license_files():
    """Returns a list of :class:`Path <Path>` objects representing existing LICENSE files in the
    current directory.
    """
    rule = re.compile('(?i)license(\.[a-zA-Z]*)?')
    return [
        path for path in Path('.').glob('*') if path.is_file() and rule.match(path.name)
    ]


@click.group()
def cli():
    """Manage your project's license."""


def join_licensor_name(ctx, param, value):
    return " ".join(value)


@cli.command('add', short_help='add a license')
@click.argument('license_name', metavar='LICENSE', type=click.STRING)
@click.argument('licensor', nargs=-1, type=click.STRING, callback=join_licensor_name)
@click.argument('year')
def add(license_name=None, licensor=None, year=None):
    """Tries to find a license that matches the given LICENSE argument. If one exists and
    takes a licensor and year, it adds them to the license. Otherwise it writes the license
    without an licensor and year and informs the user.

    :param license_name: the 'human' name of the license that should be added. Notary will
    try to guess the actual name from this.
    :param licensor: Tuple representing the name of the licensor.
    :param year: Integer representing the year that will be written to the license.
    """
    ensure_no_license_files()

    guesses = utils.guess_license(name=license_name, licensor=licensor, year=year)
    if len(guesses) > 1:
        lic = choose_license(guesses)
    else:
        lic = guesses[0]

    if click.confirm("Adding {0} license. Is this correct?".format(yellow(lic.name))):
        with LICENSE_FILE.open('w') as f:
            f.write(lic.content)
            click.echo(
                "Added {0} to {1}".
                format(yellow(lic.name), green(str(LICENSE_FILE.absolute())))
            )


@cli.command('remove', short_help='remove any license')
def remove():
    """Tries to find a file named LICENSE or LICENSE.md. If one (or both) exists, it asks the
    user if it should go ahead and remove them. Otherwise it exits and informs the user
    that none could be found.
    """
    existing_license_files = find_license_files()
    if not existing_license_files:
        click.echo("No license file found in the current directory.")
        sys.exit(0)

    click.echo("Found the following license file(s):")
    ensure_no_license_files()
    sys.exit(0)


def ensure_no_license_files():
    """Finds any potentially existing LICENSE files in the current directory and offers to
    delete whatever it finds.
    """
    existing_license_files = find_license_files()
    if existing_license_files:
        click.echo("The following license file(s) already exist:")
        echo_paths(existing_license_files)
        for license_file in existing_license_files:
            remove_license_file(license_file)


def echo_paths(paths):
    click.echo(green('\n'.join([str(path.absolute()) for path in paths])))


def choose_license(licenses):
    click.echo("Found the following matching licenses:")
    click.echo(
        green(
            '\n'.join([
                '{index}: {name}'.format(index=index + 1, name=lic.name)
                for index, lic in enumerate(licenses)
            ])
        )
    )
    choice = click.prompt(
        "Please choose which one you'd like to add",
        default=1,
        type=click.IntRange(1, len(licenses))
    )
    return licenses[choice - 1]


def remove_license_file(license_file):
    if not click.confirm("Remove {0}?".format(green(str(license_file.absolute())))):
        sys.exit(0)

    try:
        license_file.unlink()
        click.echo("Removed {0}.".format(green(str(license_file.absolute()))))
    except Exception:
        click.echo(
            'Could not remove {0}.'.format(green(str(license_file.absolute()))), err=True
        )
