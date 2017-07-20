"""Module that runs report queries against the database"""
import psycopg2


class DbReport:
    """Reports on a database."""

    _POPULAR_AUTHORS_SQL = """
    select authors.name as author_name, count(aae.derived_slug) as article_count
      from accessed_articles_ext as aae
      right join authors on aae.author = authors.id
      group by authors.name
      order by article_count desc"""

    _POPULAR_ARTICLES_SQL = """
    select articles.title, count(aae.derived_slug) as access_count
      from accessed_articles_ext aae
      right join articles on aae.article = articles.id
      group by aae.article, articles.title
      order by access_count desc"""

    _LIMIT_SQL = " limit %(top_n)s"

    def __init__(self, dbname):
        """Constructor.

         Keyword arguments:
         dbname -- name of the psql database to connect to. Required.
         """
        self._dbname = dbname

    def get_most_popular_authors(self, top_n=None):
        """Report the most popular authors.

        Returns a list of tuples in order of authors whose articles have been
        viewed most often, optionally constrained to the top n authors. The
        tuples in the list have first item as author name and second item as
        number of times their articles have been viewed.

        Keyword arguments:
        top_n -- the number of authors to which to limit the returned list.
        """
        authors = []

        with psycopg2.connect(dbname=self._dbname) as news_db:
            with news_db.cursor() as cursor:
                sql = DbReport._POPULAR_AUTHORS_SQL
                if top_n is not None:
                    sql += DbReport._LIMIT_SQL
                cursor.execute(sql, {"top_n":top_n})
                authors = cursor.fetchall()

        news_db.close()
        return authors

    def get_most_popular_articles(self, top_n=None):
        """Report the most popular articles.

        Returns a list of tuples in order of articles that have been
        viewed most often, optionally constrained by the top n articles.
        The tuples in the list have first item as article title and second
        item number of times it has been viewed.

        Keyword arguments:
        top_n -- the number of articles to which to limit the returned list.
        """
        articles = []

        with psycopg2.connect(dbname=self._dbname) as news_db:
            with news_db.cursor() as cursor:
                sql = DbReport._POPULAR_ARTICLES_SQL
                if top_n is not None:
                    sql += DbReport._LIMIT_SQL
                cursor.execute(sql, {"top_n":top_n})
                articles = cursor.fetchall()

        news_db.close()
        return articles
