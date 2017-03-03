import sys

import click
import requests
from bs4 import BeautifulSoup
from crayons import green, red

from notary import LICENSE_DIR

BASE_URL = "https://choosealicense.com"
LICENSES_URL = "{0}/licenses/".format(BASE_URL)


class License(object):

    def __init__(self, url, slug, name, content):
        self.url = url
        self.slug = slug
        self.name = name
        self.content = content
        self.path = LICENSE_DIR.joinpath("{0}.md".format(self.slug))

    def __repr__(self):
        return "<License slug: {0}, name: {1}".format(self.slug, self.name)

    def open(self, *args, **kwargs):
        return self.path.open('w')


@click.group()
def cli():
    """Fetch licenses from https://choosealicense.com/."""


@cli.command('run', short_help="scrape {0} licenses".format(BASE_URL))
def run():
    """
    Crawls https://choosealicense.com/licenses and fetches all open source license urls.
    It then crawls each individual license page and stores it in the {LICENSE_DIR}
    folder, under {slug}.md.
    """
    response = requests.get(LICENSES_URL)

    if response.status_code != 200:
        click.echo(
            "URL {0} returned status {1}".
            format(green(LICENSES_URL), red(response.status_code))
        )
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    url_tuples = [
        (BASE_URL, license_overview.div.h3.a.get('href'))
        for license_overview in soup.find_all('div', {'class': 'license-overview'})
    ]

    with click.progressbar(
            iterable=url_tuples, show_pos=True, label="Fetching licenses"
    ) as urls:
        for url_tuple in urls:
            click.echo()
            url = ''.join(url_tuple)
            response = requests.get(url)
            license_soup = BeautifulSoup(response.content, 'html.parser')
            try:
                lic = License(
                    url,
                    url_tuple[1].split('/')[2],
                    license_soup.h1.string,
                    license_soup.find(id='license-text').string
                )
                with lic.open('w') as f:
                    f.write(lic.content)
                click.echo("Finished crawling {0}.".format(green(url)))
            except AttributeError:
                click.echo("Could not fetch license from {0}".format(green(url)))


if __name__ == '__main__':
    cli()
