import csv
import html
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
BRA, MEX = "#16838D", "#E57835"
INK, MUTED, GRID = "#1E2933", "#586773", "#DEE5E8"

def element(tag, attrs=None, body=""):
    attrs = attrs or {}
    arg = " ".join(f'{k.replace("_", "-")}="{html.escape(str(v), quote=True)}"' for k,v in attrs.items())
    return f"<{tag} {arg}>{body}</{tag}>"

def txt(x,y,value,size=28,weight=400,fill=INK,anchor="start"):
    return element("text",{"x":x,"y":y,"font-family":"Arial, Helvetica, sans-serif","font-size":size,
                           "font-weight":weight,"fill":fill,"text-anchor":anchor},html.escape(str(value)))

def line(x1,y1,x2,y2,color=GRID,width=2):
    return element("line",{"x1":x1,"y1":y1,"x2":x2,"y2":y2,"stroke":color,"stroke-width":width})

def dot(x,y,color,r=8):
    return element("circle",{"cx":x,"cy":y,"r":r,"fill":color,"stroke":"white","stroke-width":2})

def arrow(x1,y1,x2,y2,color):
    angle=math.atan2(y2-y1,x2-x1)
    ux,uy=math.cos(angle),math.sin(angle)
    bx,by=x2-21*ux,y2-21*uy
    wing=9
    points=f"{x2:.1f},{y2:.1f} {bx-wing*uy:.1f},{by+wing*ux:.1f} {bx+wing*uy:.1f},{by-wing*ux:.1f}"
    return line(x1,y1,bx,by,color,6)+element("polygon",{"points":points,"fill":color})

def page(title, subtitle, body, footer):
    svg = [element("rect",{"x":0,"y":0,"width":1920,"height":1080,"fill":"white"}),
           txt(95,105,title,49,700),txt(95,154,subtitle,27,fill=MUTED),
           line(95,185,1825,185,"#D7E0E4",2),body]
    for i,s in enumerate(footer): svg.append(txt(95,994+i*31,s,19,fill=MUTED))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'+"".join(svg)+"</svg>"

# Exact rounded endpoints transcribed from the table embedded on slide 4 of the supplied PPTX.
# The SWIID 8.0 raw series was not available locally, so no intermediate-year observations are drawn.
endpoints = {
  "Market income Gini": [("Brazil",2003,2014,58.6,53.8,BRA),("Mexico",1997,2014,48.6,47.1,MEX)],
  "Disposable income Gini": [("Brazil",2003,2014,50.7,45.0,BRA),("Mexico",1997,2014,47.7,45.2,MEX)]
}
def endpoint_panel(x, heading, rows, disposable=False):
    w=685; top=365; height=410
    X=lambda year:x+(year-1997)/17*w
    Y=lambda value:top+(62-value)/22*height
    parts=[txt(x,295,heading,31,700)]
    if disposable:
        parts.append(txt(x,339,"2014 endpoints: Brazil 45.0  |  Mexico 45.2",21,700,fill=MUTED))
    for tick in [45,50,55,60]:
        yy=Y(tick)
        parts += [line(x,yy,x+w,yy,GRID,2),txt(x-13,yy+7,tick,20,fill=MUTED,anchor="end")]
    for year in [1997,2003,2014]:
        xx=X(year)
        parts += [line(xx,top,xx,top+height,"#E8ECEF",1),txt(xx,top+height+40,year,21,fill=MUTED,anchor="middle")]
    parts += [txt(x+w/2,top+height+86,"Year →",23,700,fill=MUTED,anchor="middle")]
    for name,start,end,v0,v1,color in rows:
        sx,sy,ex,ey=X(start),Y(v0),X(end),Y(v1)
        parts += [dot(sx,sy,color,8),arrow(sx+11,sy,ex,ey,color)]
        if name=="Brazil":
            parts += [txt(sx+12,sy-20,f"Brazil {start}: {v0:.1f}",22,700,color),
                      txt((sx+ex)/2-6,(sy+ey)/2-20,f"{v1-v0:.1f} points",21,700,color)]
        else:
            parts += [txt(sx+8,sy+41,f"Mexico {start}: {v0:.1f}",22,700,color),
                      txt((sx+ex)/2-6,(sy+ey)/2+40,f"{v1-v0:.1f} points",21,700,color)]
        if not disposable:
            parts.append(txt(ex+14,ey+7,f"{name} 2014: {v1:.1f}",21,700,color))
    return "".join(parts)

body=endpoint_panel(140,"Market income Gini",endpoints["Market income Gini"])
body+=endpoint_panel(1060,"Disposable income Gini",endpoints["Disposable income Gini"],True)
(HERE/"01_swiid_inequality_program_windows.svg").write_text(page(
    "Inequality fell more in Brazil in both income measures",
    "Program-era endpoints: Brazil 2003–2014; Mexico 1997–2014",
    body,["Source: SWIID 8.0 summary values reproduced in the supplied presentation, slide 4.",
          "Windows differ in length; endpoint changes are descriptive and are not estimates of CCT effects.",
          "Only four rounded endpoints per measure were available; no annual values were reconstructed."]),encoding="utf-8")

# Primary ILO annual wage series; rebase each country's 2000=100 source index to 2003=100.
with open(DATA/"ilo_real_minimum_wage_2003_2014.csv",newline="",encoding="utf-8") as f:
    wages=list(csv.DictReader(f))
series=[]
for country,color in [("Brazil",BRA),("Mexico",MEX)]:
    raw=[(int(r["year"]),float(r["real_minimum_wage_index_2000_100"])) for r in wages if r["country"]==country]
    base=dict(raw)[2003]
    series.append((country,color,[(year,value/base*100) for year,value in raw]))
x,y,w,h=175,335,1370,500
X=lambda year:x+(year-2003)/11*w
Y=lambda val:y+h-(val-95)/85*h
body=[txt(x,y-40,"Real national minimum wage (2003 = 100)",31,700)]
for tick in [100,120,140,160,180]:
    yy=Y(tick);body.extend([line(x,yy,x+w,yy),txt(x-15,yy+8,f"{tick}",21,fill=MUTED,anchor="end")])
for year in [2003,2005,2008,2011,2014]:body.append(txt(X(year),y+h+42,year,21,fill=MUTED,anchor="middle"))
body.append(line(x,y+h,x+w,y+h,"#AAB6BC",2))
for name,color,rows in series:
    path=" ".join(("M" if i==0 else "L")+f"{X(yr):.1f},{Y(v):.1f}" for i,(yr,v) in enumerate(rows))
    body.append(element("path",{"d":path,"fill":"none","stroke":color,"stroke-width":5,"stroke-linecap":"round","stroke-linejoin":"round"}))
    for yr,v in rows:body.append(dot(X(yr),Y(v),color,7))
    yr,v=rows[-1];body.append(txt(X(yr)+15,Y(v)+7,f"{name} {v:.1f}",25,700,color))
body.append(txt(175,945,"2003–2014: Brazil +73.4%   |   Mexico +0.5%",25,700,MUTED))
(HERE/"02_real_minimum_wage_overlap_2003_2014.svg").write_text(page(
    "Brazil's real minimum wage rose; Mexico's barely changed",
    "Common CCT overlap, 2003–2014; each country starts at 100",
    "".join(body),["Source: ILO Labour Overview 2013 and Labour Overview 2015, Table 10.",
                   "ILO's published 2000=100 indices were rebased to 2003=100; levels do not compare wages across countries."]),encoding="utf-8")
