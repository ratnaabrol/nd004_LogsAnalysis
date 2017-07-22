"""Module for reporting statistics on the news articles as text output."""

import logs_analysis.db_report as db_report


class NewsTextReport:
    """Reporter for news articles."""

    _DB_NAME = "news"

    def __init__(self):
        self._db_reporter = db_report.DbReport(NewsTextReport._DB_NAME)

    def report_most_popular_articles(self, out, limit=None):
        """Outputs list of most popular articles.

        Keyword arguments:
        out -- the stream to which to output. Required.
        limit -- the maximum number of articles to output. Optional. Defaults
                 to unlimited.
        """
        articles = self._db_reporter.get_most_popular_articles(limit)
        for article in articles:
            views_str = format(article[1], ",d")
            msg = "'{}' - {} views".format(article[0], views_str)
            print(msg, file=out)

    def report_most_popular_authors(self, out, limit=None):
        """Outputs list of most popular author.

        Keyword arguments:
        out -- the stream to which to output. Required.
        limit -- the maximum number of authors to output. Optional. Defaults
                 to unlimited.
        """
        authors = self._db_reporter.get_most_popular_authors(limit)
        for author in authors:
            views_str = format(author[1], ",d")
            msg = "'{}' - {} views".format(author[0], views_str)
            print(msg, file=out)

    def report_get_dates_gt_errors_pct(self, out, pct_errors):
        """Outputs list of dates with a percentage of errors
        greater than a given percentage.

        Keyword arguments:
        out -- the stream to which to output. Required.
        pct_errors -- the percentage of errors that is our lower bound
                      (exclusive). Required.
        """
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
