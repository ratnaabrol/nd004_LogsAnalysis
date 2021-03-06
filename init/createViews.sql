-- view of all the articles shown as accessed in the log augmented by the article slug which has been extracted from the path
create view accessed_articles as
  select substr(path, char_length('/article/') + 1) as derived_slug, method, ip, time
    from log
    where path like '/article/%' and status = '200 OK';

-- view of all articles shown as accessed in the log augmented by article and author information
create view accessed_articles_ext as
  select aa.*, articles.id as article, articles.author as author
    from accessed_articles as aa, articles
    where aa.derived_slug = articles.slug;

-- view of all log entries augmented with the date the entry took place and whether the entry produced a success or failure status
create view log_ext as
  select *, date_trunc('day', time) as date, status = '200 OK' as status_ok, status != '200 OK' as status_nok from log;
