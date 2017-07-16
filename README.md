# Udacity Project - Log Analysis
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
  * the article's short name.
  * text, required.
* *__time__*:
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
