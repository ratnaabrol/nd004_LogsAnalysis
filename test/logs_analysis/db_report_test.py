"""Tests for db_report module."""

import unittest

import logs_analysis.db_report as db_report
import logs_analysis.db_report_test_helper as db_report_test_helper

class DbReportTest(unittest.TestCase):
    """Test cases"""

    _TEST_DB = "news_test"

    def test_can_get_most_popular_authors(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.reset_database()
        helper.add_author("first author")
        helper.add_author("second author")
        helper.add_article("first author", "title", "slug1")
        helper.add_article("second author", "title", "slug2")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug2")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug2")

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        authors = report.get_most_popular_authors()
        self.assertIsNotNone(authors)
        self.assertTupleEqual(("first author", 3), authors[0])
        self.assertTupleEqual(("second author", 2), authors[1])

    def test_most_popular_authors_includes_those_with_no_accesses(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.reset_database()
        helper.add_author("first author")
        helper.add_author("second author")
        helper.add_article("first author", "title", "slug1")
        helper.add_article("second author", "title", "slug2")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        authors = report.get_most_popular_authors()
        self.assertIsNotNone(authors)
        self.assertTupleEqual(("first author", 4), authors[0])
        self.assertTupleEqual(("second author", 0), authors[1])

    def test_can_limit_most_popular_authors_list_length(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.reset_database()
        helper.add_author("first author")
        helper.add_author("second author")
        helper.add_author("third author")
        helper.add_article("first author", "title", "slug1")
        helper.add_article("second author", "title", "slug2")
        helper.add_article("third author", "title", "slug3")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug2")
        helper.add_log("/article/slug2")
        helper.add_log("/article/slug3")

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        authors = report.get_most_popular_authors(top_n=2)
        self.assertIsNotNone(authors)
        self.assertEqual(2, len(authors))
        self.assertTupleEqual(("first author", 3), authors[0])
        self.assertTupleEqual(("second author", 2), authors[1])
