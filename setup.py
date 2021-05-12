from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()


setup(
    name="csv_splitter",
    version="0.0.1",
    description="",
    long_description=readme,
    author="ktftk",
    url="https://github.com/ktftk/csv_splitter",
    packages=find_packages(),
    tests_require=["pytest", "csv-diff"],
)
