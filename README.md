# Udacity Project - Log Analysis

__Note__: the instructions below use commands `python3` and `pip3`. Please replace these as appropriate depending on your python installation (e.g. `python` or `pip`).

## Prerequisites
__Note__: The version requirements below are so strict because this project was built with specific versions of tools and libraries and has only been tested with those versions.

### Global Prerequisites
* python (v3.5.2)

### Distribution Prerequisites
* wheel (v0.29.0): `pip3 install wheel==0.29.0`

### Database Prerequisites
The database must be as provided in the VM for this course.

The additional views required by this module must be created. To create the views, from the project root:

```
psql -d news -f init/createViews.sql
```

__Note__: the sql for the views is not explicitly listed in this README to ensure that the code in this document does not get out of step with that in the actual sql file. To see the sql look at the `init/createViews.sql` file.

To allow the unit tests to run a test database must be created. From the project root:
```
psql -f init/createTestDatabase.sql
psql -d news_test -f init/createViews.sql
```

### Usage Prerequisites
(these dependencies will be installed when installing the distribution wheel)
* psycopg2 (v2.7.1): `pip3 install psycopg2==2.7.1`

### Testing Prerequisites
* coverage (v4.4.1): `pip3 install coverage==4.4.1`

## Distribution
To create distributable wheel, in the project root:
```
$> python3 setup.py bdist_wheel
```
This will create a `dist` directory and a wheel archive within it.

## Installation
To install the wheel from the project root directory:
```
$> pip3 install dist/<wheel_file>
```
where `<wheel_file>` is the file name of the distribution wheel (see above).

Installation will create a script called 'logs_analysis'

## Usage
Once installed, usage can be found by running:

```
$> logs_analysis -h
usage: logs_analysis [-h] [--articles N] [--authors N] [--errors F]
                     [--db name]

Displays analysis of a news database.

optional arguments:
  -h, --help    show this help message and exit
  --articles N  Show most popular N articles (default 3).
  --authors N   Show the most popular N authors (default all).
  --errors F    Show dates on which the %age of errors is greater than F
                (default 1.0).
  --db name     sets the name of the database to report upon (default 'news').
```

To generate the default analysis output:
```
$> logs_analysis
```

When run within the VM for this course, the above command will produce the following output:

```

The most popular 3 articles are:
'Candidate is jerk, alleges rival' - 338,647 views
'Bears love berries, alleges bear' - 253,801 views
'Bad things gone, say good people' - 170,098 views

The most popular authors are:
'Ursula La Multa' - 507,594 views
'Rudolf von Treppenwitz' - 423,457 views
'Anonymous Contributor' - 170,098 views
'Markoff Chaney' - 84,557 views

The days on which more than 1.0% of requests led to errors:
Sun 17 July 2016 - 2.26% errors out of 55,907 requests
```

## Testing
__Note__: Tests are not included in the distributable wheel, so the tests below must be run when the distributable is __not__ installed.

To run tests, in the project root directory:
```
$> python3 setup.py test
```

To produce code coverage report, add the logs_analysis packge to your python library path (e.g. `export PYTHONPATH=src`), and from the project root directory:
```
coverage run -m unittest discover -s "test" -p "*_test.py"
.........
----------------------------------------------------------------------
Ran 9 tests in 0.558s

OK
$> coverage report --omit=/usr/*
Name                                          Stmts   Miss  Cover
-----------------------------------------------------------------
src/logs_analysis/__init__.py                     2      0   100%
src/logs_analysis/db_report.py                   39      0   100%
test/logs_analysis/__init__.py                    2      0   100%
test/logs_analysis/db_report_test.py            199      0   100%
test/logs_analysis/db_report_test_helper.py      29      0   100%
-----------------------------------------------------------------
TOTAL                                           271      0   100%
```

## Uninstall
To uninstall this package:
```
$> pip3 uninstall logs-analysis
```

## Known Issues
* This application only supports PostgreSQL as dbms, and assumes it is run locally to the PostgreSQL database installation, as provided by within course's VM.

* The application must be run as a user that has been granted access to the database though [PostgreSQL's peer authentication mechanism](https://www.postgresql.org/docs/9.5/static/auth-methods.html#AUTH-PEER).

* The application does not support username/password access to the database.

* Coverage results do not include code that is not touched by any of the tests.

## Revision History
* 1.0.0
    * first release

## Appendix: Implementation notes
The code has been structured as a project to be packaged and installed using setuptools. Whilst the code can be run directly from the project directory, it is recommended that a distribution is created and installed as described in the sections above.

Database access uses the `psycopg2` library, and specifically the [context manager pattern provided by that library](http://initd.org/psycopg/docs/usage.html?highlight=context#with-statement). So, it takes advantage of transactional commit, rollback and resource management provided by using the python `with` statement.

The project's `sql` directory provides the initial scripts that were used to create and test the sql for this solution to the project. This directory is for information only.

The `log_ext` view (as created in `init/createViews.sql`) ensures that the timezone is included when extracting the date from the `log` table's time column. This is to avoid ambiguity as to when the log entry actually occurred.

Database access code can be found in `src/logs_analysis/db_report.py`.

Code for formatting of the resultsets for text output can be found in `src/logs_analysis/news_text_report.py`.

The command line application code can be found in `src/logs_analysis/cmd_line_app.py`.

The main script can be found in `src/logs_analysis/__main__.py`.

## Appendix: Database design
The information below was derived from inspecting the database provided as the project starting point (`newsdata.sql`).

Column definitions below are listed in required (__bold__), optional with default (*__bold italic__*), optional (_italic_) order. Each definition will contain a description and then type and constraint information.

### `articles` table
__Description__: List of articles, each identified by a unique id. Each row contains the article text and metadata (e.g. author, date/time added).

__Columns__:
* __id__:
    * unique id for the article.
    * integer, primary key, required.
    * backed by sequence `articles_id_seq`.
* __author__:
    * id of the author that wrote this article.
    * integer, foreign key, required.
* __title__:
     * the article's title.
     * text, required.
* __slug__:
     * the article's short name. Used to reference article as a resource in URL (e.g. `/article/<slug>`).
     * text, required.
*    *__time__*:
    * the date/time that the article was added.
    * timestamp, optional, defaults to database insert time.
* _body_:
     * the full article text.
     * text, optional.
* _lead_:
    * the article's lead summary encapsulating the article's main ideas in order to capture the reader's attention.
    * text, optional.

### `authors` table
__Description__: List of authors of articles, along with author metadata (bio).

__Columns__:
* __id__:
    * unique id for the author.
    * integer, primary key, required.
    * backed by sequence `authors_id_seq`.
* __name__:
    * the author's full name.
    * text, required.
* _bio_:
    * short biography of the author
    * text, optional.

### `log` table
__Description__: Article access log, detailing (as well as other metadata) accessor IP address, resource accessed and date/time of access.

__Columns__:
* __id__
    * unique id for the log entry.
    * integer, primary key.
    * backed by sequence `log_id_seq`.
* *__time__*
    * the date/time that the log entry was generated.
    * timestamp, optional, defaults to database insert time.
* _path_
    * URL path to resource accessed.
    * text, optional.
* _ip_
    * IP address exposed by the computer accessing the resource.
    * IP address, optional.
* _method_
    * The HTTP method used to access the resource. E.g. 'GET', 'POST'.
    * text, optional.
* _status_
    * The HTTP status code and code description response from the server for the access request. E.g. '200 OK'.
