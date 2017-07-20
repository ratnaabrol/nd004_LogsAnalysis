"""Tests for db_report module. These are integration tests and require that
the test database has been created and db structure created before these
tests are run."""

import unittest
import datetime as dt

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


    #
    # Percent response errors tests
    #
    def test_can_get_list_of_dates_with_more_than_Npct_errors(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)

        # 20% errors on 31st March 2020
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 31))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 31))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 3, 31))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 31))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 31))

        # 33.3% errors on 1st April 2020
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 1))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 1))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 1))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 1))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 1))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 1))

        # 50% errors on 2nd April 2020
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 2))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 2))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 2))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 2))

        # 75% errors on 3nd April 2020
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 3))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 3))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 4, 3))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 4, 3))


        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)

        # more than 19%
        pct_errors = report.get_dates_wth_more_pct_errors(19)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(4, len(pct_errors))

        # more than 33%
        pct_errors = report.get_dates_wth_more_pct_errors(33)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(3, len(pct_errors))

        # more than 49%
        pct_errors = report.get_dates_wth_more_pct_errors(49)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(2, len(pct_errors))

        # more than 74%
        pct_errors = report.get_dates_wth_more_pct_errors(74)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(1, len(pct_errors))

        # more than 76%
        pct_errors = report.get_dates_wth_more_pct_errors(76)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(0, len(pct_errors))

    def test_can_get_list_of_dates_when_a_date_has_no_errors(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)

        # 0% errors on 21st March 2020
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 21))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 21))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 21))
        helper.add_log("/article/slug1",
                       timestamp=dt.datetime(2020, 3, 21))

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        pct_errors = report.get_dates_wth_more_pct_errors(0)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(0, len(pct_errors))

    def test_can_get_list_of_dates_when_a_date_has_only_errors(self):
        # add test data
        helper = \
            db_report_test_helper.DbReportTestHelper(DbReportTest._TEST_DB)

        # 100% errors on 21st March 2020
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 3, 21))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 3, 21))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 3, 21))
        helper.add_log("/article/slug1", status="500 Server Error",
                       timestamp=dt.datetime(2020, 3, 21))

        # run the test
        report = db_report.DbReport(DbReportTest._TEST_DB)
        pct_errors = report.get_dates_wth_more_pct_errors(99)
        self.assertIsNotNone(pct_errors)
        self.assertEqual(1, len(pct_errors))
