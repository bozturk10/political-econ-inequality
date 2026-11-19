import csv
import html
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=Path('/Users/berkyoztyurk/Desktop/pol_ec_ineq')
FILES={
    'Brazil':SOURCE/'EAR_INEE_CUR_NB_A-filtered-2026-11-19.csv',
    'Mexico':SOURCE/'EAR_INEE_CUR_NB_A-filtered-2026-11-19 (1).csv',
}
COLOR={'Brazil':'#16838D','Mexico':'#E57835'}
INK='#1E2933'; MUTED='#586773'; GRID='#DEE5E8'

def e(tag,attrs=None,body=''):
    attrs=attrs or {}
    a=' '.join(f'{k.replace("_","-")}="{html.escape(str(v),quote=True)}"' for k,v in attrs.items())
    return f'<{tag} {a}>{body}</{tag}>'
def t(x,y,s,size=26,weight=400,fill=INK,anchor='start'):
    return e('text',{'x':x,'y':y,'font-family':'Arial, Helvetica, sans-serif','font-size':size,
                     'font-weight':weight,'fill':fill,'text-anchor':anchor},html.escape(str(s)))
def ln(x1,y1,x2,y2,color=GRID,width=2,dash=None):
    a={'x1':x1,'y1':y1,'x2':x2,'y2':y2,'stroke':color,'stroke-width':width}
    if dash:a['stroke-dasharray']=dash
    return e('line',a)

records=[]
for country,file in FILES.items():
    with file.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    assert set(r['ref_area.label'] for r in rows)=={country}
    assert set(r['indicator.label'] for r in rows)=={'Monthly minimum wage by currency'}
    for r in rows:
        records.append({'country':country,'year':int(r['time']),'currency':r['classif1.label'],
                        'value':float(r['obs_value']),'source':r['source.label'],
                        'note':r['note_indicator.label']})

years={'Brazil':list(range(2003,2015)),'Mexico':list(range(1997,2015))}
for country in years:
    for cur in ['Currency: Local currency','Currency: 2021 PPP $','Currency: U.S. dollars']:
        have=sorted(r['year'] for r in records if r['country']==country and r['currency']==cur)
        assert have==years[country],(country,cur,have)

with (HERE/'ilostat_monthly_minimum_wage_brazil_mexico.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['country','year','monthly_minimum_local_currency','monthly_minimum_2021_ppp_dollars','monthly_minimum_us_dollars','source','note'])
    for country in ['Brazil','Mexico']:
        for year in years[country]:
            group=[r for r in records if r['country']==country and r['year']==year]
            vals={r['currency']:r['value'] for r in group}
            w.writerow([country,year,vals['Currency: Local currency'],vals['Currency: 2021 PPP $'],
                        vals['Currency: U.S. dollars'],group[0]['source'],group[0]['note']])

ppp={country:sorted([(r['year'],r['value']) for r in records if r['country']==country and r['currency']=='Currency: 2021 PPP $'])
     for country in years}
X=lambda year:165+(year-1997)/17*1400
Y=lambda value:780-(value-100)/320*495
body=[e('rect',{'x':0,'y':0,'width':1920,'height':1080,'fill':'white'}),
      t(95,104,'Statutory monthly minimum wage in Brazil and Mexico',49,700),
      t(95,155,'Annual observations; Mexico 1997–2014, Brazil 2003–2014',27,fill=MUTED),
      ln(95,184,1825,184,'#D7E0E4'),
      e('rect',{'x':X(1997),'y':285,'width':X(2003)-X(1997),'height':495,'fill':'#F7F8F9'}),
      t((X(1997)+X(2003))/2,255,'Mexico only: 1997–2002',21,600,fill=MUTED,anchor='middle')]
for tick in [100,150,200,250,300,350,400]:
    yy=Y(tick);body.extend([ln(165,yy,1565,yy),t(148,yy+7,tick,20,fill=MUTED,anchor='end')])
for year in [1997,2000,2003,2006,2009,2012,2014]:
    body.append(t(X(year),821,year,21,fill=MUTED,anchor='middle'))
body.append(t(95,238,'2021 PPP international dollars per month',29,700))
body.append(ln(165,780,1565,780,'#AAB6BC',2))
for country in ['Mexico','Brazil']:
    color=COLOR[country];rows=ppp[country]
    d=' '.join(('M' if i==0 else 'L')+f'{X(year):.1f},{Y(value):.1f}' for i,(year,value) in enumerate(rows))
    body.append(e('path',{'d':d,'fill':'none','stroke':color,'stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round'}))
    for year,value in rows:
        body.append(e('circle',{'cx':X(year),'cy':Y(value),'r':7,'fill':color,'stroke':'white','stroke-width':2}))
    year0,v0=rows[0];year1,v1=rows[-1]
    start_label=(190,665) if country=='Mexico' else (X(year0)+15,565)
    body.append(t(*start_label,f'{country} {year0}: {v0:.1f}',22,700,color))
    body.append(t(X(year1)+14,Y(v1)+8,f'{country} 2014: {v1:.1f}',24,700,color))
body.extend([t(95,900,'PPP conversion allows a common-unit level comparison; this is not the real-wage index.',21,fill=MUTED),
             t(95,930,'Mexico: daily statutory rate converted to a month using 6 days × 4.33 weeks; Brazil: monthly national floor.',20,fill=MUTED),
             t(95,978,'Source: ILOSTAT, EAR_INEE_CUR_NB_A (Monthly minimum wage by currency), two supplied CSV exports.',18,fill=MUTED),
             t(95,1008,'The series is annual and has no sex breakdown. “Monthly” describes the wage amount, not observation frequency.',18,fill=MUTED)])
(HERE/'01_ilostat_monthly_minimum_wage_ppp.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'+''.join(body)+'</svg>',encoding='utf-8')

local={country:sorted([(r['year'],r['value']) for r in records if r['country']==country and r['currency']=='Currency: Local currency'])
       for country in years}
body=[e('rect',{'x':0,'y':0,'width':1920,'height':1080,'fill':'white'}),
      t(95,104,'Minimum wage in local currency',49,700),
      t(95,155,'Nominal statutory monthly amount; each country has its own currency and vertical scale',26,fill=MUTED),
      ln(95,184,1825,184,'#D7E0E4')]
for country,x0,x1,ymax,ticks,unit in [
    ('Mexico',135,890,2000,[0,500,1000,1500,2000],'Mexican pesos / month'),
    ('Brazil',1050,1805,800,[0,200,400,600,800],'Brazilian reais / month')]:
    rows=local[country];first=rows[0][0];last=rows[-1][0]
    body.extend([t(x0,245,country,33,700,COLOR[country]),t(x0,282,unit,22,fill=MUTED)])
    x=lambda yr:x0+56+(yr-first)/(last-first)*(x1-x0-106)
    y=lambda val:745-val/ymax*390
    for tick in ticks:
        yy=y(tick)
        body.extend([ln(x0+50,yy,x1-40,yy),t(x0+38,yy+7,tick,19,fill=MUTED,anchor='end')])
    for yr in [first,2003,2008,2014]:
        if first<=yr<=last:
            body.append(t(x(yr),790,yr,20,fill=MUTED,anchor='middle'))
    d=' '.join(('M' if i==0 else 'L')+f'{x(yr):.1f},{y(val):.1f}' for i,(yr,val) in enumerate(rows))
    body.append(e('path',{'d':d,'fill':'none','stroke':COLOR[country],'stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round'}))
    for yr,val in rows:
        body.append(e('circle',{'cx':x(yr),'cy':y(val),'r':6,'fill':COLOR[country],'stroke':'white','stroke-width':2}))
    yr,val=rows[-1]
    body.append(t(x(yr)-8,y(val)-18,f'{val:,.0f} {"MXN" if country=="Mexico" else "BRL"}',25,700,COLOR[country],anchor='end'))
body.extend([t(95,887,'Local-currency values cannot be compared directly across countries; use the companion PPP chart for levels.',21,fill=MUTED),
             t(95,922,'Nominal changes include inflation. Use the separate real-wage index chart to assess purchasing-power growth over time.',21,fill=MUTED),
             t(95,978,'Source: ILOSTAT, EAR_INEE_CUR_NB_A (Monthly minimum wage by currency), two supplied CSV exports.',18,fill=MUTED),
             t(95,1008,'Mexico: daily rate converted to a month using 6 days × 4.33 weeks. Annual observations; no sex breakdown.',18,fill=MUTED)])
(HERE/'02_ilostat_monthly_minimum_wage_local_currency.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'+''.join(body)+'</svg>',encoding='utf-8')
