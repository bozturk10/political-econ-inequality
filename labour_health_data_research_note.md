# Labour organisation, informality and health: Brazil–Mexico data check

Checked 16 November 2026. Main inequality comparison window: **2008–2014** (see `comparison_window_decision.md`). The indicators below are descriptive covariates or possible mechanisms, not estimates of CCT effects.

## Best usable labour indicators

| Indicator (%; annual observations) | Brazil 2008 | Brazil 2012 | Brazil 2014 | Mexico 2008 | Mexico 2012 | Mexico 2014 |
|---|---:|---:|---:|---:|---:|---:|
| Trade union density, share of employees | 19.4 | 17.7 | 17.8 | 15.6 | 14.0 | 13.6 |
| Informal employment, share of all employment | — | 41.6 | 40.7 | 58.8 | 60.3 | 58.7 |

Source: ILOSTAT bulk downloads [`ILR_TUMT_NOC_RT_A`](https://ilostat.ilo.org/data/bulk/) and [`EMP_NIFL_SEX_RT_A`](https://ilostat.ilo.org/data/bulk/); raw downloads retained in `work/raw/`. Brazil informal employment has a **2009 observation of 46.8%** and a **2011 observation of 42.7%**, but no 2008 or 2010 observations in this file. Do not fill these gaps. Brazil's informal employment source changes after 2015; keep this figure in the 2008–2014 period. The two indicators have different denominators: trade union density covers employees, informal employment covers all employed people. [ILO union definition](https://ilostat.ilo.org/blog/beyond-the-numbers-exploring-the-relationship-between-collective-bargaining-coverage-and-inequality/); [ILO informal employment definition](https://ilostat.ilo.org/data/snapshots/informal-employment-rate/).

Changes in **percentage points**, using observed endpoints: union density Brazil −1.6 (2008–14), Mexico −2.0 (2008–14); informal employment Brazil −0.9 (2012–14), Mexico −1.6 (2012–14). Mexico 2008–14 informal employment is essentially flat (−0.1 pp). Rounded figures above can produce slightly different arithmetic.

Use union **density**, not the number of union organisations. A count can grow through fragmentation or registration changes without implying that more workers are represented. Union density is still only a proxy for bargaining power; collective bargaining coverage may capture a different group of workers.

## Quarterly cross-check: LABLAC

LABLAC (CEDLAS and World Bank) has quarterly informal employment measures for both countries. Its social-security definition is the **share of salaried workers without social security rights**, a different denominator and definition from the ILO annual series above. For Q1 2012 and Q1 2014: Brazil's national PNADC survey 23.0% → 20.9%; Mexico's ENOE survey 55.2% → 53.6%. Brazil's older PME series gives much lower levels (Q1 2012 16.5%, Q1 2014 13.5%) because it covers metropolitan areas; **do not splice PME and PNADC into one national line**. PNADC starts in 2012. [LABLAC tables](https://www.cedlas.econo.unlp.edu.ar/wp/estadisticas/lablac/estadisticas-lablac/); [methodological guide](https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/guide_lablac_eng.pdf).

LABLAC also contains Mexico's union membership among salaried workers (Q2 2008 15.84%, Q1 2012 14.12%, Q1 2014 13.71%) and work-linked health coverage (Q1 2008 56.06%, Q1 2012 52.98%, Q1 2014 54.62%). The corresponding Brazil columns are blank. Thus LABLAC does **not** supply a bilateral union or work-linked health coverage comparison. Work-linked coverage is not the same as access to healthcare services.

## Healthcare access: broad, sparse, and indirect

The WHO/World Bank **UHC service coverage index** is comparable for both countries, but only for reference years 2000, 2005, 2010, 2015, 2017, 2019, 2021 in the 2023 report. Brazil: **76 in 2010 and ≥80 in 2015**. Mexico: **66 in 2010 and 74 in 2015**. This is a **0–100 index**, not a percentage of people with coverage. It combines 14 tracer indicators; it is too broad to attribute to CCTs or to align precisely with the 2008–2014 inequality window. [WHO/World Bank 2023 report, Annex 3](https://iris.who.int/bitstream/handle/10665/374059/9789240080379-eng.pdf); [WHO indicator description](https://www.who.int/data/gho/data/themes/topics/service-coverage/GHO/).

For a CCT-specific healthcare mechanism, a child vaccination or prenatal-visit indicator would be closer to the programmes' conditions, but comparable annual Brazil–Mexico series for 2008–2014 require a separate data check. A generic health-access line should be supplementary context, not a central causal test.

## How this fits the question

The strongest labour alternative to a **direct-transfer explanation** of inequality change is a **labour-income explanation**: changes in earnings at the lower end, formalisation, and bargaining institutions. Informality and union density show that the institutional setting differed and changed, but neither alone shows why the Gini or bottom-20 income share moved. For the presentation, pair these as one contextual labour slide with wage-distribution evidence if available. Keep healthcare as a separate possible CCT pathway, especially when discussing longer-run child outcomes.

Figures: `figures/labour_union_informality_brazil_mexico_2008_2014_zero_baseline.png` uses a 0–100% axis for presentation; `figures/labour_union_informality_brazil_mexico_2008_2014.png` is a zoomed view for inspecting small year-to-year changes. Both are generated by `labour_health_figures.py`.
