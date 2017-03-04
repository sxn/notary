from pathlib import Path

from click.testing import CliRunner

import notary
from notary import cli


def test_add_license_no_preexisting():
    runner = CliRunner()
    with runner.isolated_filesystem():
        license_file = Path('LICENSE')
        assert not license_file.exists()
        result = runner.invoke(cli.add, input="\n".join(['mit', 'John Smith', 'y']))
        assert result.exit_code == 0
        assert "License name: mit\n" in result.output
        assert "Author: John Smith\n" in result.output
        assert "Adding MIT License as the project's license. Continue? [y/N]: y\n"
        assert "Added MIT License" in result.output
        assert license_file.exists()


def test_add_license_no_preexisting_multiple_found():
    runner = CliRunner()
    with runner.isolated_filesystem():
        license_file = Path('LICENSE')
        assert not license_file.exists()
        result = runner.invoke(cli.add, input="\n".join(['m', '1', 'John Smith', 'y']))
        assert result.exit_code == 0
        assert "License name: m\n" in result.output
        assert "Found the following matching licenses:\n" in result.output
        assert "1: MIT License\n" in result.output
        assert "2: Mozilla Public License Version 2.0\n" in result.output
        assert "Please choose which one you'd like to add [1]: 1\n"
        assert "Author: John Smith\n" in result.output
        assert "Adding MIT License as the project's license. Continue? [y/N]: y\n"
        assert "Added MIT License to /" in result.output
        assert "/LICENSE.\n" in result.output
        assert license_file.exists()


def test_add_license_no_preexisting_no_author_needed():
    runner = CliRunner()
    with runner.isolated_filesystem():
        license_file = Path('LICENSE')
        assert not license_file.exists()
        result = runner.invoke(cli.add, input="\n".join(['agpl', 'y']))
        assert result.exit_code == 0
        assert "License name: agpl\n" in result.output
        assert "Adding GNU Affero General Public License version 3 as the project's license. Continue? [y/N]: y\n" in result.output
        assert "Added GNU Affero General Public License version 3 to /" in result.output
        assert "/LICENSE.\n" in result.output
        assert license_file.exists()


def test_add_license_no_preexisting_no_license_matched():
    runner = CliRunner()
    with runner.isolated_filesystem():
        license_file = Path('LICENSE')
        assert not license_file.exists()
        result = runner.invoke(cli.add, input="\n".join(['gibberish', '3', 'y']))
        assert result.exit_code == 0
        assert "License name: gibberish\n" in result.output
        assert "Found the following matching licenses:\n" in result.output
        assert "1: GNU Affero General Public License version 3\n" in result.output
        assert "2: Apache License 2.0\n" in result.output
        assert "3: GNU General Public License v3.0\n" in result.output
        assert "4: GNU Lesser General Public License v3.0\n" in result.output
        assert "5: MIT License\n" in result.output
        assert "6: Mozilla Public License Version 2.0\n" in result.output
        assert "7: The Unlicense\n" in result.output
        assert "Please choose which one you'd like to add [1]: 3\n" in result.output
        assert "Adding GNU General Public License v3.0 as the project's license. Continue? [y/N]: y\n" in result.output
        assert "Added GNU General Public License v3.0 to /" in result.output
        assert "/LICENSE.\n" in result.output
        assert license_file.exists()


def test_add_license_preexisting_license():
    runner = CliRunner()
    with runner.isolated_filesystem():
        old_license_file = Path('LICENSE.rst')
        with old_license_file.open('w') as f:
            f.write('')
        new_license_file = Path('LICENSE')
        assert not new_license_file.exists()
        result = runner.invoke(cli.add, input="\n".join(['y', 'mit', 'John Smith', 'y']))
        assert result.exit_code == 0
        assert "The following license file(s) already exist:\n" in result.output
        assert "/LICENSE.rst\n" in result.output
        assert "Remove /" in result.output
        assert "/LICENSE.rst? [y/N]: y\n" in result.output
        assert "Removed /" in result.output
        assert "/LICENSE.rst.\n" in result.output
        assert "License name: mit\n" in result.output
        assert "Author: John Smith\n" in result.output
        assert "Adding MIT License as the project's license. Continue? [y/N]: y\n"
        assert "Added MIT License" in result.output
        assert new_license_file.exists()


def test_remove_no_license():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.remove)
        assert result.exit_code == 0
        assert "No license file found in the current directory." in result.output


def test_remove_existing_license_answer_yes():
    runner = CliRunner()
    with runner.isolated_filesystem():
        license_file = Path('LICENSE.rst')
        with license_file.open('w') as f:
            f.write('')
        assert license_file.exists()
        result = runner.invoke(cli.remove, input='y')
        assert result.exit_code == 0
        assert "The following license file(s) already exist:" in result.output
        assert "/LICENSE.rst? [y/N]: y\n" in result.output
        assert "Removed /" in result.output
        assert "/LICENSE.rst.\n" in result.output
        assert not license_file.exists()


def test_remove_existing_license_answer_no():
    runner = CliRunner()
    with runner.isolated_filesystem():
        license_file = Path('LICENSE.rst')
        with license_file.open('w') as f:
            f.write('')
        assert license_file.exists()
        result = runner.invoke(cli.remove, input='n')
        assert result.exit_code == 0
        assert "The following license file(s) already exist:" in result.output
        assert "/LICENSE.rst? [y/N]: n\n" in result.output
        assert "Not removing license.\n" in result.output
        assert license_file.exists()
