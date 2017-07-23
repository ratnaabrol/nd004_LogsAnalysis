"""Module defining a command line application for running log analysis on a
   database."""

import sys
import argparse

import logs_analysis.news_text_report as news_text_report

# one public method is acceptable for this class, so ok to ignore pylint error
# pylint: disable-msg=R0903


class CmdLineApp:
    """Command line application for running log analysis"""

    _DEFAULT_DB_NAME = "news"

    def __init__(self):
        self.args = {}

    def run(self):
        """Runs the command line application."""
        self._parse_cmd_line()
        reporter = news_text_report.NewsTextReport(self.args.db)
        print()  # line space to improve readability of output

        self._print_articles_report(reporter)
        self._print_authors_report(reporter)
        self._print_errors_report(reporter)

    def _parse_cmd_line(self):
        parser = argparse.ArgumentParser(
            description="Displays analysis of a news database.",
            prog="logs_analysis")
        parser.add_argument("--articles", dest="articles", type=int,
                            metavar="N", default=3,
                            help="Show most popular N articles (default 3).")
        parser.add_argument("--authors", dest="authors", type=int, metavar="N",
                            default=None,
                            help="Show the most popular N authors "
                            + "(default all).")
        parser.add_argument("--errors", dest="errors", type=float, metavar="F",
                            default=1.0,
                            help="Show dates on which the %%age of errors " +
                            "is greater than F (default 1.0).")
        parser.add_argument("--db", dest="db", type=str, metavar="name",
                            default=CmdLineApp._DEFAULT_DB_NAME,
                            help="sets the name of the database to report upon"
                            + " (default '{}')."
                            .format(CmdLineApp._DEFAULT_DB_NAME))
        self.args = parser.parse_args()

    def _print_articles_report(self, reporter):
        print("The most popular {} articles are:".format(self.args.articles))
        reporter.report_most_popular_articles(sys.stdout, self.args.articles)

    def _print_authors_report(self, reporter):
        if self.args.authors is None:
            print("The most popular authors are:")
        else:
            print("The most popular {} authors are:".format(self.args.authors))
        reporter.report_most_popular_authors(sys.stdout, self.args.authors)

    def _print_errors_report(self, reporter):
        print("The days on which more than {}% of requests led to errors:"
              .format(self.args.errors))
        reporter.report_get_dates_gt_errors_pct(sys.stdout, self.args.errors)
