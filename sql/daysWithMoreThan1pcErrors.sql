-- NOTE: access_ok and access_not_ok views must be created *before* this query can be run.
select * from (
  select ok_rollup.date,
         coalesce(ok_count,0) as ok_count,
         coalesce(nok_count, 0) as nok_count,
         100 * nok_count::float/(coalesce(ok_count,0) + coalesce(nok_count,0)) as bad_pct
    from (select count(*) as ok_count, date from access_ok group by date) as ok_rollup
    right join (select count(*) as nok_count, date from access_not_ok group by date) as nok_rollup
    on ok_rollup.date = nok_rollup.date) as wrapping_table
  where bad_pct > 1.0;
