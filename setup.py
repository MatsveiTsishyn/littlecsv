
"""
WARNING: this 'setup.py' file is not used as PIP packages setup is now done from he 'pyproject.toml' file.
But I will just leave it here for compatibility with older pip versions (< 19).
"""

# Imports ----------------------------------------------------------------------
from setuptools import setup, find_packages


# Setup ------------------------------------------------------------------------
setup(
    name="littlecsv",
    version="1.0.2",
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