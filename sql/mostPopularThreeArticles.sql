-- NOTE: accessed_articles_ext view must be created *before* this query can be run.
select title, count(*) as access_count
  from accessed_articles_ext
  group by title
  order by access_count desc
  limit 3;
