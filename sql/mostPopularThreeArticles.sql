-- TODO: extract subselect into view
select title, path, num
  from (select path, substr(path, char_length('/article/') + 1) as slug, count(*) as num from log where path like '/article/%' and status = '200 OK' group by path) as logged_articles,
       articles
  where logged_articles.slug = articles.slug
  order by num desc
  limit 3;
