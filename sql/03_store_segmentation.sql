/* 03_store_segmentation.sql
   Segments stores into an action recommendation using holiday lift +
   sales consistency (coefficient of variation), the decision-science
   output equivalent to the original pricing segmentation. */
WITH base AS (
    SELECT store_id, AVG(weekly_sales) avg_sales,
        AVG(weekly_sales*weekly_sales) - AVG(weekly_sales)*AVG(weekly_sales) AS variance
    FROM sales GROUP BY store_id
),
holiday AS (
    SELECT store_id,
        AVG(CASE WHEN holiday_flag=0 THEN weekly_sales END) AS reg_sales,
        AVG(CASE WHEN holiday_flag=1 THEN weekly_sales END) AS hol_sales
    FROM sales GROUP BY store_id
)
SELECT b.store_id, ROUND(b.avg_sales,0) AS avg_weekly_sales,
    ROUND(SQRT(b.variance)/NULLIF(b.avg_sales,0)*100,1) AS coeff_of_variation_pct,
    ROUND((h.hol_sales-h.reg_sales)/NULLIF(h.reg_sales,0)*100,1) AS holiday_lift_pct,
    CASE
        WHEN (h.hol_sales-h.reg_sales)/NULLIF(h.reg_sales,0) >= 0.10 THEN 'EXPAND HOLIDAY MARKDOWNS'
        WHEN (h.hol_sales-h.reg_sales)/NULLIF(h.reg_sales,0) < 0.02 THEN 'REVIEW MARKDOWN ROI'
        ELSE 'MAINTAIN CURRENT STRATEGY'
    END AS recommendation,
    NTILE(4) OVER (ORDER BY b.avg_sales DESC) AS size_quartile
FROM base b JOIN holiday h ON h.store_id=b.store_id
ORDER BY holiday_lift_pct DESC;
