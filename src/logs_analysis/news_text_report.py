"""Module for reporting statistics on the news articles as text output."""

import psycopg2
import logs_analysis.db_report as db_report


class NewsTextReport:
    """Text reporter for news articles."""

    _DB_ERR_MSG = "There was a problem querying the database: {}"

    def __init__(self, dbname):
        """Constructor.

        Keyword arguments:
        dbname -- the name of the database to report on.
                  Required.
        """
        self._dbname = dbname  # stored for diagnostic purposes
        self._db_reporter = db_report.DbReport(self._dbname)

    def report_most_popular_articles(self, out, limit=None):
        """Outputs list of most popular articles.

        Keyword arguments:
        out -- the stream to which to output. Required.
        limit -- the maximum number of articles to output. Optional. Defaults
                 to None, which means unlimited.
        """
        try:
            articles = self._db_reporter.get_most_popular_articles(limit)
            msg = ""
            for article in articles:
                views_str = format(article[1], ",d")
                msg += "'{}' - {} views\n".format(article[0], views_str)
            if not msg:
                msg = "None"
            print(msg, file=out)
        except psycopg2.Error as exp:
            print(NewsTextReport._DB_ERR_MSG.format(exp))

    def report_most_popular_authors(self, out, limit=None):
        """Outputs list of most popular author.

        Keyword arguments:
        out -- the stream to which to output. Required.
        limit -- the maximum number of authors to output. Optional. Defaults
                 to None, which means unlimited.
        """
        try:
            authors = self._db_reporter.get_most_popular_authors(limit)
            msg = ""
            for author in authors:
                views_str = format(author[1], ",d")
                msg += "'{}' - {} views\n".format(author[0], views_str)
            if not msg:
                msg = "None"
            print(msg, file=out)
        except psycopg2.Error as exp:
            print(NewsTextReport._DB_ERR_MSG.format(exp))

    def report_get_dates_gt_errors_pct(self, out, pct_errors):

        """Outputs list of dates with a percentage of errors
        greater than a given percentage.

        Keyword arguments:
        out -- the stream to which to output. Required.
        pct_errors -- the percentage of errors that is our lower bound
                      (exclusive). Required.
        """
        try:
            days = self._db_reporter.get_dates_wth_more_pct_errors(pct_errors)
            msg = ""
            for day in days:
                date_str = day[0].strftime("%a %d %B %Y")
                pct_str = format(day[1], ".2f")
                total_str = format(day[2], ",d")
                msg += "{} - {}% errors out of {} requests\n".format(date_str,
                                                                     pct_str,
                                                                     total_str)
            if not msg:
                msg = "None"
            print(msg, file=out)
        except psycopg2.Error as exp:
            print(NewsTextReport._DB_ERR_MSG.format(exp))
