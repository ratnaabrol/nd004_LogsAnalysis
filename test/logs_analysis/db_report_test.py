"""Tests for db_report module. These are integration tests and require that
the test database has been created and db structure created before these
tests are run."""

import unittest

import logs_analysis.db_report as db_report
import logs_analysis.db_report_test_helper as db_report_test_helper

class DbReportTest(unittest.TestCase):
    """Test cases"""

    _TEST_DB = "news_test"

    #
    # Set up and tear down methods.
    #
    @classmethod
    def tearDownClass(cls):
        """Reset database once all tests have run."""
        helper = \
            db_report_test_helper.DbReportTestHelper(cls._TEST_DB)
        helper.reset_database()

    def setUp(self):
        """Reset the database before each test is run"""
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.reset_database()

    #
    # Popular authors tests
    #
    def test_can_get_most_popular_authors(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
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
        self.assertEqual(2, len(authors))
        self.assertTupleEqual(("first author", 3), authors[0])
        self.assertTupleEqual(("second author", 2), authors[1])

    def test_most_popular_authors_includes_those_with_no_accesses(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
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
        self.assertEqual(2, len(authors))
        self.assertTupleEqual(("first author", 4), authors[0])
        self.assertTupleEqual(("second author", 0), authors[1])

    def test_can_limit_length_of_most_popular_authors_list(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.add_author("first author")
        helper.add_author("second author")
        helper.add_author("third author")
        helper.add_author("forth author")
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
        authors = report.get_most_popular_authors(top_n=3)
        self.assertIsNotNone(authors)
        self.assertEqual(3, len(authors))
        self.assertTupleEqual(("first author", 3), authors[0])
        self.assertTupleEqual(("second author", 2), authors[1])
        self.assertTupleEqual(("third author", 1), authors[2])

    #
    # Popular articles tests
    #
    def test_can_get_most_popular_articles(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.add_author("first author")
        helper.add_article("first author", "title one", "slug1")
        helper.add_article("first author", "title two", "slug2")
        helper.add_article("first author", "title three", "slug3")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug2")
        helper.add_log("/article/slug3")
        helper.add_log("/article/slug3")

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        articles = report.get_most_popular_articles()
        self.assertIsNotNone(articles)
        self.assertEqual(3, len(articles))
        self.assertTupleEqual(("title one", 4), articles[0])
        self.assertTupleEqual(("title three", 2), articles[1])
        self.assertTupleEqual(("title two", 1), articles[2])

    def test_most_popular_articles_includes_those_with_no_accesses(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.add_author("first author")
        helper.add_article("first author", "title one", "slug1")
        helper.add_article("first author", "title two", "slug2")
        helper.add_article("first author", "title three", "slug3")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug3")
        helper.add_log("/article/slug3")

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        articles = report.get_most_popular_articles()
        self.assertIsNotNone(articles)
        self.assertEqual(3, len(articles))
        self.assertTupleEqual(("title one", 4), articles[0])
        self.assertTupleEqual(("title three", 2), articles[1])
        self.assertTupleEqual(("title two", 0), articles[2])

    def test_can_limit_length_of_most_popular_articles_list(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)
        helper.add_author("first author")
        helper.add_article("first author", "title one", "slug1")
        helper.add_article("first author", "title two", "slug2")
        helper.add_article("first author", "title three", "slug3")
        helper.add_article("first author", "four three", "slug4")
        helper.add_article("first author", "five three", "slug5")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug1")
        helper.add_log("/article/slug2")
        helper.add_log("/article/slug3")
        helper.add_log("/article/slug3")

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        articles = report.get_most_popular_articles(top_n=3)
        self.assertIsNotNone(articles)
        self.assertEqual(3, len(articles))
        self.assertTupleEqual(("title one", 4), articles[0])
        self.assertTupleEqual(("title three", 2), articles[1])
        self.assertTupleEqual(("title two", 1), articles[2])
