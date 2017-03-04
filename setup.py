from setuptools import setup, find_packages

setup(
    name='notary',
    version='0.1.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    install_requires=['click', 'crayons'],
    entry_points='''
        [console_scripts]
        notary=notary:cli
    '''
)
