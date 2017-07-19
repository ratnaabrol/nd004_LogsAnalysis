"""Module that runs report queries against the database"""
import psycopg2


class DbReport:
    """Reports on a database."""

    _POPULAR_AUTHORS_SQL = """
    select author_name, count(*) as article_count
      from accessed_articles_ext
      group by author_name
      order by article_count desc"""

    _LIMIT_SQL = " limit %(top_n)s"

    def __init__(self, dbname):
        """Constructor.

         Keyword arguments:
         dbname -- name of the psql database to connect to. Must be provided by the caller.
         """
        self._dbname = dbname

    def get_most_popular_authors(self, top_n=None):
        """Report the most popular authors.

        Returns a list of tuples in order of authors whose articles have been
        viewed most often, optionally constrained to the top n authors. The
        tuple in the list contains author name and number of times their
        articles have been viewed.

        Keyword arguments:
        top_n -- the number of authors to which to limit the returned list.
        """
        authors = ()

        with psycopg2.connect(dbname=self._dbname) as news_db:
            with news_db.cursor() as cursor:
                sql = DbReport._POPULAR_AUTHORS_SQL
                if top_n is not None:
                    sql += DbReport._LIMIT_SQL
                cursor.execute(sql, (top_n))
                authors = cursor.fetchall()

        news_db.close()
        return authors
