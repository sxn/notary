# Notary: License your project

Notary is a Python CLI tool that allows you to manage your project's license.
any license from [Choose a License](https://choosealicense.com/) and add it to your project.

## Usage

```shell
$ notary --help
Usage: notary [OPTIONS] COMMAND [ARGS]...

Options:
  --version        Show the version and exit.
  --help           Show this message and exit.

Commands:
  add        Adds a license to your project, replacing any that might exist.
  remove     Removes LICENSE or LICENSE.md if they exist, otherwise nothing.
```

``` shell
$ notary add --help
Usage: notary add [OPTIONS] LICENSE AUTHOR YEAR

Tries to find a license that matches the given LICENSE argument. If one exists and takes an author and year, it adds them to the license. Otherwise it writes the license without an author and year and informs the user.

Options:
  --help           Show this message and exit.
```

``` shell
$ notary remove --help
Usage: notary remove [OPTIONS]

Tries to find a file named LICENSE or LICENSE.md. If one (or both) exists, it asks the user if it should go ahead and removes them. Otherwise it exits and informs the user that none could be found.

Options:
  --help           Show this message and exit.
```

## Installation
``py
pip install notary
``
