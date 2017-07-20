-- NOTE: accessed_articles_ext view must be created *before* this query can be run.
select authors.name as author_name, count(aae.derived_slug) as article_count
  from accessed_articles_ext as aae
  right join authors on aae.author = authors.id
  group by authors.name
  order by article_count desc;
