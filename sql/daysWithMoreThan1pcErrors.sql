-- NOTE: log_ext view must be created *before* this query can be run.
select * from (
  select date,
         100 * count(case when status_nok = true then 1 else NULL end)::float/count(*) as nok_pct,
         count (*) as count_all
      from log_ext group by date) as nok_table
  where nok_pct > 1.0
  order by nok_pct desc;
