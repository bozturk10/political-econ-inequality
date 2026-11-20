"""Four presentation assets from the original SWIID 8.0 summary CSV."""

from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "swiid8_0_summary.csv"

COUNTRIES = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica",
    "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras",
    "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela",
]
NAME = {"Dominican Republic": "Dominican Rep."}
BLUE, ORANGE = "#1F527A", "#D65E13"
INK, MUTED, GRID, GREY = "#172734", "#5C6972", "#DCE3E7", "#AAB5BB"

with SOURCE.open(newline="", encoding="utf-8") as f:
    data = {(r["country"], int(r["year"])): r for r in csv.DictReader(f)}

def val(country, year, field):
    return float(data[(country, year)][field])

def set_style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 13, "axes.titlesize": 26,
        "axes.labelsize": 15, "axes.edgecolor": "#9EABB2", "axes.labelcolor": INK,
        "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white",
        "axes.facecolor": "white", "savefig.facecolor": "white",
    })

def base(title, subtitle, note, *, wide_labels=False):
    fig = plt.figure(figsize=(16, 9))
    left, width = (0.075, 0.725) if wide_labels else (0.085, 0.84)
    ax = fig.add_axes([left, 0.20, width, 0.58])
    fig.text(0.075, 0.925, title, fontsize=26, weight="bold", color=INK)
    fig.text(0.075, 0.875, subtitle, fontsize=14.5, color=MUTED)
    fig.text(0.075, 0.105, note, fontsize=11.2, color=MUTED)
    fig.text(0.075, 0.073,
             "Source: Solt, SWIID 8.0 summary file (2019). Gini scale: 0–100. Authors’ calculations.",
             fontsize=10.5, color=MUTED)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_title("Gini coefficient", loc="left", pad=12, fontsize=16, color=INK)
    ax.set_xticks([1997, 2000, 2003, 2006, 2009, 2012, 2014])
    return fig, ax

def save(fig, stem):
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{stem}.{ext}", dpi=200)
    plt.close(fig)

set_style()
years = list(range(1997, 2015))
for c in COUNTRIES:
    for y in years:
        assert data[(c, y)]["gini_mkt"] and data[(c, y)]["gini_disp"]

# 1. Regional market-income context: fixed, balanced 18-country simple mean.
fig, ax = base(
    "Market-income inequality across Latin America",
    "18 countries and their unweighted average · 1997–2014 · annual SWIID 8.0 estimates",
    "Balanced 18-country sample; Cuba has no SWIID 8.0 series and Haiti has no 2014 observation."
    " The mean includes Brazil and Mexico.", wide_labels=True,
)
for c in COUNTRIES:
    color = BLUE if c == "Brazil" else ORANGE if c == "Mexico" else GREY
    z = 4 if c in ("Brazil", "Mexico") else 2
    ax.plot(years, [val(c, y, "gini_mkt") for y in years], color=color,
            lw=3.0 if z == 4 else 1.4, alpha=1 if z == 4 else 0.68, zorder=z)
means = [sum(val(c, y, "gini_mkt") for c in COUNTRIES) / len(COUNTRIES) for y in years]
ax.plot(years, means, color=INK, lw=3.5, zorder=5)
ax.set_xlim(1997, 2018.9)
ax.set_ylim(35, 64)
ax.tick_params(axis="y", labelsize=17, pad=10)
ax.tick_params(axis="x", labelsize=14)
ax.set_title("Gini coefficient", loc="left", pad=14, fontsize=19, color=INK)

# Place all direct labels at the right edge without collisions.
labels = [(c, val(c, 2014, "gini_mkt")) for c in COUNTRIES] + [("18-country mean", means[-1])]
labels.sort(key=lambda item: item[1])
lower, upper, gap = 36.0, 62.1, 1.32
positions = [max(v, lower + i * gap) for i, (_, v) in enumerate(labels)]
for i in range(len(positions) - 2, -1, -1):
    positions[i] = min(positions[i], positions[i + 1] - gap)
if positions[-1] > upper:
    shift = positions[-1] - upper
    positions = [p - shift for p in positions]
for (c, actual), ypos in zip(labels, positions):
    color = BLUE if c == "Brazil" else ORANGE if c == "Mexico" else INK if c == "18-country mean" else MUTED
    label = f"{NAME.get(c, c)}  {actual:.1f}"
    ax.plot([2014.1, 2014.75], [actual, ypos], color=color, lw=0.8, alpha=.7, clip_on=False)
    ax.text(2014.9, ypos, label, color=color, va="center",
            fontsize=14.5 if c in ("Brazil", "Mexico", "18-country mean") else 9.8,
            weight="bold" if c in ("Brazil", "Mexico", "18-country mean") else "normal")
save(fig, "01_latin_america_market_gini")

# 2. Focus the same market-income measure on the two cases.
fig, ax = base(
    "The market-income trajectories diverge",
    "Brazil and Mexico · market-income Gini · 1997–2014",
    "Programme-era changes use different starting years: Brazil 2003–2014; Mexico 1997–2014."
    " Descriptive comparison, not a CCT effect.",
)
for c, color in (("Brazil", BLUE), ("Mexico", ORANGE)):
    series = [val(c, y, "gini_mkt") for y in years]
    ax.plot(years, series, color=color, lw=4, marker="o", ms=4, label=c)
    start = 2003 if c == "Brazil" else 1997
    ax.scatter([start, 2014], [val(c, start, "gini_mkt"), series[-1]],
               s=125, color=color, edgecolor="white", linewidth=1.5, zorder=6)
    ax.annotate(f"{c} {start}: {val(c,start,'gini_mkt'):.1f}",
                (start, val(c, start, "gini_mkt")), xytext=(7, 12 if c == "Brazil" else -24),
                textcoords="offset points", color=color, fontsize=18, weight="bold")
    ax.text(2014.15, series[-1], f"{c}  {series[-1]:.1f}", color=color, va="center",
            fontsize=18, weight="bold")
ax.set_xlim(1997, 2016.2)
ax.set_ylim(39, 63)
ax.tick_params(axis="y", labelsize=17, pad=10)
ax.tick_params(axis="x", labelsize=15)
ax.set_title("Gini coefficient", loc="left", pad=14, fontsize=19, color=INK)
save(fig, "02_brazil_mexico_market_gini")

# 3. Add disposable-income Gini, preserving the case colours.
fig, ax = base(
    "Disposable-income inequality is lower in both countries",
    "Brazil and Mexico · market vs disposable-income Gini · 1997–2014",
    "Solid = market income; dashed = disposable income. Separate programme windows remain Brazil 2003–2014"
    " and Mexico 1997–2014.",
)
for c, color in (("Brazil", BLUE), ("Mexico", ORANGE)):
    for field, style, width in (("gini_mkt", "-", 3.6), ("gini_disp", "--", 3.2)):
        series = [val(c, y, field) for y in years]
        ax.plot(years, series, color=color, ls=style, lw=width, marker="o", ms=3.4,
                label=f"{c} — {'market' if field == 'gini_mkt' else 'disposable'}")
ax.set_xlim(1997, 2014)
ax.set_ylim(39, 63)
ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor=GRID,
          fontsize=12, ncol=2, columnspacing=1.5)
save(fig, "03_brazil_mexico_market_disposable_gini")

# A compact version that can share one slide with the companion table.
fig = plt.figure(figsize=(8.4, 5.7))
fig.text(.08,.91,"Market vs disposable Gini",fontsize=20,weight="bold",color=INK)
fig.text(.08,.845,"Brazil and Mexico · 1997–2014",fontsize=11.5,color=MUTED)
ax = fig.add_axes([.10,.21,.84,.55])
ax.spines[["top","right"]].set_visible(False)
ax.grid(axis="y",color=GRID,lw=1)
ax.set_axisbelow(True)
ax.set_xlim(1997,2014); ax.set_ylim(39,63)
ax.set_xticks([1997,2000,2003,2006,2009,2012,2014])
ax.set_yticks([40,45,50,55,60])
ax.tick_params(labelsize=10,colors=MUTED)
ax.set_title("Gini coefficient",loc="left",pad=10,fontsize=11,color=INK)
for c,color in (("Brazil",BLUE),("Mexico",ORANGE)):
    for field,style in (("gini_mkt","-"),("gini_disp","--")):
        ax.plot(years,[val(c,y,field) for y in years],color=color,ls=style,
                lw=2.6,marker="o",ms=2.7)
handles=[Line2D([0],[0],color=BLUE,lw=2.8),Line2D([0],[0],color=ORANGE,lw=2.8),
         Line2D([0],[0],color=INK,lw=2.8),Line2D([0],[0],color=INK,lw=2.8,ls="--")]
fig.legend(handles,["Brazil","Mexico","Market","Disposable"],loc="lower center",
           bbox_to_anchor=(.52,.115),ncol=4,frameon=False,fontsize=10)
fig.text(.08,.065,"Source: Solt, SWIID 8.0 summary file (2019).",fontsize=9.2,color=MUTED)
save(fig,"03_compact_for_table")

# 4. A compact companion table for positioning next to figure 3.
rows = []
for c, start in (("Brazil", 2003), ("Mexico", 1997), ("Mexico", 2003)):
    m0, m1 = val(c, start, "gini_mkt"), val(c, 2014, "gini_mkt")
    d0, d1 = val(c, start, "gini_disp"), val(c, 2014, "gini_disp")
    rows.append({"country": c, "period": f"{start}–2014", "market_start": m0,
                 "market_end": m1, "market_change": round(m1-m0,1),
                 "disposable_start": d0, "disposable_end": d1,
                 "disposable_change": round(d1-d0,1),
                 "gap_start": round(m0-d0,1), "gap_end": round(m1-d1,1),
                 "gap_change": round((m1-d1)-(m0-d0),1)})
with (OUT / "04_companion_table.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)

fig = plt.figure(figsize=(8.4, 5.7))
fig.text(.06,.91,"Gini changes",fontsize=20,weight="bold",color=INK)
fig.text(.06,.845,"Programme windows and shared 2003–2014 comparison",fontsize=11.5,color=MUTED)
ax=fig.add_axes([.06,.21,.88,.55]); ax.set_axis_off()
colx=[0,.31,.54,.77,1]
heights=[.19,.27,.27,.27]
ys=[1]
for h in heights: ys.append(ys[-1]-h)
for j in range(4):
    ax.add_patch(Rectangle((colx[j],ys[1]),colx[j+1]-colx[j],heights[0],
                           facecolor=INK if j==0 else BLUE if j==1 else ORANGE if j==2 else "#AD4B0C",transform=ax.transAxes))
for j,s in enumerate(["Measure","Brazil\n2003–14","Mexico\n1997–14","Mexico\n2003–14"]):
    ax.text((colx[j]+colx[j+1])/2, (ys[0]+ys[1])/2,s,ha="center",va="center",
            color="white",weight="bold",fontsize=11.5,linespacing=1.3,transform=ax.transAxes)
table_data=[
    ("Market-income Gini", "market"),
    ("Disposable-income Gini", "disposable"),
    ("Market − disposable¹", "gap"),
]
for i,(label,key) in enumerate(table_data,1):
    y0,y1=ys[i+1],ys[i]
    ax.add_patch(Rectangle((0,y0),1,y1-y0,facecolor="#F3F6F7" if i%2 else "white",
                           edgecolor=GRID,lw=1,transform=ax.transAxes))
    ax.text(.02,(y0+y1)/2,label,ha="left",va="center",fontsize=10.8,
            color=INK,transform=ax.transAxes)
    for j,r in enumerate(rows,1):
        x=(colx[j]+colx[j+1])/2
        s=f"{r[key+'_start']:.1f} → {r[key+'_end']:.1f}\n{r[key+'_change']:+.1f} pp"
        ax.text(x,(y0+y1)/2,s,ha="center",va="center",fontsize=10.9,
                color=BLUE if j==1 else ORANGE,
                linespacing=1.6,transform=ax.transAxes)
fig.text(.06,.13,"¹ Market minus disposable Gini; reflects all taxes and transfers, not CCTs alone.",fontsize=9.7,color=MUTED)
fig.text(.06,.075,"Source: Solt, SWIID 8.0 summary file (2019); authors’ calculations.",fontsize=9.2,color=MUTED)
save(fig,"04_companion_table")

print(f"Wrote three figures, companion table, and CSV to {OUT}")
