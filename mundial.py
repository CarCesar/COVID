import altair as alt
from vega_datasets import data

import auxilio

def bump_chart(source,col):
    click = alt.selection_multi(fields=['location'])
    
    g1 = alt.Chart(source).mark_line(point = True).encode(
    x = alt.X("date:O", timeUnit="yearmonth",axis=alt.Axis(labelAngle=-90,grid=True,domain=False,title=None,ticks=False,labels=False
                                                           ,labelFont='Courier',labelFontSize=9)),
    y=alt.Y("rank:O",axis = alt.Axis(domain=False,grid = True,ticks=False)),
    color=alt.condition(click,alt.Color("location:N",legend=None),alt.value('lightgray')),
    tooltip=[alt.Tooltip(f'{col}:Q'),alt.Tooltip('location:N'),'rank:O'],
    opacity = alt.condition(click,alt.value(1),alt.value(0.3)),
    ).transform_window(
    rank="rank()",
    sort=[alt.SortField(f"{col}", order="descending")],
    groupby=["date"]
    ).properties(
    title=auxilio.titulo(col),
    width=600,
    height=150,
    )#.add_selection(click)
       
    b1 = alt.Chart(source).mark_line(point = True).encode(
    x = alt.X("date:O", timeUnit="yearmonth", title="date",axis=alt.Axis(orient='top',grid=True,domain=False,title=None,ticks=False,),
              ),
    y=alt.Y(f"{col}:Q",axis = alt.Axis(domain=False,grid =True,gridOpacity=0.5,ticks=False,orient='right',titleFont='Courier',
                                           title=auxilio.titulo(col)),),
    #color = alt.Color("location:N",legend=None),
    color=alt.condition(click,alt.Color("location:N",legend=None),alt.value('lightgray')),
    opacity = alt.condition(click,alt.value(.9),alt.value(0.3)),
).transform_window(
    rank="rank()",
    sort=[alt.SortField(f"{col}", order="descending")],
    groupby=["date"]
).properties(
    width=600,
    height=150,
)
    
    rm1 =alt.Chart(
    source,
).mark_rect().encode(
    x=alt.X('date:O',timeUnit="yearmonth",axis=alt.Axis(domain=False,title=None,ticks=False,orient='top',labelAngle=-90,labelFont='Courier',labelFontSize=9)),
    y=alt.Y('location:N',axis = alt.Axis(domain=False,ticks=False,title=None,labelFont='Courier')
            ,scale=alt.Scale(domain=['Oceania','Africa','Asia','Europe','North America','South America'])),
    color=alt.Color(f'{col}:Q', scale=alt.Scale(scheme="browns"),legend=alt.Legend(orient='right',title=None,)),
    opacity = alt.condition(click,alt.value(.9),alt.value(0)),
).transform_window(
    rank="rank()",
    sort=[alt.SortField(col, order="descending")],
    groupby=["date"]
).properties(width=600,height=150)#.add_selection(click)
    
    rm2 = rm1.encode(opacity=alt.value(0),tooltip=[alt.Tooltip(f'{col}:Q'),alt.Tooltip('location:N'),'rank:O']).transform_filter(click)
    
    rm3 = rm1.add_selection(click)+rm2
    
    legenda = alt.Chart(source).mark_rect(stroke='bisque',cornerRadius=10,x=20).encode(y=alt.Y('location',axis=alt.Axis(domain = False,ticks=False,
                                                                                                                        orient='right',labelFont='Courier',
                                                                                                                        title=None)),
                                                                                       color='location').properties(
    width=20,
    height=150,
).add_selection(click)
    
    return ((alt.vconcat((g1).add_selection(click)|legenda,(b1+rm3) ,spacing=1))).configure_view(strokeWidth=0)
    #return(((g1+g2)|legenda)&(b1+rm3))


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


    mapa = (mar+linhas+fundo+mapa).properties(width=435, height=250).project(type='naturalEarth1').configure_view(strokeWidth=0)

    return mapa