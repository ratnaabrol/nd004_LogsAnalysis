-- NOTE: access_ok and access_not_ok views must be created *before* this query can be run.
select * from (
  select ok_rollup.date, ok_count, nok_count, 100 * nok_count::float/(ok_count + nok_count) as bad_pc from
    (select count(*) as ok_count, date from access_ok group by date) as ok_rollup,
    (select count(*) as nok_count, date from access_not_ok group by date) as nok_rollup
    where ok_rollup.date = nok_rollup.date) as wrapping_table
  where bad_pc > 1.0;
