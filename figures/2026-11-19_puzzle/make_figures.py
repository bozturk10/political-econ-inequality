import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "data"
PREP = ROOT.parent / "data"
BRA = "#16838D"
MEX = "#E57835"
INK = "#1E2933"
MUTED = "#586773"
GRID = "#DEE5E8"


def read(name):
    with open(PREP / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def el(tag, attrs=None, body=""):
    attrs = attrs or {}
    a = " ".join(f'{k.replace("_", "-")}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f"<{tag} {a}>{body}</{tag}>"


def text(x, y, s, size=28, weight=400, fill=INK, anchor="start"):
    return el("text", {"x": x, "y": y, "font-family": "Arial, Helvetica, sans-serif", "font-size": size,
                       "font-weight": weight, "fill": fill, "text-anchor": anchor}, html.escape(str(s)))


def line(x1, y1, x2, y2, color=GRID, width=2, dash=None):
    a = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": color, "stroke-width": width}
    if dash: a["stroke-dasharray"] = dash
    return el("line", a)


def circle(x, y, color, r=6):
    return el("circle", {"cx": x, "cy": y, "r": r, "fill": color, "stroke": "white", "stroke-width": 2})


def chart(x, y, w, h, series, years, ymin, ymax, ticks, heading, fmt=lambda v: f"{v:g}", annotation=None, xticks=None):
    out = [text(x, y - 38, heading, 30, 700)]
    X = lambda yr: x + (yr - years[0]) / (years[1] - years[0]) * w
    Y = lambda val: y + h - (val - ymin) / (ymax - ymin) * h
    for v in ticks:
        yy = Y(v)
        out += [line(x, yy, x + w, yy), text(x - 14, yy + 8, fmt(v), 21, fill=MUTED, anchor="end")]
    for yr in (xticks or sorted(set([years[0], years[1]] + ([2010, 2012] if years == (2008, 2014) else [])))):
        if years[0] <= yr <= years[1]: out.append(text(X(yr), y + h + 39, yr, 21, fill=MUTED, anchor="middle"))
    out.append(line(x, y + h, x + w, y + h, "#AAB6BC", 2))
    for name, rows, color in series:
        pts = sorted([(int(yr), float(v)) for yr, v in rows if years[0] <= int(yr) <= years[1]])
        if len(pts) < 2: continue
        path = " ".join(("M" if i == 0 else "L") + f"{X(yr):.1f},{Y(v):.1f}" for i, (yr, v) in enumerate(pts))
        out.append(el("path", {"d": path, "fill": "none", "stroke": color, "stroke-width": 5,
                               "stroke-linecap": "round", "stroke-linejoin": "round"}))
        for yr, v in pts: out.append(circle(X(yr), Y(v), color, 7))
        yr, v = pts[-1]
        out.append(text(X(yr) + 13, Y(v) + (8 if name == "Brazil" else 7), f"{name} {fmt(v)}", 24, 700, color))
    if annotation: out.append(text(x, y + h + 96, annotation, 22, 600, MUTED))
    return "".join(out)


def page(title, subtitle, content, source_lines, note=None, status=None):
    out = [el("rect", {"x": 0, "y": 0, "width": 1920, "height": 1080, "fill": "white"}),
           text(95, 104, title, 50, 700), text(95, 155, subtitle, 27, fill=MUTED),
           line(95, 184, 1825, 184, "#D7E0E4", 2), content]
    if status: out.append(text(1825, 155, status, 22, 700, MEX, anchor="end"))
    if note: out.append(text(95, 968, note, 21, fill=MUTED))
    for i, s in enumerate(source_lines): out.append(text(95, 1015 + 27 * i, s, 18, fill=MUTED))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">' + "".join(out) + "</svg>"


def save(name, body):
    (ROOT / name).write_text(body, encoding="utf-8")


out = read("outcomes_wdi_2008_2014.csv")
print("outcome columns", list(out[0]))

# Values are only observed survey years; the paths join observations and do not fill missing years.
def outcome_rows(country, key):
    return [(r["year"], r[key]) for r in out if r["country_code"] == country and r[key]]

gini = [("Brazil", outcome_rows("BRA", "gini_0_100"), BRA),
        ("Mexico", outcome_rows("MEX", "gini_0_100"), MEX)]
bottom = [("Brazil", outcome_rows("BRA", "bottom20_share_pct"), BRA),
          ("Mexico", outcome_rows("MEX", "bottom20_share_pct"), MEX)]
c = chart(135, 325, 680, 500, gini, (2008, 2014), 47, 56, [48, 50, 52, 54, 56], "Gini index (0–100)",
          fmt=lambda v: f"{v:.1f}", annotation="2008–2014: both −1.9 Gini points")
c += chart(1090, 325, 600, 500, bottom, (2008, 2014), 3, 5.2, [3, 3.5, 4, 4.5, 5],
           "Income share of the bottom 20%", fmt=lambda v: f"{v:.1f}%",
           annotation="Brazil +0.4 pp   |   Mexico +0.8 pp")
save("01_same_gini_different_bottom20.svg", page("Same Gini drop, different gains at the bottom",
     "Brazil and Mexico, observed household survey years, 2008–2014", c,
     ["Source: World Bank WDI, SI.POV.GINI and SI.DST.FRST.20; local extraction of published series."],
     "Lines connect observed surveys; missing years are not estimated. Percentage-point changes use 2008 and 2014 endpoints."))

wage = read("ilo_real_minimum_wage_2003_2014.csv")
wseries = [("Brazil", [(r["year"], r["real_minimum_wage_index_2000_100"]) for r in wage if r["country"] == "Brazil"], BRA),
           ("Mexico", [(r["year"], r["real_minimum_wage_index_2000_100"]) for r in wage if r["country"] == "Mexico"], MEX)]
c = chart(175, 340, 1370, 505, wseries, (2003, 2014), 90, 220, [100, 125, 150, 175, 200],
          "Real national minimum wage (2000 = 100)", fmt=lambda v: f"{v:.1f}",
          annotation="2008–2014: Brazil +26.6%   |   Mexico +1.2%", xticks=[2003, 2005, 2008, 2011, 2014])
save("02_real_minimum_wage.svg", page("Brazil's real minimum wage rose much faster",
     "National minimum wage, inflation-adjusted; 2000 = 100", c,
     ["Source: ILO, Labour Overview 2013 and Labour Overview 2015, Table 10."],
     "Compare within-country changes; indexed levels do not compare purchasing power across countries."))

uhc = read("welfare_uhc_service_coverage_2000_2015.csv")
useries = [("Brazil", [(r["year"], r["uhc_service_coverage_index"]) for r in uhc if r["country_code"] == "BRA"], BRA),
           ("Mexico", [(r["year"], r["uhc_service_coverage_index"]) for r in uhc if r["country_code"] == "MEX"], MEX)]
c = chart(175, 340, 1370, 505, useries, (2000, 2015), 55, 80, [55, 60, 65, 70, 75, 80],
          "UHC service coverage index (0–100)", fmt=lambda v: f"{v:.0f}",
          annotation="2000–2015: Brazil 68 → 75   |   Mexico 60 → 73", xticks=[2000, 2005, 2010, 2015])
save("03_uhc_service_coverage.svg", page("Mexico narrowed the service-coverage gap",
     "WHO UHC index, four reported years, 2000–2015", c,
     ["Source: WHO and World Bank, Tracking Universal Health Coverage 2021, Annex 3."],
     "Service coverage is not a measure of legal entitlement, segmentation, or financial protection. 2021 data vintage."))

oop = read("welfare_oop_health_2000_2014.csv")
oseries = [("Brazil", [(r["year"], r["oop_pct_current_health_expenditure"]) for r in oop if r["country_code"] == "BRA"], BRA),
           ("Mexico", [(r["year"], r["oop_pct_current_health_expenditure"]) for r in oop if r["country_code"] == "MEX"], MEX)]
c = chart(175, 340, 1370, 505, oseries, (2003, 2014), 20, 60, [20, 30, 40, 50, 60],
          "Out-of-pocket share of current health spending (%)", fmt=lambda v: f"{v:.1f}%",
          annotation="2014: Brazil 28.2%   |   Mexico 40.9%", xticks=[2003, 2005, 2008, 2011, 2014])
save("04_out_of_pocket_health_provisional.svg", page("Mexico's out-of-pocket health share remained higher",
     "Household payments as a share of total current health expenditure, 2003–2014", c,
     ["Underlying indicator: WHO GHED / World Bank WDI, SH.XPD.OOPC.CH.ZS.",
      "Historical values retrieved from a third-party WDI mirror; confirm against the current WHO/WDI export before presenting."],
     "National expenditure share does not directly measure the burden on poor households.",
     status="PROVISIONAL"))
