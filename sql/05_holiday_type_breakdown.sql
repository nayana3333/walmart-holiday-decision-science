/* Holiday-type labels follow the competition's documented flagged weeks.
   The December flags are the week after Christmas, not Christmas week. */
WITH labelled AS (
 SELECT *, CASE
  WHEN substr(date,6,5) IN ('02-12','02-11','02-10') THEN 'Super Bowl'
  WHEN substr(date,6,5) IN ('09-10','09-09','09-07') THEN 'Labor Day'
  WHEN substr(date,6,5) IN ('11-26','11-25','11-23') THEN 'Thanksgiving'
  WHEN substr(date,6,5) IN ('12-31','12-30') THEN 'Post-Christmas flagged week'
  END holiday_type
 FROM sales WHERE holiday_flag=1
), regular AS (SELECT AVG(weekly_sales) avg_regular FROM sales WHERE holiday_flag=0)
SELECT holiday_type, COUNT(DISTINCT date) occurrence_weeks,
 ROUND(AVG(weekly_sales),0) avg_store_sales,
 ROUND((AVG(weekly_sales)-avg_regular)/avg_regular*100,1) lift_vs_regular_pct
FROM labelled CROSS JOIN regular
GROUP BY holiday_type ORDER BY avg_store_sales DESC;
