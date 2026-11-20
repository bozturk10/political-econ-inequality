#!/usr/bin/env python3
"""Create source-backed Brazil/Mexico CCT comparison infographics.

Run: python3 scripts/program_comparison_infographics.py
Population denominator is fetched from the World Bank API (SP.POP.TOTL).
Other snapshot values are from the official sources listed in SOURCES below.
"""

from __future__ import annotations

import html
import csv
import json
import shutil
import subprocess
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
DATA = ROOT / "data"
POP_API = "https://api.worldbank.org/v2/country/BRA;MEX/indicator/SP.POP.TOTL?date=2018&format=json"
SOURCES = {
    "brazil_profile": "https://www.mds.gov.br/webarquivos/sala_de_imprensa/boletins/boletim_senarc/2018/Boletim%20Senarc%20N%20%2039_SETEMBRO_2018.pdf",
    "brazil_rural": "https://repositorio.enap.gov.br/bitstream/1/3647/4/15%20Anos%20Bolsa%20Fam%C3%ADlia.pdf",
    "brazil_rules": "https://www.mds.gov.br/webarquivos/sala_de_imprensa/boletins/boletim_bolsa_familia/2018/julho/05072018_boletim_BFInforma.html",
    "mexico_profile": "https://sil.gobernacion.gob.mx/Archivos/Documentos/2018/09/asun_3739965_20180925_1537985977.pdf",
    "mexico_rural": "https://www.diconsa.gob.mx/tf/rc/4o_IL_SEDESOL_2016.pdf",
    "mexico_gender": "https://www.gob.mx/bienestar/articulos/las-mujeres-son-el-pilar-en-la-implementacion-y-practica-de-los-programas-sociales-en-nuestro-pais",
    "mexico_rules": "https://www.coneval.org.mx/EvaluacionDS/PP/CEIPP/IEPSM/Documents/Libro_POP_20.pdf",
    "mexico_benefits": "https://www.bienestar.gob.mx/work/models/Bienestar/Transparencia/InformesPresupuestoEjercido/Primer_Informe_Trimestral_2018.pdf",
    "brazil_transition": "https://www.gov.br/mds/pt-br/noticias-e-conteudos/desenvolvimento-social/noticias-desenvolvimento-social/bolsa-familia-reforca-combate-a-pobreza-e-melhora-seguranca-alimentar-aponta-estudo/40_Caderno_Estudos.pdf",
    "mexico_transition": "https://www.coneval.org.mx/InformesPublicaciones/Documents/FIMyE_19-20.pdf",
    "wdi_gini": "https://api.worldbank.org/v2/country/BRA;MEX/indicator/SI.POV.GINI?date=2004:2014&format=json&per_page=1000",
    "wdi_bottom20": "https://api.worldbank.org/v2/country/BRA;MEX/indicator/SI.DST.FRST.20?date=2004:2014&format=json&per_page=1000",
    "sedlac_poverty": "https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2024_Act1_poverty_LAC.xlsx",
    "comparative_gini_attribution": "https://ipcid.org/sites/default/files/pub/en/IPCWorkingPaper35.pdf",
    "brazil_later_gini_attribution": "https://repositorio.ipea.gov.br/items/53006dfc-16db-46d0-a9bc-212c7121c2af",
    "brazil_schooling": "https://citeseerx.ist.psu.edu/document?doi=08d48e5902fd8137c449c717180f2e626638be03&repid=rep1&type=pdf",
    "mexico_schooling": "https://ageconsearch.umn.edu/record/16409/files/fc010102.pdf",
    "brazil_health": "https://acervodigital.mds.gov.br/xmlui/bitstream/handle/123456789/77/AvaliacaodeImpactoProgramaBolsaFamiliaII.pdf?sequence=1",
    "mexico_health": "https://www.povertyactionlab.org/sites/default/files/research-paper/449%20Progresa%20Health%20Gertler%202001.pdf",
    "mexico_broader_gini_attribution": "https://est.cmq.edu.mx/index.php/est/article/download/467/1203/7439",
    "mexico_transfer_gini_attribution": "https://www.imf.org/-/media/files/publications/wp/2019/wpiea2019148.pdf",
    "mexico_overall_schooling": "https://www.imf.org/-/media/websites/imf/imported-full-text-pdf/external/pubs/ft/wp/2009/_wp09187.pdf",
    "brazil_bf_launch": "https://legislacao.presidencia.gov.br/atos/?ano=2003&ato=33dgXUU50dRpWTa36&numero=132&tipo=MPV",
}


def population_2018() -> dict[str, int]:
    with urlopen(POP_API, timeout=30) as response:
        payload = json.load(response)
    result = {r["countryiso3code"]: r["value"] for r in payload[1] if r["value"] is not None}
    if not {"BRA", "MEX"} <= result.keys():
        raise RuntimeError("World Bank population response missing Brazil or Mexico")
    return result


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def line(x1, y1, x2, y2, color="#d6dce2", width=1) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def rect(x, y, w, h, fill, rx=0, stroke="none") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'


def txt(x, y, s, size=18, fill="#203040", weight="normal", anchor="start") -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'


def svg_start(w, h) -> list[str]:
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            '<style>text{font-family:Arial,Helvetica,sans-serif}</style>', rect(0, 0, w, h, "#ffffff")]


def bar(parts: list[str], x: int, y: int, value: float, color: str, max_width=380) -> None:
    parts += [rect(x, y, max_width, 14, "#e9edf0", 7), rect(x, y, round(max_width * value / 100, 1), 14, color, 7)]


def country_changes() -> dict[str, dict[str, tuple[float, float]]]:
    """Read the project's WDI and SEDLAC extracts; use observed 2004/2014 values."""
    specs = [
        ("gini", "gini_brazil_mexico_1997_2026.csv", "country_code", "gini_index_0_100"),
        ("bottom20", "bottom20_income_share.csv", "country_code", "income_share_percent"),
        ("poverty_gap", "sedlac_rural_urban_poverty_gap.csv", "country", "rural_minus_urban_pp"),
        ("poverty_rural", "sedlac_rural_urban_poverty_gap.csv", "country", "rural_headcount_percent"),
        ("poverty_urban", "sedlac_rural_urban_poverty_gap.csv", "country", "urban_headcount_percent"),
    ]
    result: dict[str, dict[str, tuple[float, float]]] = {"BRA": {}, "MEX": {}}
    for metric, filename, country_key, value_key in specs:
        with (DATA / filename).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for code, country_name in (("BRA", "Brazil"), ("MEX", "Mexico")):
            country = code if country_key == "country_code" else country_name
            values = {int(row["year"]): float(row[value_key]) for row in rows
                      if row[country_key] == country and int(row["year"]) in (2004, 2014)}
            if set(values) != {2004, 2014}:
                raise ValueError(f"Missing {metric} data for {code} in 2004 or 2014")
            result[code][metric] = (values[2004], values[2014])
    return result


def comparison(population: dict[str, int]) -> Path:
    brazil_people = 44_080_713  # August 2018, beneficiary household members
    mexico_people = 28_000_000  # approximate, 2018 government report
    brazil_share = 100 * brazil_people / population["BRA"]
    mexico_share = 100 * mexico_people / population["MEX"]
    colors = {"BRA": "#147d86", "MEX": "#d77237"}
    p = svg_start(1200, 2140)
    p += [txt(70, 60, "Brazil and Mexico: CCT programs at a glance", 30, weight="bold"),
          txt(70, 91, "2018 snapshot unless otherwise noted  |  Counts refer to households and their members", 16, "#5b6570"),
          line(70, 111, 1130, 111)]
    for code, x, name, program, households, people, share in [
        ("BRA", 70, "BRAZIL", "Bolsa Família", "13.95m", "44.08m", brazil_share),
        ("MEX", 625, "MEXICO", "Prospera", "~6.9m", "~28m", mexico_share),
    ]:
        color = colors[code]
        p += [rect(x, 135, 505, 225, "#f7f9fa", 12),
              rect(x, 135, 7, 225, color),
              txt(x + 25, 170, name, 18, color, "bold"),
              txt(x + 25, 203, program, 24, weight="bold"),
              txt(x + 25, 250, households, 31, color, "bold"),
              txt(x + 25, 273, "households", 14, "#5b6570"),
              txt(x + 270, 250, people, 31, color, "bold"),
              txt(x + 270, 273, "people in covered households", 14, "#5b6570"),
              txt(x + 25, 319, f"~{share:.1f}% of national population", 20, weight="bold")]
        bar(p, x + 25, 329, share, color, 455)
    p += [txt(70, 401, "WHO WAS REACHED?", 19, weight="bold"), line(70, 413, 1130, 413)]
    for x, color, female, rural, rural_year, note in [
        (70, colors["BRA"], 89.3, 27.4, "2018", "Urban: 72.1%"),
        (625, colors["MEX"], 96.0, 54.0, "2016", "Semi-urban: 19%; urban: 26%"),
    ]:
        p += [txt(x, 450, "Women among designated household holders", 16),
              txt(x + 455, 450, f"{female:.1f}%", 18, color, "bold", "end")]
        bar(p, x, 460, female, color, 455)
        p += [txt(x, 522, f"Rural households ({rural_year})", 16),
              txt(x + 455, 522, f"{rural:.1f}%", 18, color, "bold", "end")]
        bar(p, x, 532, rural, color, 455)
        p += [txt(x, 575, note, 14, "#5b6570")]
    p += [txt(70, 626, "PROGRAM DESIGN", 19, weight="bold"), line(70, 638, 1130, 638)]
    for x, color, title, eligibility, conditions, payment in [
        (70, colors["BRA"], "BOLSA FAMÍLIA", ["Income-tested; Cadastro Único", "2018 entry: up to R$89/person, or R$178", "with a child or adolescent"], ["School attendance + child health", "monitoring and prenatal care"], ["Aug 2018 average: R$187/month", "per household; basic + child top-ups"]),
        (625, colors["MEX"], "PROSPERA", ["Income / socioeconomic targeting", "Poverty threshold; rural and urban", "households eligible"], ["School attendance + health visits", "Also had a no-conditions support track"], ["2018: MXN 335/month food support", "+ MXN 140 supplement; school grants vary"]),
    ]:
        p += [rect(x, 658, 505, 280, "#f7f9fa", 12), txt(x + 23, 691, title, 18, color, "bold"),
              txt(x + 23, 722, "ENTRY", 13, "#65717c", "bold")]
        for i, s in enumerate(eligibility): p.append(txt(x + 23, 746 + i * 20, s, 15))
        p.append(txt(x + 23, 808, "CONDITIONS", 13, "#65717c", "bold"))
        for i, s in enumerate(conditions): p.append(txt(x + 23, 831 + i * 19, s, 15))
        p.append(txt(x + 23, 876, "PAYMENT", 13, "#65717c", "bold"))
        for i, s in enumerate(payment): p.append(txt(x + 23, 897 + i * 19, s, 14))
    p += [txt(70, 956, "Coverage includes all members of recipient households; benefits and rural definitions differ.", 14, "#5b6570"),
          txt(70, 1001, "OBSERVED COUNTRY-LEVEL CHANGE", 19, weight="bold"), line(70, 1013, 1130, 1013),
          txt(70, 1040, "2004 to 2014  |  Relative % change uses the 2004 value as its base; not CCT effects", 14, "#5b6570")]
    changes = country_changes()
    for code, x, name in (("BRA", 70, "BRAZIL"), ("MEX", 625, "MEXICO")):
        color = colors[code]
        p += [rect(x, 1055, 505, 315, "#f7f9fa", 12), txt(x + 20, 1085, name, 17, color, "bold")]
        for index, metric, label, unit in [
            (0, "gini", "Gini index", "index points"),
            (1, "bottom20", "Bottom 20% income share", "pp"),
            (2, "poverty_gap", "Rural–urban poverty gap", "pp"),
        ]:
            before, after = changes[code][metric]
            y = 1120 + index * 62
            delta = after - before
            relative_pct = 100 * delta / before
            before_s = f"{before:.1f}"
            after_s = f"{after:.1f}"
            if metric == "poverty_gap":
                rural_2004, rural_2014 = changes[code]["poverty_rural"]
                urban_2004, urban_2014 = changes[code]["poverty_urban"]
                p += [txt(x + 20, y, "Rural − urban poverty rates", 15, weight="bold"),
                      txt(x + 20, y + 26, f"2004   Rural {rural_2004:.1f}% − Urban {urban_2004:.1f}% = {before_s} pp", 15),
                      txt(x + 20, y + 53, f"2014   Rural {rural_2014:.1f}% − Urban {urban_2014:.1f}% = {after_s} pp", 15),
                      txt(x + 480, y + 83, f"Gap change: {delta:+.1f} pp ({relative_pct:+.1f}%)", 14, color, "bold", "end")]
            else:
                p += [txt(x + 20, y, label, 15, weight="bold"),
                      txt(x + 20, y + 24, f"{before_s} → {after_s}", 17),
                      txt(x + 480, y + 24, f"{delta:+.1f} {unit} ({relative_pct:+.1f}%)", 14, color, "bold", "end")]
            if index < 2:
                p.append(line(x + 20, y + 38, x + 485, y + 38, "#e2e8eb"))
    p += [txt(70, 1390, "Poverty rate = population share below US$6.85/day (2017 PPP). Gap = rural minus urban, in percentage points.", 13, "#5b6570"),
          '<g transform="translate(0, 80)">',
          txt(70, 1347, "ESTIMATES FROM THE RESEARCH LITERATURE", 19, weight="bold"),
          line(70, 1359, 1130, 1359),
          txt(70, 1385, "Different studies, samples and periods; compare the definitions, not just the numbers", 14, "#5b6570")]
    for x, code, title, gini, gini_note, school, school_note, health, health_note in [
        (70, "BRA", "BRAZILIAN CCTS (BF FROM 2003)", "20.8% of Gini decline", "1995 baseline → 2004; BF began in 2003 [1]", "+4.5 pp school participation", "Ages 6–17, 2005–09 matched panel; p<0.10 [3]", "+15.5 pp on-time DPT dose 2", "2005–09 impact evaluation; children [5]"),
        (625, "MEX", "PROGRESA / OPORTUNIDADES", "20.5% of Gini decline", "1996–2004; income-source decomposition [1]", "+5.4 pp overall school enrollment", "Ages 10–16, rural Progresa [9]; girls +9.3 pp [4]", "+18.2% clinic visits", "Rural clinics, 1996–98; all local patients [6]"),
    ]:
        color = colors[code]
        p += [rect(x, 1401, 505, 320, "#f7f9fa", 12), txt(x + 20, 1432, title, 16, color, "bold")]
        for index, heading, value, note in [
            (0, "INEQUALITY ATTRIBUTION", gini, gini_note),
            (1, "SCHOOLING", school, school_note),
            (2, "HEALTH SERVICE USE", health, health_note),
        ]:
            y = 1463 + index * 87
            p += [txt(x + 20, y, heading, 12, "#65717c", "bold"),
                  txt(x + 20, y + 27, value, 18, color, "bold"),
                  txt(x + 20, y + 49, note, 13, "#5b6570")]
    p += [txt(70, 1755, "OTHER GINI ATTRIBUTION ESTIMATES", 19, weight="bold"),
          line(70, 1767, 1130, 1767),
          txt(70, 1791, "Study periods and the included transfer programs differ; figures are not directly comparable", 14, "#5b6570"),
          rect(70, 1805, 505, 205, "#f7f9fa", 12),
          txt(90, 1834, "BRAZIL: BOLSA FAMÍLIA (FROM 2003)", 16, colors["BRA"], "bold"),
          txt(90, 1872, "~17%", 24, colors["BRA"], "bold"),
          txt(192, 1872, "of Gini decline, 2001–06 [2]", 15),
          txt(90, 1902, "~10%", 24, colors["BRA"], "bold"),
          txt(192, 1902, "of Gini decline, 2001–15 [2]", 15),
          txt(90, 1940, "Income-source decomposition; 2001 baseline", 13, "#5b6570"),
          txt(90, 1960, "predates the Bolsa Família launch.", 13, "#5b6570"),
          rect(625, 1805, 505, 205, "#f7f9fa", 12),
          txt(645, 1834, "MEXICO: BROADER TRANSFER GROUPS", 16, colors["MEX"], "bold"),
          txt(645, 1872, "11.15%", 24, colors["MEX"], "bold"),
          txt(755, 1872, "of Gini decline, 2000–12 [7]", 15),
          txt(645, 1902, "Oportunidades-type public programs; includes others.", 13, "#5b6570"),
          txt(645, 1940, "73%", 24, colors["MEX"], "bold"),
          txt(724, 1940, "of transfer-related Gini effect, 2016 [8]", 15),
          txt(645, 1967, "Prospera + old-age pensions; not the total Gini decline.", 13, "#5b6570"),
          txt(70, 2042, "All attribution figures are accounting decompositions, not causal estimates. Full references and methods: data/cct_infographic_sources.md.", 12, "#5b6570"),
          txt(70, 2062, "No comparable national health-access effect or bottom-50 share is shown.", 12, "#5b6570"),
          '</g>',
          '</svg>']
    path = FIGURES / "cct_program_comparison_infographic.svg"
    path.write_text("\n".join(p), encoding="utf-8")
    return path


def timeline() -> Path:
    p = svg_start(1600, 900)
    p += [txt(70, 57, "Brazil and Mexico: CCTs across governments", 31, weight="bold"),
          txt(70, 88, "Presidential terms above program timelines, 1997–2026", 17, "#5b6570"),
          line(70, 111, 1530, 111)]
    def px(year: float) -> float:
        return 180 + (year - 1997) / (2026 - 1997) * 1320
    ideology = {
        "left": ("#285aa8", "#ffffff"),
        "centre": ("#c9d1d8", "#203040"),
        "centre_right": ("#e7b35a", "#203040"),
        "right": ("#b23549", "#ffffff"),
    }
    legend = [("Left / centre-left", "left"), ("Centre / mixed", "centre"),
              ("Centre-right", "centre_right"), ("Right", "right")]
    for i, (label, key) in enumerate(legend):
        x = 70 + i * 242
        p += [rect(x, 132, 18, 18, ideology[key][0], 3), txt(x + 27, 147, label, 15)]
    for year in (1997, 2000, 2003, 2006, 2008, 2011, 2014, 2016, 2019, 2021, 2023, 2026):
        xx = px(year)
        p += [line(round(xx, 1), 190, round(xx, 1), 650, "#e6eaed"),
              txt(round(xx, 1), 183, str(year), 13, "#69737c", anchor="middle")]
    def phase(start, end, y, title, year_label="", label_size=15):
        x1, x2 = px(start), px(end)
        p.append(f'<rect x="{x1:.1f}" y="{y}" width="{x2-x1:.1f}" height="58" rx="3" fill="#eef2f5" stroke="#b7c2cb" stroke-width="1.5"/>')
        p.append(txt(round((x1+x2)/2, 1), y + 27, title, label_size, "#203040", "bold", "middle"))
        if year_label: p.append(txt(round((x1+x2)/2, 1), y + 46, year_label, 12, "#5b6570", anchor="middle"))
    def government(start, end, y, name, party, group, size=12):
        x1, x2 = px(start), px(end)
        fill, ink = ideology[group]
        p.append(rect(round(x1, 1), y, round(x2 - x1, 1), 53, fill, 3))
        p.append(txt(round((x1+x2)/2, 1), y + 22, name, size, ink, "bold", "middle"))
        p.append(txt(round((x1+x2)/2, 1), y + 40, party, 11, ink, anchor="middle"))
    p += [txt(70, 230, "MEXICO", 18, "#b85b2c", "bold"),
          txt(70, 267, "Government", 14, "#5b6570"),
          txt(70, 341, "Program", 14, "#5b6570"),
          txt(70, 439, "BRAZIL", 18, "#147d86", "bold"),
          txt(70, 476, "Government", 14, "#5b6570"),
          txt(70, 550, "Program", 14, "#5b6570")]
    # Fractional years approximate the actual inauguration dates, avoiding a
    # false impression that Mexico's handovers occurred on January 1.
    government(1997, 2000.92, 246, "Zedillo", "PRI", "centre")
    government(2000.92, 2006.92, 246, "Fox", "PAN", "centre_right")
    government(2006.92, 2012.92, 246, "Calderón", "PAN", "centre_right")
    government(2012.92, 2018.92, 246, "Peña Nieto", "PRI", "centre")
    government(2018.92, 2024.75, 246, "López Obrador", "Morena", "left")
    government(2024.75, 2026, 246, "Sheinbaum", "Morena", "left", 10)
    phase(1997, 2002, 320, "Progresa", "1997–2002")
    phase(2002, 2014, 320, "Oportunidades", "2002–2014")
    phase(2014, 2019, 320, "Prospera", "2014–2019")
    x1, x2 = px(2019), px(2026)
    p += [f'<rect x="{x1:.1f}" y="320" width="{x2-x1:.1f}" height="58" rx="3" fill="#ffffff" stroke="#9aa8b4" stroke-width="1.5" stroke-dasharray="6 4"/>',
          txt(round((x1+x2)/2, 1), 347, "Benito Juárez scholarships", 14, "#203040", "bold", "middle"),
          txt(round((x1+x2)/2, 1), 366, "redesigned from 2019", 12, "#5b6570", anchor="middle")]
    government(1997, 2003, 455, "F. H. Cardoso", "PSDB", "centre_right")
    government(2003, 2011, 455, "Lula", "PT", "left")
    government(2011, 2016.67, 455, "Dilma", "PT", "left")
    government(2016.67, 2019, 455, "Temer", "MDB", "centre_right")
    government(2019, 2023, 455, "Bolsonaro", "PSL / PL", "right")
    government(2023, 2026, 455, "Lula", "PT", "left")
    phase(2003, 2021, 529, "Bolsa Família", "2003–2021")
    phase(2021, 2023, 529, "Auxílio Brasil", "2021–23", 12)
    phase(2023, 2026, 529, "Bolsa Família", "2023–", 12)
    p += [line(70, 650, 1530, 650),
          txt(70, 679, "Mexico", 15, "#b85b2c", "bold"),
          line(round(px(1997), 1), 674, round(px(2014), 1), 674, "#b85b2c", 4),
          line(round(px(1997), 1), 666, round(px(1997), 1), 682, "#b85b2c", 3),
          line(round(px(2014), 1), 666, round(px(2014), 1), 682, "#b85b2c", 3),
          txt(round((px(1997)+px(2014))/2, 1), 695, "1997–2014", 14, "#b85b2c", anchor="middle"),
          txt(70, 717, "Brazil", 15, "#147d86", "bold"),
          line(round(px(2003), 1), 712, round(px(2014), 1), 712, "#147d86", 4),
          line(round(px(2003), 1), 704, round(px(2003), 1), 720, "#147d86", 3),
          line(round(px(2014), 1), 704, round(px(2014), 1), 720, "#147d86", 3),
          txt(round((px(2003)+px(2014))/2, 1), 733, "2003–2014", 14, "#147d86", anchor="middle"),
          txt(70, 769, "Government colours are broad ideological placements; PRI is coded centre/mixed and party coalitions vary.", 15),
          txt(70, 797, "Mexico's post-2019 scholarships changed the CCT design, including health and nutrition components.", 15),
          txt(70, 825, "Program and government overlap describes timing; it does not identify a government's effect on inequality.", 15),
          txt(70, 849, "Sources: Brazil Casa Civil / MDS; Mexico INE / SIDOF / CONEVAL; ideology: party research. Details in data/cct_government_timeline_sources.md.", 13, "#5b6570"),
          txt(70, 872, "2026 is the chart boundary, not a government or program end date.", 13, "#5b6570"), '</svg>']
    path = FIGURES / "cct_program_timeline_1997_2003_to_2014.svg"
    path.write_text("\n".join(p), encoding="utf-8")
    return path


def save_sources(population: dict[str, int]) -> Path:
    DATA.mkdir(exist_ok=True)
    path = DATA / "cct_infographic_sources.md"
    rows = ["# CCT infographic data and sources", "", "Figures use English labels and show a 2018 snapshot unless stated otherwise.",
            "Coverage counts include all people in recipient households; they are not counts of individual cash recipients.", "",
            "## World Bank population denominator", "", f"API: {POP_API}",
            f"- Brazil 2018: {population['BRA']:,}", f"- Mexico 2018: {population['MEX']:,}", "",
            "## Official program sources", ""]
    rows.extend(f"- {key}: {url}" for key, url in SOURCES.items())
    rows += ["", "## Snapshot values", "", "- Brazil, August 2018: 13,951,980 recipient households; 44,080,713 people in those households; 89.3% female family heads (MDS/SENARC).",
             "- Brazil, August 2018: 27.38% rural and 72.09% urban recipient households (ENAP, remaining fraction unclassified).",
             "- Brazil, August 2018: R$187.13 mean monthly household payment (MDS/SENARC).",
             "- Mexico, 2018: approximately 6.9 million households and 28 million people (government report).",
             "- Mexico, March 2018: 96% of household program holders were women (Secretaría de Bienestar).",
             "- Mexico, June 2016: 54% rural, 19% semiurban, 26% urban recipient households (SEDESOL, rounded).",
             "- Mexico, first half 2018: MXN 335 monthly food support and MXN 140 food supplement; educational grants varied (PROSPERA budget report).",
             "", "Ratios are rounded; source dates and settlement classifications differ. Monetary amounts are nominal and should not be compared as equivalent purchasing power.",
             "", "## Observed country-level change: 2004–2014", "",
             "The script reads the three project CSV extracts rather than hardcoding these values. These are observed national survey indicators, not estimated effects of CCTs. Relative percentage change is calculated as (2014 value − 2004 value) / 2004 value × 100; it differs from percentage-point change.",
             "", "| Indicator | Brazil 2004 → 2014 | Mexico 2004 → 2014 | Unit |",
             "|---|---:|---:|---|",
             "| WDI Gini index | 56.5 → 52.1 (−4.4 points; −7.8%) | 50.3 → 48.9 (−1.4 points; −2.8%) | 0–100 index points |",
             "| WDI bottom-20 income share | 2.9 → 3.6 (+0.7 pp; +24.1%) | 4.0 → 4.7 (+0.7 pp; +17.5%) | percent and percentage points |",
             "| SEDLAC rural minus urban poverty headcount | 28.2 → 25.2 (−3.0 pp; −10.5%) | 32.7 → 28.4 (−4.3 pp; −13.2%) | percentage points |",
             "", "The underlying SEDLAC poverty rates (percent of each area's population below the line) are: Brazil 2004 rural 70.7%, urban 42.5%; 2014 rural 45.9%, urban 20.7%. Mexico 2004 rural 69.2%, urban 36.5%; 2014 rural 62.2%, urban 33.8%. The figure calculates rural minus urban for each year.",
             "", "SEDLAC poverty line: $6.85 per person per day in 2017 PPP. The gap is rural poverty incidence minus urban incidence. The periods 2004–2014 avoid Mexico's major 2014–2016 ENIGH survey break and Brazil's later PNAD/PNAD Contínua transition. These series still reflect different national surveys and are descriptive, not a common causal design.",
             "", "## Research outcomes shown in the infographic", "",
             "[1] Soares et al. (2007), *Conditional Cash Transfers in Brazil, Chile and Mexico*: CCT income-source decomposition attributes 20.8% of Brazil's observed 1995–2004 Gini decline and 20.5% of Mexico's observed 1996–2004 decline to CCTs. The first years are survey baselines, not program start dates. Brazil's Bolsa Família was created in October 2003 by consolidating earlier transfers; therefore, do not describe the 20.8% as a Bolsa Família-only effect over 1995–2004. This is an accounting decomposition, not an experimental causal estimate. " + SOURCES["comparative_gini_attribution"] + " Launch law: " + SOURCES["brazil_bf_launch"],
             "[2] Souza et al. (2019), IPEA: Bolsa Família accounts for about 17% of Brazil's observed Gini reduction in 2001–2006 and about 10% in 2001–2015. The 2001 survey is a prelaunch baseline; the program began in 2003. Income-source decomposition, not causal. " + SOURCES["brazil_later_gini_attribution"],
             "[3] de Brauw et al. (2014), IFPRI: Brazil 2005–2009 matched panel estimates +4.5 percentage points school participation among ages 6–17 overall (significant only at 10%); +8.2 pp for girls and +7.4 pp in rural areas. These are percentage points per the body and Table 5.1 of the study. " + SOURCES["brazil_schooling"],
             "[4] Schultz, IFPRI: Mexico early rural Progresa randomized rollout, 1997/98 baseline and 1998–99 follow-up; panel secondary-school enrollment effect +9.3 percentage points for girls and +5.8 pp for boys. These findings do not describe national enrollment. " + SOURCES["mexico_schooling"],
             "[5] Brazil MDS/IFPRI AIBF-II evaluation (2005–2009): on-time second DPT dose +15.5 percentage points among children; third dose +26 pp. These are program evaluation estimates, not a national health-access rate. " + SOURCES["brazil_health"],
             "[6] Gertler and Boyce (2001): Mexico clinic administrative data, 1996–1998; difference-in-differences estimate +2.09 visits per clinic per day or +18.2% in Progresa localities. Visits include beneficiaries and nonbeneficiaries in clinic catchments. This is utilization, not national health coverage. " + SOURCES["mexico_health"],
             "[7] Aguilar-Gutiérrez (2016), *Economía, Sociedad y Territorio*, Table 7: 11.15% of Mexico's 2000–2012 Gini decline is attributed to 'Oportunidades-type public programs' in an income-source decomposition of ENIGH microdata. The paper's footnote 4 explicitly groups benefits from Oportunidades and other government programs under this label. It is not an Oportunidades-only estimate or a causal effect. " + SOURCES["mexico_broader_gini_attribution"],
             "[8] Lambert and Park (2019), IMF, Figure 10 / Section 4.4: in 2016 Prospera and non-contributory old-age pensions jointly account for 73% of the Gini reduction due to government transfers. The denominator is the transfer-induced Gini effect, not Mexico's total observed Gini decline; the programs are not separately quantified by that figure. " + SOURCES["mexico_transfer_gini_attribution"],
             "[9] Bornhorst (2009), IMF Working Paper 09/187: using the rural Progresa randomized rollout data, the observed treatment-versus-control difference estimator yields +5.4 percentage points in overall school enrollment for eligible children ages 10–16. This is the measured estimate, not the paper's +8.1 pp microsimulation. Survey waves span 1997–1999. It is not a national school-enrollment change. " + SOURCES["mexico_overall_schooling"],
             "", "## Deliberate omissions", "",
             "A comparable bottom-50 income share is not in the WDI series used here. WID provides bottom-50 *pre-tax national income* shares, a different income concept from the WDI survey-based bottom-20 share. Combining them in the same delta panel would be misleading. The infographic also does not present a national healthcare-access effect because the available CCT evaluations measure service use in selected samples rather than a national access rate."]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def main() -> None:
    FIGURES.mkdir(exist_ok=True)
    population = population_2018()
    paths = [comparison(population), timeline()]
    converter = shutil.which("rsvg-convert")
    for path in paths:
        if converter:
            png = path.with_suffix(".png")
            subprocess.run([converter, "-w", "2400", str(path), "-o", str(png)], check=True)
            print(f"Saved {png}")
        print(f"Saved {path}")
    print(f"Saved {save_sources(population)}")


if __name__ == "__main__":
    main()
