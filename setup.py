from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="csv_splitter",
    version="0.0.1",
    description="",
    long_description=readme,
    author="ktftk",
    url="",
    packages=find_packages(),
    install_requires=_requires_from_file("requirements.txt"),
    include_package_data=True,
)
