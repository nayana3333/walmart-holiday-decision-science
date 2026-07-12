/* 02_economic_sensitivity.sql
   No price column exists, so true price elasticity can't be computed.
   Instead: sensitivity of weekly sales to fuel price, CPI and unemployment
   per store -- the real macro "elasticity" this dataset supports, via
   simple standardized covariance (a lightweight regression-slope proxy
   computable in pure SQL without a stats extension). */
WITH stats AS (
    SELECT store_id, AVG(weekly_sales) avg_sales, AVG(fuel_price) avg_fuel,
        AVG(cpi) avg_cpi, AVG(unemployment) avg_unemp
    FROM sales GROUP BY store_id
),
joined AS (
    SELECT s.store_id, s.weekly_sales, s.fuel_price, s.cpi, s.unemployment,
        st.avg_sales, st.avg_fuel, st.avg_cpi, st.avg_unemp
    FROM sales s JOIN stats st ON st.store_id = s.store_id
)
SELECT store_id,
    ROUND(SUM((weekly_sales-avg_sales)*(fuel_price-avg_fuel)) / NULLIF(SUM((fuel_price-avg_fuel)*(fuel_price-avg_fuel)),0), 0) AS fuel_price_sensitivity,
    ROUND(SUM((weekly_sales-avg_sales)*(unemployment-avg_unemp)) / NULLIF(SUM((unemployment-avg_unemp)*(unemployment-avg_unemp)),0), 0) AS unemployment_sensitivity,
    ROUND(SUM((weekly_sales-avg_sales)*(cpi-avg_cpi)) / NULLIF(SUM((cpi-avg_cpi)*(cpi-avg_cpi)),0), 0) AS cpi_sensitivity
FROM joined GROUP BY store_id ORDER BY unemployment_sensitivity ASC;
