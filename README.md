# Udacity Project - Log Analysis

Note: the instructions below use commands ```python``` and ```pip```. Please replace these as appropriate depending on your python installation (e.g. ```python3``` or ```pip3```).

## Prerequisites
Note: The version requirements below are so strict because this project was built with specific versions of tools and libraries and has only been tested with those versions.

### Global Prerequisites
* python (v3.6.1)

### Distribution Prerequisites
* wheel (v0.29.0): ```pip install wheel==0.29.0```

### Usage Prerequisites
(these dependencies will be installed when installing the distribution wheel)
* psycopg2 (v2.7.1): ```pip install psycopg2==2.7.1```

### Testing Prerequisites
* coverage (v4.4.1): ```pip install coverage==4.4.1```

## Distribution
To create distributable wheel, in the project root:
```
$> python setup.py bdist_wheel
```
This will create a ```dist``` directory and a wheel archive within it.

## Installation
To install the wheel:
```
$> pip install <wheel_file>
```
where ```<wheel_file>``` is the distribution wheel (see above).

## Testing
To run tests, in the project root directory:
```
$> python setup.py test
```

To produce code coverage report, add the movie_project packge to your python library path, and from the project root directory:
__TODO__: UPDATE WITH LATEST OUTPUT
```
$> coverage run -m unittest discover -s "test" -p "*_test.py"
[('Ursula La Multa', 507594), ('Rudolf von Treppenwitz', 423457), ('Anonymous Contributor', 170098), ('Markoff Chaney', 84557)]
.
----------------------------------------------------------------------
Ran 1 test in 1.246s

OK
$> coverage report --omit=/usr/*
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
src/logs_analysis/__init__.py              2      0   100%
src/logs_analysis/db_report.py            17      1    94%
test/logs_analysis/__init__.py             2      0   100%
test/logs_analysis/db_report_test.py       8      0   100%
----------------------------------------------------------
TOTAL                                     29      1    97%
```

## Database design
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
__Description__: Article access log, detailing (among other metadata) accessor IP address, resource accessed and date/time of access.

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
