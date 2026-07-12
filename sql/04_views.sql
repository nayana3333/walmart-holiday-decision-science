/* 04_views.sql -- governed reporting layer for BI tools */
DROP VIEW IF EXISTS vw_weekly_kpi;
CREATE VIEW vw_weekly_kpi AS
SELECT date, SUM(weekly_sales) total_sales, AVG(weekly_sales) avg_store_sales,
    MAX(holiday_flag) is_holiday_week, AVG(fuel_price) fuel_price, AVG(cpi) cpi, AVG(unemployment) unemployment
FROM sales GROUP BY date;

DROP VIEW IF EXISTS vw_store_segmentation;
CREATE VIEW vw_store_segmentation AS
WITH base AS (
    SELECT store_id, AVG(weekly_sales) avg_sales,
        AVG(weekly_sales*weekly_sales)-AVG(weekly_sales)*AVG(weekly_sales) AS variance
    FROM sales GROUP BY store_id),
holiday AS (
    SELECT store_id, AVG(CASE WHEN holiday_flag=0 THEN weekly_sales END) reg_sales,
        AVG(CASE WHEN holiday_flag=1 THEN weekly_sales END) hol_sales
    FROM sales GROUP BY store_id)
SELECT b.store_id, b.avg_sales,
    (h.hol_sales-h.reg_sales)/NULLIF(h.reg_sales,0)*100 AS holiday_lift_pct,
    CASE WHEN (h.hol_sales-h.reg_sales)/NULLIF(h.reg_sales,0)>=0.10 THEN 'EXPAND HOLIDAY MARKDOWNS'
         WHEN (h.hol_sales-h.reg_sales)/NULLIF(h.reg_sales,0)<0.02 THEN 'REVIEW MARKDOWN ROI'
         ELSE 'MAINTAIN CURRENT STRATEGY' END AS recommendation
FROM base b JOIN holiday h ON h.store_id=b.store_id;
