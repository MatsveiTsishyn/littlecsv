
# Imports ----------------------------------------------------------------------
from setuptools import setup, find_packages


# Setup ------------------------------------------------------------------------
setup(
    name="littlecsv",
    version="1.0.1",
    author="Matsvei Tsishyn",
    author_email="matsvei.tsishyn@protonmail.com",
    description="Simple, light and little pip package to read, write and manage CSV files ('.csv') in Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MatsveiTsishyn/littlecsv",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts":[
            "littlecsv_show=littlecsv.cli:show",
        ],
    },
)