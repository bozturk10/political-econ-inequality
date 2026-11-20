# CCT comparison: program rules and 2014 reach within the 1997–2014 study window

Rebuild offline with `python3 scripts/cct_2014_snapshot.py`. The script reads
`data/cct_2014_snapshot.csv` and writes `figures/cct_program_comparison_2014_snapshot.svg`.
It also writes a 2400 px PNG if `rsvg-convert` is installed. The input file freezes
the published figures and World Bank population denominator; rebuilding does not
depend on the present state of external websites.

## Program details shown above the reach figures

The details summarize rules in force during the study window. Brazil's 2014
requirements included 85% school attendance for children aged 6–15 and 75%
for ages 16–17, plus child vaccination and nutritional monitoring, prenatal
care and postpartum follow-up. The [2014 federal monitoring report](https://www.gov.br/planejamento/pt-br/assuntos/planejamento/plano-plurianual/arquivos/planos-plurianuais-anteriores/ppa-2012-2015/relatorios-de-monitoramento/relatorio-anual-de-avaliacao-do-ppa-2012-2015-ano-base-2014/tomo-i-programas-sociais.pdf)
and [Bolsa Família regulations](https://legis.senado.gov.br/norma/407869/publicacao/15734033)
support these items. Benefits were paid preferentially to a woman holder;
the Caixa payment card and eligible account routes are described in the
[program law](https://www.caixa.gov.br/downloads/bolsa-familia-documentacao-programa/LEI_N__10_836.PDF)
and [decree](https://www.caixa.gov.br/downloads/bolsa-familia-documentacao-programa/DECRETO_N__5_209.PDF).

Mexico's [2014 Oportunidades operating rules](https://dof.gob.mx/reglas_2014/SEDESOL_301213_13.pdf)
require school enrollment and attendance; scheduled health appointments and
community health workshops; and, for the specific older-adult benefit, a
health-service visit every six months. That visit certification also counted
as proof of life. The rules say the named recipient was generally the mother
and allow different payment channels, including payment points and account
credit. Accordingly, the slide does not claim all transfers used bank deposits.

| Input | Brazil | Mexico | Source and timing |
| --- | ---: | ---: | --- |
| Recipient households | 14,003,441 | 6,122,458 | Brazil December 2014, [Caixa 2014 report](https://www.caixa.gov.br/downloads/caixa-relatorio-sustentabilidade/relatorio_de_sustentabilidade_2014.pdf), p. 59; Mexico through September 2014, [CEFP note 074/2014](https://www.cefp.gob.mx/publicaciones/nota/2014/diciembre/notacefp0742014.pdf), p. 4. |
| People in recipient households | 48,694,698 | approximately 27,000,000 | Brazil same Caixa report. Mexico [Secretaría de Salud, 5 February 2015](https://www.gob.mx/salud/prensa/ingresan-al-seguro-popular-tres-millones-de-personas-del-programa-prospera), reporting the then-current 6.1 million families. Mexico is an approximate adjacent-date figure, not a September 2014 count. |
| National population, 2014 | 200,085,127 | 119,784,261 | [World Bank WDI SP.POP.TOTL API](https://api.worldbank.org/v2/country/BRA;MEX/indicator/SP.POP.TOTL?date=2014&format=json), downloaded 19 November 2026. |
| Women among designated holders | 93% | 96% | Brazil 2014 CadÚnico figure in [Brazilian government publication, p. 24](https://www.ba.gov.br/mulheres/sites/site-spm/files/migracao_2024/arquivos/File/Publicacoes/Encarte_Maisigualdadeparaasmulheresbrasileiras.pdf); Mexico April 2014 statement by the program head in [Gaceta Parlamentaria, p. 101](https://gaceta.diputados.gob.mx/PDF/62/2014/abr/20140425.pdf). These are designated benefit holders, not necessarily all household heads. |
| Rural recipient households | 3,796,980 / 13,956,776 classified = 27.2% | 59.2% | Brazil December 2014 MDS/CadÚnico/TABCAD tabulation reproduced in [Aquino et al., Table 1, p. 161](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1088537/1/Joao3.pdf). Table excludes households with no urban/rural response, explaining the difference from the Caixa total. Mexico through September 2014, [CEFP note 074/2014, p. 4](https://www.cefp.gob.mx/publicaciones/nota/2014/diciembre/notacefp0742014.pdf); semiurban 19.1%, urban 21.7%. Definitions of rural differ across countries. |

Displayed population shares are calculated as people in recipient households divided
by World Bank 2014 national population, then rounded to one decimal. They are not
effects of the programs and should not be compared as matched survey estimates.
Mexico's adjacent-date people figure makes its displayed share an approximation.

Program timing: Bolsa Família began in 2003; Mexico's Progresa began in 1997,
became Oportunidades, and was renamed Prospera in 2014. See the [CONEVAL
program history](https://www.coneval.org.mx/EvaluacionDS/PP/CEIPP/IEPSM/Documents/Libro_POP_20.pdf).
