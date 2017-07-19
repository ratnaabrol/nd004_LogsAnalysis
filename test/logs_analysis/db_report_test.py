"""Tests for db_report module."""

import unittest
import logs_analysis.db_report as db_report

class DbReportTest(unittest.TestCase):
    """Test cases"""

    def test_can_get_most_popular_authors(self):
        # TODO: use test database instead of the live database
        report = db_report.DbReport("news")
        authors = report.get_most_popular_authors()
        print(authors)
        self.assertIsNotNone(authors)
