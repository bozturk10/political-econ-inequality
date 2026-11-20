# Latin America poverty context figure

Files: `latin_america_poverty_2006_2014.png` for the slide, editable `latin_america_poverty_2006_2014.svg`, and `poverty_chart_values.csv` for an audit of observations versus interpolated years.

**Measure:** national headcount rate below USD 6.85 per person per day at 2017 purchasing-power parity. Source: [SEDLAC poverty workbook, September 2024](https://www.cedlas.econo.unlp.edu.ar/wp/en/statistics/sedlac/statistics-3/), sheet `poverty USD6.85`, national `FGT(0)` column. The source workbook is `work/raw/sedlac_poverty.xlsx` in this project.

**Sample:** Bolivia, Brazil, Colombia, Costa Rica, Dominican Republic, Ecuador, El Salvador, Guatemala, Honduras, Mexico, Nicaragua, Panama, Paraguay, Peru, and Uruguay. All have national observations bracketing 2006–2014. Argentina's series in this workbook is urban-only; Chile ends in 2013; Venezuela, Cuba, and Haiti are unavailable in this workbook. This is a 15-country sample, not a population-weighted regional poverty rate.

**Drawing:** Country dots mark observed household-survey years. Country lines connect observed years. The dark 15-country mean is the unweighted average of country values; for missing years, values are linearly interpolated between each country's adjacent observed surveys. The interpolation is for visual continuity and does not create new survey observations. The CSV marks each observed and interpolated value.

**Survey choices and limitations:** Brazil's original PNAD `With Rural North` series is used through 2014, rather than mixing it with overlapping PNAD Continua values from 2012 onward. Uruguay uses only its national series beginning in 2006. Several other country series cross survey or income-method changes in this period, including Costa Rica, Colombia, the Dominican Republic, and Panama. Treat long-run changes as descriptive and avoid attributing them to conditional cash transfers. This poverty figure uses SEDLAC's 2017-PPP threshold, whereas the preceding inequality figure uses SWIID 8.0 Gini estimates; the levels are different concepts and datasets.

At the endpoints, the fixed-sample mean falls from 44.2% in 2006 to 31.3% in 2014; Brazil falls from 41.4% to 23.2%; Mexico moves from 39.7% to 40.3%. These are rounded, descriptive estimates for this source and window.
