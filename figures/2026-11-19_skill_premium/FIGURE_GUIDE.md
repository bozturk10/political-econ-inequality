# Education wage premium: Brazil and Mexico

## Measure and source

The figure uses the `wagegaps` sheet of [SEDLAC's November 2026 wages and hours workbook](https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2026_Act1_wages_hours_LAC.xlsx), produced by CEDLAS and the World Bank. The workbook labels the indicator **“Ratio of hourly wages by educational groups. Prime-age males.”** The plotted ratio is high education divided by low education; a value of 4 means the high-education group's hourly wage is four times the low-education group's.

The [SEDLAC methodological guide](https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/Methodological_Guide_v201404.pdf) defines low as 0–8 completed years of schooling, medium as 9–13, and high as 14 or more. It cautions that survey coverage and questionnaires can change within a country and between countries.

| Country and chosen window | First observed ratio | Last observed ratio | Change |
| --- | ---: | ---: | ---: |
| Brazil, 2003–2014 | 6.168 (2003) | 4.359 (2014) | −29.3% |
| Mexico, 1997–2014 | 3.748 (1998) | 4.197 (2014) | +12.0% |

Mexico has no 1997 observation in this series. The figure uses 1998 as its first observed year and does not estimate 1997. There are no Mexican observations for 2003–2007, and no Brazilian 2010 observation. The dotted connectors indicate missing years, not estimated values.

For Brazil, the 2004 row with rural North coverage is selected to match later PNAD rows. The 2003 observation precedes that geographic expansion. The separate PNADC sequence for 2012 onward is not spliced into the PNAD series. The tidy CSV records the source workbook row for every plotted value.

## Interpretation for the slide

The existing slide headline **“The skill premium fell in both, but from different ends”** is not supported by this comparable high/low ratio over the selected study windows. Brazil's measured ratio fell; Mexico's ended above its first in-window observation. The Mexican path fluctuates, so the conclusion is sensitive to choosing a different start year: 2000–2014, for example, yields a decline. The 1997–2014 window should therefore be stated explicitly.

The ratio alone cannot establish whether low-skilled wages rose or high-skilled wages fell in real terms. The companion figure `02_real_hourly_wages_by_education.png` uses the workbook's `wage_1` sheet (nominal hourly wages by education) and [World Bank WDI consumer price index, `FP.CPI.TOTL`](https://data.worldbank.org/indicator/FP.CPI.TOTL). Each nominal wage is divided by that country's annual CPI and multiplied by 100 to express it in 2010-price local currency. Each education group's first observed year is then indexed to 100. The [calculation CSV](sedlac_real_hourly_wage_by_education_brazil_mexico.csv) retains the nominal wage, CPI, deflated wage, index and source row.

| Country and observed endpoints | Low education | Middle education | High education |
| --- | ---: | ---: | ---: |
| Brazil, 2003–2014 | +69.2% | +34.1% | +18.8% |
| Mexico, 1998–2014 | −12.6% | −17.7% | −9.7% |

Thus Brazil's low-education wage rose fastest in real terms. In Mexico, all three groups' real wages declined between the first and last observed years; the low-education decline was larger than the high-education decline. This does **not** reproduce the slide's “compression from the top” claim for the selected Mexico window. The result is start-year sensitive: using 2000 instead gives Mexico low −6.7%, middle −19.0%, high −19.7% through 2014.

The `wage_1` groups include all sexes and ages represented in the source, unlike the `wagegaps` series for prime-age males. The two figures should not be presented as an exact decomposition of the same population. Brazil's PNAD expansion to the rural North in 2004 and missing survey years still limit trend interpretation. CPI adjustment and these descriptive changes do not identify a causal effect of wage policy or education expansion.

ILOSTAT also offers an annual table titled **“Average hourly earnings of employees by sex, education and currency.”** The SEDLAC wage-gap series was used here because its historical survey observations and exact high/low ratios can be traced directly through the chosen periods.
