-- NOTE: accessed_articles_ext view must be created *before* this query can be run.
select articles.title, count(aae.derived_slug) as access_count
  from accessed_articles_ext aae
  right join articles on aae.article = articles.id
  group by aae.article, articles.title
  order by access_count desc
  limit 3;
