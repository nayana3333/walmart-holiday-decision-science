# Walmart Holiday Sales: Decision Brief

## The business question

Where does holiday-period sales strength appear credible enough to investigate further, and which forecasting approach should planners use as a starting point?

This dataset cannot answer price elasticity or markdown ROI because it has no price, discount, margin, or product fields. The work therefore focuses on honest, supportable decisions: holiday-week prioritization, uncertainty, and store-level forecast benchmarking.

## Approach

I built a reproducible pipeline combining SQL analysis, statistical testing, robust regression, time-based forecasting, automated quality checks, and a six-view decision dashboard. All results are generated from 6,435 store-week rows covering 45 stores from 2010–2012.

## Three findings

1. **Flagged weeks show a positive overall association, with moderate confidence.** Sales are 7.84% higher than regular weeks (95% interval: 2.08%–13.67%; p=0.0259). However, this comes from only 10 distinct calendar weeks and does not establish markdown causality.

2. **Store 7 is the clearest expansion-test candidate, not an automatic rollout.** Its observed lift is 19.44% (95% interval: 4.20%–36.46%; nominal p=0.0166). Seven stores pass the unadjusted exploratory screen, but none survives correction for testing 45 stores; all store findings therefore remain exploratory.

3. **The feature model wins at aggregate level, but a simple baseline remains competitive.** On the last 20 weeks, feature OLS records 1.87% MAPE versus 2.24% for seasonal naive. Across stores plus aggregate, the split is close—24 wins to 22—so model choice should remain store-specific.

## Recommendation

Run a controlled holiday-markdown pilot in Store 7 with matched comparison stores. Predefine margin-aware success metrics. Keep seasonal naive as the governance baseline; adopt the feature model only where repeated backtests show a durable advantage.

## Critical data-quality insight

The dataset’s “Christmas” flag is actually the week after Christmas. Those two weeks average 7.7% below regular weeks, so treating the flag as Christmas demand would mislead planning.

## What I would add next

Product-level price and units, markdown depth and timing, margin, inventory/stockouts, local events, competitor prices, and a randomized or quasi-experimental control design. For forecasting, I would add rolling-origin backtests and operational forecasts for macro inputs.
