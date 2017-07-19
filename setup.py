from setuptools import setup, find_packages
import unittest

# configure test discovery
TEST_DIR = "test"
TEST_PATTERN = "*_test.py"


def test_suite():
    '''Creates test suite using the unittest module's discovery algorithm.'''
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR, TEST_PATTERN)
    return suite

setup(
    name = "logs_analysis",
    version = "0.0.1",
    namespace_packages=["logs_analysis"],
    packages = find_packages("src"),
    package_dir={"":"src"},

    install_requires=["psycopg2==2.7.1"],

    test_suite = "setup.test_suite"
)
