-- NOTE: accessed_articles_ext view must be created *before* this query can be run.
select author_name, count(*) as article_count
  from accessed_articles_ext
  group by author_name
  order by article_count desc;
