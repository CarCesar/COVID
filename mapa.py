import altair as alt
from vega_datasets import data

terra = alt.topo_feature(data.world_110m.url,'countries')

dic = {'Africa':[-17, 0 ,0],'Asia':[-80, -20 ,0],'Europe':[-30, -60 ,0],'Oceania':[-150, 20 ,0],'North America':[100, -40 ,0],'South America':[60, 20 ,0]}


sphere = alt.sphere()
graticule = alt.graticule()
mar = alt.Chart(sphere).mark_geoshape(fill='lightgrey')#lightblue
linhas = alt.Chart(graticule).mark_geoshape(stroke='#444444', strokeWidth=0.5)
fundo = alt.Chart(terra).mark_geoshape(stroke="#444444", strokeWidth=0.15,fill='#444444')#lightgrey

def mapa(df,nome,col,cor="goldred"):
    mapa = alt.Chart(terra
         ).mark_geoshape(stroke="black", strokeWidth=0.15).transform_lookup(
    lookup = 'id',from_=alt.LookupData(data=df, key='id', fields=[f'{col}','location'])
    ).encode(
    color = alt.Color(f'{col}:Q', scale=alt.Scale(scheme=cor),legend = None),#range=['gold','red']
    tooltip = [alt.Tooltip('location:N',title = 'Country'),alt.Tooltip(f'{col}:Q')]
    )

    fig = (mar+fundo+linhas+mapa
           ).properties(width=400, height=400
                        ).project(type='orthographic',rotate=dic[nome]
                                  ).configure_view(strokeWidth=0)
    return fig

