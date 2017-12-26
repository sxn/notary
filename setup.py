from pathlib import Path
from setuptools import setup

here = Path(__file__).parent

with here.joinpath("README.rst").open() as f:
    long_description = "\n" + f.read()

about = {}
with here.joinpath("notary", "__version__.py").open() as f:
    exec(f.read(), about)

required = ["click", "crayons"]

setup(
    name="notary",
    version=about["__version__"],
    description="License your project",
    long_description=long_description,
    author="Sorin Muntean",
    author_email="contact@sorinmuntean.ro",
    url="https://github.com/sxn/notary",
    packages=["notary"],
    package_data={"notary": ["licenses/*.md"]},
    entry_points={
        "console_scripts": ["notary=notary.cli:cli"],
    },
    install_requires=required,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
)
