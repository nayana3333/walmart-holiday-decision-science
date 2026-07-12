/* 01_holiday_impact.sql
   Holiday_Flag marks Walmart's known markdown weeks (Super Bowl, Labor Day,
   Thanksgiving, Christmas). This is the promotion-effect analysis this
   dataset actually supports: holiday (promo) weeks vs regular weeks,
   per store, using CTEs + window functions. */
WITH store_avg AS (
    SELECT store_id,
        AVG(CASE WHEN holiday_flag=0 THEN weekly_sales END) AS avg_regular_sales,
        AVG(CASE WHEN holiday_flag=1 THEN weekly_sales END) AS avg_holiday_sales
    FROM sales GROUP BY store_id
)
SELECT store_id, ROUND(avg_regular_sales,0) AS avg_regular_sales,
    ROUND(avg_holiday_sales,0) AS avg_holiday_sales,
    ROUND((avg_holiday_sales-avg_regular_sales)/NULLIF(avg_regular_sales,0)*100,1) AS holiday_lift_pct,
    RANK() OVER (ORDER BY (avg_holiday_sales-avg_regular_sales)/NULLIF(avg_regular_sales,0) DESC) AS lift_rank
FROM store_avg ORDER BY holiday_lift_pct DESC;
