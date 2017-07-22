"""Main script for the package. Will output text report to stdout."""

import sys
import argparse

import logs_analysis.news_text_report as news_text_report

# pylint: disable-msg=C0103

parser = argparse.ArgumentParser(
    description="Displays analysis of the news database.",
    prog="logs_analysis")

parser.add_argument("--articles", dest="articles", type=int, metavar="N",
                    default=3,
                    help="Show most popular N articles (default 3).")
parser.add_argument("--authors", dest="authors", type=int, metavar="N",
                    default=None,
                    help="Show the most popular N authors (default all).")
parser.add_argument("--errors", dest="errors", type=float, metavar="F",
                    default=1.0,
                    help="Show dates on which the %%age of errors is greater"
                    + " than F (default 1.0).")

args = parser.parse_args()

reporter = news_text_report.NewsTextReport()

print()
print("The most popular {} articles are:".format(args.articles))
reporter.report_most_popular_articles(sys.stdout, args.articles)

print()
if args.authors is None:
    print("The most popular authors are:")
else:
    print("The most popular {} authors are:".format(args.authors))

reporter.report_most_popular_authors(sys.stdout, args.authors)

print()
print("The days on which more than {}% of requests led to errors:"
      .format(args.errors))
reporter.report_get_dates_gt_errors_pct(sys.stdout, args.errors)

print()
