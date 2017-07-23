"""Project build script. This uses setuptools to drive the build."""

import unittest
from setuptools import setup, find_packages

# configure test discovery
TEST_DIR = "test"
TEST_PATTERN = "*_test.py"


def test_suite():
    '''Creates test suite using the unittest module's discovery algorithm.'''
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR, TEST_PATTERN)
    return suite


setup(
    name="logs_analysis",
    version="1.0.0",
    namespace_packages=["logs_analysis"],
    python_requires='>=3',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["psycopg2==2.7.1"],
    entry_points={
        "console_scripts": [
            "logs_analysis=logs_analysis:__main__.main"
        ]
    },
    test_suite="setup.test_suite"
)
