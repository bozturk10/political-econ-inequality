# Welfare mechanism data notes

## Out-of-pocket health spending

- Series: WHO Global Health Expenditure Database, distributed by World Bank WDI as `SH.XPD.OOPC.CH.ZS`.
- Official indicator: https://data.worldbank.org/indicator/SH.XPD.OOPC.CH.ZS
- Local CSV: `welfare_oop_health_2000_2014.csv`, annual data for Brazil and Mexico.
- Retrieval caveat: the World Bank API could not be accessed from this environment. Numeric values were transcribed from openly accessible mirrors of the WDI/WHO series (https://economicsbydesign.com/tools/place-based-value/brazil/ and https://economicsbydesign.com/tools/place-based-value/mexico/), which identify the WDI code and report a 2026 data vintage. Confirm against a fresh official export before publication.
- Interpretation: percentage of *all current health expenditure* paid directly by households. It does not itself measure the burden specifically borne by poor households, catastrophic spending, or program beneficiaries.

## UHC service coverage

- Source: WHO/World Bank, *Global Monitoring Report on Universal Health Coverage 2021*, Annex 3, pp. 76–77: https://cdn.who.int/media/docs/default-source/world-health-data-platform/events/tracking-universal-health-coverage-2021-global-monitoring-report_uhc-day.pdf?download=true
- Local CSV: `welfare_uhc_service_coverage_2000_2015.csv`, original reported data at 2000, 2005, 2010, 2015.
- Interpretation: essential health service coverage, not whether the law promises universal access or whether the health system is segmented. The WHO revised this index after 2021; do not join this historical vintage to current 2026 Data360 values.

## Non-contributory expenditure

- ECLAC's programme database provides expenditure as a share of GDP for conditional transfers and non-contributory pensions: https://dds.cepal.org/bpsnc/home ; glossary: https://dds.cepal.org/bpsnc/glossary?bd=cct
- A directly comparable combined national annual series for Brazil and Mexico could not be confirmed. Programme-level values would need a defined programme list, years, and aggregation rules, and missing values would have to be flagged.
- CEPALSTAT's aggregate social expenditure by government function (https://statistics.cepal.org/portal/cepalstat/dashboard.html?area_id=411&indicator_id=3127&lang=en) is broader and should not be labeled non-contributory transfers.
