# generate setup.py file for the package

from setuptools import setup, find_packages

setup(
    name='kabucom-station-py',
    version='0.1',
    packages=find_packages("src"),
    package_dir={"": "src"}
)