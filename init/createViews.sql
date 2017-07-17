-- view of all the articles shown as accessed in the log augmented by the article slug which has been extracted from the path
create view accessed_articles as
  select substr(path, char_length('/article/') + 1) as derived_slug, method, ip, time
    from log
    where path like '/article/%' and status = '200 OK';

-- view of all articles shown as accessed in the log augmented by article and author information
create view accessed_articles_ext as
  select aa.*, articles.title as title, authors.name as author_name
    from accessed_articles as aa, articles, authors
    where aa.derived_slug = articles.slug
      and articles.author = authors.id;

-- view of all the accesses that were ok
create view access_not_ok as
  select *, date_trunc('day', time) as date from log where status != '200 OK';

-- view of all the accesses that were not ok
create view access_ok as
  select *, date_trunc('day', time) as date from log where status = '200 OK';
