import datetime
import sys

import click
from crayons import blue, green, white, yellow

from notary.__version__ import __version__
from notary import LICENSE_FILE
import notary.utils as utils

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name=yellow("notary"), version=blue(__version__))
def cli():
    """Manages your project's license."""


@cli.command(
    "add", short_help=f"Adds a license, {white('replacing any that might exist.')}", context_settings=CONTEXT_SETTINGS
)
@click.option(
    "-l",
    "--license",
    "license_name",
    type=click.STRING,
    help=f'The name of the license you want to add. {white("Does not have to be exact.")}'
)
@click.option(
    "-a",
    "--author",
    type=click.STRING,
    help=f"The name that will be on the license. {white('Is ignored if not required.')}"
)
@click.option(
    "-y",
    "--year",
    type=click.INT,
    default=datetime.datetime.now().year,
    show_default=True,
    help=f"The year that will be on the license. {white('Is ignored if not required.')}"
)
def add(license_name, author, year):
    """Tries to find a license that matches the given LICENSE argument. If one exists and
    takes a author and year, it adds them to the license. Otherwise it writes the license
    without an author and year and informs the user.

    :param license_name: the 'human' name of the license that should be added. Notary will
    try to guess the actual name from this.
    :param author: Tuple representing the name of the author.
    :param year: Integer representing the year that will be written to the license.
    """

    ensure_no_license_files()

    if not license_name:
        license_name = click.prompt("License name", type=click.STRING)

    guesses = utils.guess_license(name=license_name)
    if len(guesses) > 1:
        cls = choose_license(guesses, author=author, year=year)
    else:
        cls = guesses[0]

    if cls.author_placeholder and not author:
        click.echo(f"{yellow(cls.name)} requires an author.")
        author = click.prompt("Author", type=click.STRING)

    lic = cls(author=author, year=year)

    if click.confirm(f"Adding {yellow(lic.name)} as the project's license. Continue?"):
        with LICENSE_FILE.open("w") as f:
            f.write(lic.content)

        click.echo(f"Added {yellow(lic.name)} to {green(str(LICENSE_FILE.absolute()))}.")


@cli.command(
    "remove", short_help="Removes any license present in the current folder.", context_settings=CONTEXT_SETTINGS
)
def remove():
    """Tries to find a file named LICENSE or LICENSE.md. If one (or both) exists, it asks the
    user if it should go ahead and remove them. Otherwise it exits and informs the user
    that none could be found.
    """

    existing_license_files = utils.find_license_files()
    if not existing_license_files:
        click.echo("No license file found in the current directory.")
        return

    ensure_no_license_files()


def ensure_no_license_files():
    """Finds any potentially existing LICENSE files in the current directory and offers to
    delete whatever it finds.
    """

    existing_license_files = utils.find_license_files()

    if existing_license_files:
        click.echo("The following license file(s) already exist:")
        echo_paths(existing_license_files)
        for license_file in existing_license_files:
            remove_license_file(license_file)


def echo_paths(paths):
    click.echo(green("\n".join([str(path.absolute()) for path in paths])))


def choose_license(licenses, author, year):
    click.echo("Found the following matching licenses:")
    click.echo(green("\n".join([f"{index + 1}: {lic.name}" for index, lic in enumerate(licenses)])))
    choice = click.prompt("Please choose which one you'd like to add", default=1, type=click.IntRange(1, len(licenses)))
    return licenses[choice - 1]


def remove_license_file(license_file):
    if not click.confirm(f"Remove {green(str(license_file.absolute()))}?"):
        click.echo("Not removing license.")
        sys.exit(0)

    try:
        license_file.unlink()
        click.echo(f"Removed {green(str(license_file.absolute()))}.")
    except Exception:
        click.echo(f"Could not remove {green(str(license_file.absolute()))}.", err=True)
