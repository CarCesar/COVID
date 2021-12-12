import altair as alt
from vega_datasets import data

def bump_chart(source):
    click = alt.selection_multi(fields=['location'])
    
    g1 = alt.Chart(source).mark_line(point = True).encode(
    x = alt.X("date:O", timeUnit="yearmonth",axis=alt.Axis(labelAngle=-90,grid=True,domain=False,title=None,ticks=False,labelFont='Courier',labelFontSize=9)),
    y=alt.Y("rank:O",axis = alt.Axis(domain=False,grid = True,ticks=False)),
    color=alt.condition(click,alt.Color("location:N",legend=None),alt.value('lightgray'))
    ).transform_window(
    rank="rank()",
    sort=[alt.SortField("new_deaths", order="descending")],
    groupby=["date"]
    ).properties(
    title="Bump Chart for New Deaths / Population",
    width=600,
    height=150,
    ).add_selection(click)
    
    middle = alt.Chart(source).encode(
    x=alt.X("date:O", axis=None,sort=alt.SortOrder('ascending')),
    text=alt.Text("date:O", timeUnit="yearmonth"),
).mark_text(color='white',angle =270,fontSize=11,font='Courier').properties(width=600)
    
    b1 = alt.Chart(source).mark_line(point = True).encode(
    x = alt.X("date:O", timeUnit="yearmonth", title="date",axis=alt.Axis(orient='top',grid=True,domain=False,title=None,ticks=False,labels=False,),
              ),
    y=alt.Y("new_deaths:Q",axis = alt.Axis(domain=False,grid = True,ticks=False),),
    color=alt.condition(click,alt.Color("location:N",legend=None),alt.value('lightgray')),
    tooltip=[alt.Tooltip('new_deaths:Q'),alt.Tooltip('location:N'),'rank:O']
).transform_window(
    rank="rank()",
    sort=[alt.SortField("new_deaths", order="descending")],
    groupby=["date"]
).properties(
    width=600,
    height=150,
).add_selection(click)
    
    rm1 =alt.Chart(
    source,
).mark_rect().encode(
    x=alt.X('date:O',timeUnit="yearmonth",axis=alt.Axis(domain=False,title=None,ticks=False,orient='top',labelAngle=-90,labelFont='Courier',labelFontSize=9)),
    y=alt.Y('location:N',axis = alt.Axis(domain=False,ticks=False,title=None)),
    color=alt.condition(click,alt.Color('new_deaths:Q', scale=alt.Scale(scheme="yelloworangered"),legend=alt.Legend(orient='left')),alt.value('lightgray')),
).properties(width=600).add_selection(click)
    
    legenda = alt.Chart(source).mark_rect().encode(y='location',color='location').properties(width = 10)
    
    return ((alt.vconcat(g1,b1,rm1 ,spacing=1))).configure_view(strokeWidth=0)


def mapa_mundi(df1):
    sphere = alt.sphere()
    graticule = alt.graticule()
    mar = alt.Chart(sphere).mark_geoshape(fill='black')#lightblue
    linhas = alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.2)

    terra = alt.topo_feature(data.world_110m.url,
                               'countries')
    fundo = alt.Chart(terra).mark_geoshape(stroke="black", strokeWidth=0.15,fill="white")

    # O LOOKUP funciona pelo ISO 3166-1 numeric

    mapa = alt.Chart(terra
             ).mark_geoshape(stroke="black", strokeWidth=0.15).transform_lookup(
        lookup = 'id',from_=alt.LookupData(data=df1, key='id', fields=['new_cases','location','continent'])
    ).encode(
        color = alt.Color('continent:N',scale=alt.Scale(domain=['Africa','Asia',"Europe","North America",'Oceania','South America']),legend=None),)


    mapa = (mar+linhas+fundo+mapa).properties(width=500, height=263).project(type='equirectangular')

    return mapa