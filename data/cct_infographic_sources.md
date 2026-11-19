# CCT infographic data and sources

Figures use English labels and show a 2018 snapshot unless stated otherwise.
Coverage counts include all people in recipient households; they are not counts of individual cash recipients.

## World Bank population denominator

API: https://api.worldbank.org/v2/country/BRA;MEX/indicator/SP.POP.TOTL?date=2018&format=json
- Brazil 2018: 206,107,261
- Mexico 2018: 124,573,711

## Official program sources

- brazil_profile: https://www.mds.gov.br/webarquivos/sala_de_imprensa/boletins/boletim_senarc/2018/Boletim%20Senarc%20N%20%2039_SETEMBRO_2018.pdf
- brazil_rural: https://repositorio.enap.gov.br/bitstream/1/3647/4/15%20Anos%20Bolsa%20Fam%C3%ADlia.pdf
- brazil_rules: https://www.mds.gov.br/webarquivos/sala_de_imprensa/boletins/boletim_bolsa_familia/2018/julho/05072018_boletim_BFInforma.html
- mexico_profile: https://sil.gobernacion.gob.mx/Archivos/Documentos/2018/09/asun_3739965_20180925_1537985977.pdf
- mexico_rural: https://www.diconsa.gob.mx/tf/rc/4o_IL_SEDESOL_2016.pdf
- mexico_gender: https://www.gob.mx/bienestar/articulos/las-mujeres-son-el-pilar-en-la-implementacion-y-practica-de-los-programas-sociales-en-nuestro-pais
- mexico_rules: https://www.coneval.org.mx/EvaluacionDS/PP/CEIPP/IEPSM/Documents/Libro_POP_20.pdf
- mexico_benefits: https://www.bienestar.gob.mx/work/models/Bienestar/Transparencia/InformesPresupuestoEjercido/Primer_Informe_Trimestral_2018.pdf
- brazil_transition: https://www.gov.br/mds/pt-br/noticias-e-conteudos/desenvolvimento-social/noticias-desenvolvimento-social/bolsa-familia-reforca-combate-a-pobreza-e-melhora-seguranca-alimentar-aponta-estudo/40_Caderno_Estudos.pdf
- mexico_transition: https://www.coneval.org.mx/InformesPublicaciones/Documents/FIMyE_19-20.pdf
- wdi_gini: https://api.worldbank.org/v2/country/BRA;MEX/indicator/SI.POV.GINI?date=2004:2014&format=json&per_page=1000
- wdi_bottom20: https://api.worldbank.org/v2/country/BRA;MEX/indicator/SI.DST.FRST.20?date=2004:2014&format=json&per_page=1000
- sedlac_poverty: https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2024_Act1_poverty_LAC.xlsx
- comparative_gini_attribution: https://ipcid.org/sites/default/files/pub/en/IPCWorkingPaper35.pdf
- brazil_later_gini_attribution: https://repositorio.ipea.gov.br/items/53006dfc-16db-46d0-a9bc-212c7121c2af
- brazil_schooling: https://citeseerx.ist.psu.edu/document?doi=08d48e5902fd8137c449c717180f2e626638be03&repid=rep1&type=pdf
- mexico_schooling: https://ageconsearch.umn.edu/record/16409/files/fc010102.pdf
- brazil_health: https://acervodigital.mds.gov.br/xmlui/bitstream/handle/123456789/77/AvaliacaodeImpactoProgramaBolsaFamiliaII.pdf?sequence=1
- mexico_health: https://www.povertyactionlab.org/sites/default/files/research-paper/449%20Progresa%20Health%20Gertler%202001.pdf
- mexico_broader_gini_attribution: https://est.cmq.edu.mx/index.php/est/article/download/467/1203/7439
- mexico_transfer_gini_attribution: https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019148.pdf
- mexico_overall_schooling: https://www.imf.org/-/media/websites/imf/imported-full-text-pdf/external/pubs/ft/wp/2009/_wp09187.pdf
- brazil_bf_launch: https://legislacao.presidencia.gov.br/atos/?ano=2003&ato=33dgXUU50dRpWTa36&numero=132&tipo=MPV

## Snapshot values

- Brazil, August 2018: 13,951,980 recipient households; 44,080,713 people in those households; 89.3% female family heads (MDS/SENARC).
- Brazil, August 2018: 27.38% rural and 72.09% urban recipient households (ENAP, remaining fraction unclassified).
- Brazil, August 2018: R$187.13 mean monthly household payment (MDS/SENARC).
- Mexico, 2018: approximately 6.9 million households and 28 million people (government report).
- Mexico, March 2018: 96% of household program holders were women (Secretaría de Bienestar).
- Mexico, June 2016: 54% rural, 19% semiurban, 26% urban recipient households (SEDESOL, rounded).
- Mexico, first half 2018: MXN 335 monthly food support and MXN 140 food supplement; educational grants varied (PROSPERA budget report).

Ratios are rounded; source dates and settlement classifications differ. Monetary amounts are nominal and should not be compared as equivalent purchasing power.

## Observed country-level change: 2004–2014

The script reads the three project CSV extracts rather than hardcoding these values. These are observed national survey indicators, not estimated effects of CCTs. Relative percentage change is calculated as (2014 value − 2004 value) / 2004 value × 100; it differs from percentage-point change.

| Indicator | Brazil 2004 → 2014 | Mexico 2004 → 2014 | Unit |
|---|---:|---:|---|
| WDI Gini index | 56.5 → 52.1 (−4.4 points; −7.8%) | 50.3 → 48.9 (−1.4 points; −2.8%) | 0–100 index points |
| WDI bottom-20 income share | 2.9 → 3.6 (+0.7 pp; +24.1%) | 4.0 → 4.7 (+0.7 pp; +17.5%) | percent and percentage points |
| SEDLAC rural minus urban poverty headcount | 28.2 → 25.2 (−3.0 pp; −10.5%) | 32.7 → 28.4 (−4.3 pp; −13.2%) | percentage points |

The underlying SEDLAC poverty rates (percent of each area's population below the line) are: Brazil 2004 rural 70.7%, urban 42.5%; 2014 rural 45.9%, urban 20.7%. Mexico 2004 rural 69.2%, urban 36.5%; 2014 rural 62.2%, urban 33.8%. The figure calculates rural minus urban for each year.

SEDLAC poverty line: $6.85 per person per day in 2017 PPP. The gap is rural poverty incidence minus urban incidence. The periods 2004–2014 avoid Mexico's major 2014–2016 ENIGH survey break and Brazil's later PNAD/PNAD Contínua transition. These series still reflect different national surveys and are descriptive, not a common causal design.

## Research outcomes shown in the infographic

[1] Soares et al. (2007), *Conditional Cash Transfers in Brazil, Chile and Mexico*: CCT income-source decomposition attributes 20.8% of Brazil's observed 1995–2004 Gini decline and 20.5% of Mexico's observed 1996–2004 decline to CCTs. The first years are survey baselines, not program start dates. Brazil's Bolsa Família was created in October 2003 by consolidating earlier transfers; therefore, do not describe the 20.8% as a Bolsa Família-only effect over 1995–2004. This is an accounting decomposition, not an experimental causal estimate. https://ipcid.org/sites/default/files/pub/en/IPCWorkingPaper35.pdf Launch law: https://legislacao.presidencia.gov.br/atos/?ano=2003&ato=33dgXUU50dRpWTa36&numero=132&tipo=MPV
[2] Souza et al. (2019), IPEA: Bolsa Família accounts for about 17% of Brazil's observed Gini reduction in 2001–2006 and about 10% in 2001–2015. The 2001 survey is a prelaunch baseline; the program began in 2003. Income-source decomposition, not causal. https://repositorio.ipea.gov.br/items/53006dfc-16db-46d0-a9bc-212c7121c2af
[3] de Brauw et al. (2014), IFPRI: Brazil 2005–2009 matched panel estimates +4.5 percentage points school participation among ages 6–17 overall (significant only at 10%); +8.2 pp for girls and +7.4 pp in rural areas. These are percentage points per the body and Table 5.1 of the study. https://citeseerx.ist.psu.edu/document?doi=08d48e5902fd8137c449c717180f2e626638be03&repid=rep1&type=pdf
[4] Schultz, IFPRI: Mexico early rural Progresa randomized rollout, 1997/98 baseline and 1998–99 follow-up; panel secondary-school enrollment effect +9.3 percentage points for girls and +5.8 pp for boys. These findings do not describe national enrollment. https://ageconsearch.umn.edu/record/16409/files/fc010102.pdf
[5] Brazil MDS/IFPRI AIBF-II evaluation (2005–2009): on-time second DPT dose +15.5 percentage points among children; third dose +26 pp. These are program evaluation estimates, not a national health-access rate. https://acervodigital.mds.gov.br/xmlui/bitstream/handle/123456789/77/AvaliacaodeImpactoProgramaBolsaFamiliaII.pdf?sequence=1
[6] Gertler and Boyce (2001): Mexico clinic administrative data, 1996–1998; difference-in-differences estimate +2.09 visits per clinic per day or +18.2% in Progresa localities. Visits include beneficiaries and nonbeneficiaries in clinic catchments. This is utilization, not national health coverage. https://www.povertyactionlab.org/sites/default/files/research-paper/449%20Progresa%20Health%20Gertler%202001.pdf
[7] Aguilar-Gutiérrez (2016), *Economía, Sociedad y Territorio*, Table 7: 11.15% of Mexico's 2000–2012 Gini decline is attributed to 'Oportunidades-type public programs' in an income-source decomposition of ENIGH microdata. The paper's footnote 4 explicitly groups benefits from Oportunidades and other government programs under this label. It is not an Oportunidades-only estimate or a causal effect. https://est.cmq.edu.mx/index.php/est/article/download/467/1203/7439
[8] Lambert and Park (2019), IMF, Figure 10 / Section 4.4: in 2016 Prospera and non-contributory old-age pensions jointly account for 73% of the Gini reduction due to government transfers. The denominator is the transfer-induced Gini effect, not Mexico's total observed Gini decline; the programs are not separately quantified by that figure. https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019148.pdf
[9] Bornhorst (2009), IMF Working Paper 09/187: using the rural Progresa randomized rollout data, the observed treatment-versus-control difference estimator yields +5.4 percentage points in overall school enrollment for eligible children ages 10–16. This is the measured estimate, not the paper's +8.1 pp microsimulation. Survey waves span 1997–1999. It is not a national school-enrollment change. https://www.imf.org/-/media/websites/imf/imported-full-text-pdf/external/pubs/ft/wp/2009/_wp09187.pdf

## Deliberate omissions

A comparable bottom-50 income share is not in the WDI series used here. WID provides bottom-50 *pre-tax national income* shares, a different income concept from the WDI survey-based bottom-20 share. Combining them in the same delta panel would be misleading. The infographic also does not present a national healthcare-access effect because the available CCT evaluations measure service use in selected samples rather than a national access rate.
