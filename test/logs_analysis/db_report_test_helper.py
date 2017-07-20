"""Module containing helper code for testing db."""

import psycopg2

class DbReportTestHelper:
    """Helper class for creating test data"""

    _ALL_TABLES = ["articles", "authors", "log"]
    _ALL_SEQUENCES = ["articles_id_seq", "authors_id_seq", "log_id_seq"]

    def __init__(self, dbname):
        """Constructor

        Keyword arguments:
        dbname -- the name of the database this instance will operate upon.
        """
        self._dbname = dbname

    def reset_database(self):
        """Reset the database"""
        with psycopg2.connect(dbname=self._dbname) as test_db:
            with test_db.cursor() as cursor:
                for table in DbReportTestHelper._ALL_TABLES:
                    cursor.execute("TRUNCATE TABLE {}".format(table))

                for sequence in DbReportTestHelper._ALL_SEQUENCES:
                    cursor.execute("ALTER SEQUENCE {} RESTART"
                                   .format(sequence))
        test_db.close()

    def add_author(self, name, bio=None):
        """Add an author to the database.

        Keyword arguments:
        name -- the name of the author. Required.
        bio -- short biography for the user. Optional.
        """

        with psycopg2.connect(dbname=self._dbname) as test_db:
            with test_db.cursor() as cursor:
                cursor.execute("""INSERT INTO authors (name, bio)
                               VALUES (%s, %s)""", (name, bio))
        test_db.close()

    def add_article(self, author, title, slug):
        """Add an article to the database.

        Keyword arguments:
        author -- the name of the author. Required. Assumed to be an author
                  that already exists in the database.
        title -- the article title. Required.
        slug -- the article slug. Required.
        """
        with psycopg2.connect(dbname=self._dbname) as test_db:
            with test_db.cursor() as cursor:
                cursor.execute("""INSERT INTO articles (author, title, slug)
                               SELECT id, %s, %s from authors
                               where name = %s""", (title, slug, author))
        test_db.close()

    def add_log(self, path, method="GET", status="200 OK", timestamp=None):
        """Add a access log entry into the database.

        Keyword arguments:
        path -- path part of URL that was accessed. Required.
        method -- the HTTP method used to access the path.
                  Optional. Defaults to GET
        status -- the reponse status of executing the request.
                  Optional. Defaults to "200 OK".
        timestamp -- the date/time the URL was accessed.
                     Optional. Defaults to time of insertion of row into db.
        """
        with psycopg2.connect(dbname=self._dbname) as test_db:
            with test_db.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO log (path, method, status, time)
                    VALUES (%s, %s, %s, %s)""",
                    (path, method, status, timestamp))
        test_db.close()
