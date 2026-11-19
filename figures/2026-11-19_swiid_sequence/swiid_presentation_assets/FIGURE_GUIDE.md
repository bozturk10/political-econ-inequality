# SWIID 8.0 presentation sequence

Use the PNG files for slides; SVG files are editable vector versions. `03_compact_for_table` and `04_companion_table` have matching dimensions and are designed to sit side by side. `04_companion_table.csv` contains the exact table values.

1. `01_latin_america_market_gini`: all 18 Latin American countries with complete annual SWIID 8.0 market-income Gini observations from 1997 through 2014, plus their **unweighted** annual mean. Brazil and Mexico are highlighted for the transition to the next slide. Cuba has no SWIID 8.0 series; Haiti's series ends before 2014, so neither is included in this balanced comparison.
2. `02_brazil_mexico_market_gini`: the same market-income series, focused on the two cases. Programme-era starts are marked at 2003 for Brazil and 1997 for Mexico.
3. `03_brazil_mexico_market_disposable_gini`: the two market series plus the corresponding disposable-income series. The solid/dashed distinction is income concept; colour is country.
4. `04_companion_table`: rounded start and end Gini values, changes, and the market-minus-disposable redistribution gap for each country's programme-era window.

Source: Frederick Solt, [Standardized World Income Inequality Database (SWIID), version 8.0](https://fsolt.org/swiid/swiid_downloads/), archive file `x_swiid8_0.zip`, downloaded through the [official Harvard Dataverse dataset](https://doi.org/10.7910/DVN/LM4OWF). The extracted `swiid8_0_summary.csv` is in this project's `data` directory. All annual lines are original SWIID 8.0 summary estimates; no intermediate years were interpolated. The four Brazil/Mexico endpoints were cross-checked against the supplied slide and matched exactly.

Market-income Gini is before taxes and transfers; disposable-income Gini is after taxes and transfers. The gap is a descriptive difference between these series, not a causal estimate of the CCT's contribution. Brazil and Mexico have different programme-era start years, so the endpoint changes cover different lengths of time. SWIID values are estimates with uncertainty; the slides show point estimates for clarity.
