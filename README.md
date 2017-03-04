# Notary: License your project

Notary is a Python CLI tool that allows you to manage your project's license.
any license from [Choose a License](https://choosealicense.com/) and add it to your project.

## Usage

```shell
$ notary
Usage: notary [OPTIONS] COMMAND [ARGS]...

  Manages your project's license.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Adds a license, replacing any that might exist.
  remove  Removes any license present in the current folder.
```

``` shell
Usage: notary add [OPTIONS]

  Tries to find a license that matches the given LICENSE argument. If one
  exists and takes a author and year, it adds them to the license. Otherwise
  it writes the license without an author and year and informs the user.

  :param license_name: the 'human' name of the license that should be added.
  Notary will try to guess the actual name from this. :param author: Tuple
  representing the name of the author. :param year: Integer representing the
  year that will be written to the license.

Options:
  -l, --license TEXT
  -a, --author TEXT
  -y, --year INTEGER  [default: 2017]
  -h, --help          Show this message and exit.
```

``` shell
$ notary add
License name: m
Author: Sorin Muntean
Year [2017]:
The following license file(s) already exist:
/Users/sorin/Workspace/notary/LICENSE
Remove /Users/sorin/Workspace/notary/LICENSE? [y/N]: y
Removed /Users/sorin/Workspace/notary/LICENSE.
Found the following matching licenses:
1: MIT License
2: Mozilla Public License Version 2.0
Please choose which one you'd like to add [1]: 1
Adding MIT License as the project's license. Continue? [y/N]: y
Added MIT License to /Users/sorin/Workspace/notary/LICENSE
```

``` shell
$ notary add --author 'Sorin Muntean'
License name: mit
Year [2017]: 2017
Adding MIT License as the project's license. Continue? [y/N]: y
Added MIT License to /Users/sorin/Workspace/notary/LICENSE
```

``` shell
$ notary add -l mit -a 'Sorin Muntean' -y 2017
Adding MIT License as the project's license. Continue? [y/N]: y
Added MIT License to /Users/sorin/Workspace/Python/Personal/github.com/notary/LICENSE
```

``` shell
Usage: notary remove [OPTIONS]

  Tries to find a file named LICENSE or LICENSE.md. If one (or both) exists,
  it asks the user if it should go ahead and remove them. Otherwise it exits
  and informs the user that none could be found.

Options:
  -h, --help  Show this message and exit.
```

``` shell
$ notary remove
The following license file(s) already exist:
/Users/sorin/Workspace/notary/LICENSE
Remove /Users/sorin/Workspace/notary/LICENSE? [y/N]: y
Removed /Users/sorin/Workspace/notary/LICENSE.
```

``` shell
$ notary remove
The following license file(s) already exist:
/Users/sorin/Workspace/notary/LICENSE
/Users/sorin/Workspace/notary/LICENSE.md
/Users/sorin/Workspace/notary/license.rst
Remove /Users/sorin/Workspace/notary/LICENSE? [y/N]: y
Removed /Users/sorin/Workspace/notary/LICENSE.
Remove /Users/sorin/Workspace/notary/LICENSE.md? [y/N]: y
Removed /Users/sorin/Workspace/notary/LICENSE.md.
Remove /Users/sorin/Workspace/notary/license.rst? [y/N]: y
Removed /Users/sorin/Workspace/notary/license.rst.
```

``` shell
$ notary remove
No license file found in the current directory.
```

## Installation
```shell
pip install notary
```

## Documentation
Soon to come.
