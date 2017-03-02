import sys
import re
from pathlib import Path

import click
import crayons


def find_license_files():
    """
    Returns a list of pathlib.Path objects representing existing LICENSE files in the
    current directory.
    """
    rule = re.compile('(?i)license(\.[a-zA-Z]*)?')
    return [path for path in Path('.').glob('*') if rule.match(path.name)]


@click.group()
def cli():
    """Manage your project's license."""


@cli.command('add', short_help='add a license')
@click.argument('lic', metavar='LICENSE', type=click.STRING)
@click.argument('author', type=click.STRING)
@click.argument('year', type=click.INT)
def add(lic, author, year):
    """
    Tries to find a license that matches the given LICENSE argument. If one exists and
    takes an author and year, it adds them to the license. Otherwise it writes the license
    without an author and year and informs the user.
    """


@cli.command('remove', short_help='remove any license')
def remove():
    """
    Tries to find a file named LICENSE or LICENSE.md. If one (or both) exists, it asks the
    user if it should go ahead and delete them. Otherwise it exits and informs the user
    that none could be found.
    """
    license_files = find_license_files()
    if not license_files:
        click.echo("No license file found in the current directory.")
        sys.exit(0)
    click.echo("Found the following license file(s):")
    click.echo(crayons.green('\n'.join([str(path.absolute()) for path in license_files])))
    for path in license_files:
        if click.confirm("Delete {0}?".format(crayons.green(str(path.absolute())))):
            try:
                path.unlink()
                click.echo("{} removed.".format(crayons.green(str(path.absolute()))))
            except Exception:
                click.echo(
                    'Could not delete {0}.'.format(crayons.green(str(path.absolute()))),
                    err=True
                )

    sys.exit(0)
