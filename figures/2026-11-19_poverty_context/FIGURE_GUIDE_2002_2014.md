# Latin America poverty context, 2002–2014

Slide asset: `latin_america_poverty_2002_2014.png`; editable version: `latin_america_poverty_2002_2014.svg`; underlying plotted values: `poverty_chart_values_2002_2014.csv`; rebuild with `build_2002_2014.py`.

**Measure and source:** national poverty headcount below USD 6.85 per person per day at 2017 PPP. [SEDLAC September 2024 poverty workbook](https://www.cedlas.econo.unlp.edu.ar/wp/en/statistics/sedlac/statistics-3/), sheet `poverty USD6.85`, national `FGT(0)` column. The downloaded workbook is `work/raw/sedlac_poverty.xlsx`.

**Why 2002:** it is the earliest year for which 13 countries in this workbook have national survey observations at or before the starting year and at or after 2014. The fixed group is Bolivia, Brazil, Colombia, Costa Rica, Dominican Republic, El Salvador, Guatemala, Honduras, Mexico, Nicaragua, Panama, Paraguay, and Peru. Ecuador begins in 2003 and Uruguay's national series begins in 2006; Chile ends in 2013; Argentina is urban-only in this workbook. The mean is an unweighted average of these 13 countries, not a population-weighted poverty rate for all Latin America.

**Drawing:** dots denote observed survey years. Country lines connect observations. Missing interior years are linearly interpolated to calculate the fixed-country mean, and the CSV marks observed versus interpolated values. No values are extrapolated beyond a country's observed range.

**Endpoint values:** mean 50.2% in 2002 and 33.5% in 2014; Brazil 47.3% to 23.2%; Mexico 47.0% to 40.3%. Thus Mexico's 2002–2006 decline is visible, while its 2006–2014 rate is roughly flat. These are descriptive comparisons, not CCT impact estimates.

**Comparability:** Brazil uses the original PNAD `With Rural North` segment through 2014 rather than switching to the overlapping PNAD Continua series. Several countries have survey or income-method changes within the window. The US$6.85 (2017 PPP) poverty threshold and SWIID Gini figures use different sources and concepts; do not equate their levels.
