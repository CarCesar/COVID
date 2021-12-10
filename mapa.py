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

'''
def mapa(nome:str,data:str):
    #df4 = df2[(df2['date']==data) & (df2['continent']==nome)]
    #df4 = df2[(df2['date']==data) and (df2['continent']==nome)] 
    df4 = df2.query(f'date == "{data}" and continent== "{nome}"') 
    #df4 = df2[df2['date']==data][df2['continent']==nome] 
    df4 = df4.sort_values(by=['new_cases'],ascending=False)
    # O LOOKUP funciona pelo ISO 3166-1 numeric

    mapa = alt.Chart(terra
         ).mark_geoshape(stroke="black", strokeWidth=0.15).transform_lookup(
    lookup = 'id',from_=alt.LookupData(data=df4, key='id', fields=['total_cases','location'])
    ).encode(
    color = alt.Color('total_cases:Q', scale=alt.Scale(scheme="goldred"),legend = None),#range=['gold','red']
    tooltip = [alt.Tooltip('location:N',title = 'Country'),alt.Tooltip('total_cases:Q')]
    )

    fig = (mar+fundo+linhas+mapa
           ).properties(width=400, height=400
                        ).project(type='orthographic',rotate=dic[nome]
                                  ).configure_view(strokeWidth=0)
    
    st.header(nome+'-'+data)
    col1, b ,col2, col3= st.columns([10,1,1.5,3])
    #mapacont, f,d = st.columns((3,1,1))
    #with mapacont:
    col1.altair_chart(fig,use_container_width=True)
    st.header('Maiores indices de novos casos')
    paises = df4.iloc[0]
    col2.image(paises['flag'],width=70)#,caption = str(numero+1))
    #col2.write(' ⚠️  1️⃣  ⚠️')
    col2.write('\~~~ 1º ~~~')
    col3.metric(label=paises['location'], value=paises['new_cases'], delta=round((paises['new_cases']-paises['new_cases_smoothed'])/paises['new_cases_smoothed'],5),delta_color="inverse")
    paises = df4.iloc[1]
    col2.image(paises['flag'],width=70)#,caption = str(numero+1))
    #col2.write(' ⚠️  2º  ⚠️')
    col2.write('\~~~ 2º ~~~')
    col3.metric(label=paises['location'], value=paises['new_cases'], delta=round((paises['new_cases']-paises['new_cases_smoothed'])/paises['new_cases_smoothed'],5),delta_color="inverse")
    paises = df4.iloc[2]
    col2.image(paises['flag'],width=70)#,caption = str(numero+1))
    #col2.write(' ⚠️  3º  ⚠️')
    col2.write('\~~~ 3º ~~~')
    col3.metric(label=paises['location'], value=paises['new_cases'], delta=round((paises['new_cases']-paises['new_cases_smoothed'])/paises['new_cases_smoothed'],5),delta_color="inverse")
    paises = df4.iloc[3]
    col2.image(paises['flag'],width=70)#,caption = str(numero+1))
    #col2.write(' ⚠️  4º  ⚠️')
    col2.write('\~~~ 4º ~~~')
    col3.metric(label=paises['location'], value=paises['new_cases'], delta=round((paises['new_cases']-paises['new_cases_smoothed'])/paises['new_cases_smoothed'],5),delta_color="inverse")

    #col1,col2,col3,col4,col5 = st.columns(5)
    #with col1:
    #    pais(0,df4)#,f,d)
    #with col2:
    #    pais(1,df4)#,f,d)
    #with col3:
     #   pais(2,df4)#,f,d)
    #with col4:
     #   pais(3,df4)#,f,d)
    #with col5:
     #   pais(4,df4)#,f,d)
    click1 = alt.selection_multi(fields=['location'])
    click2 = alt.selection_multi(fields=['location'])
    fig1 = alt.Chart(df4).mark_point(color = 'orange').encode(x=alt.X('total_cases:Q',scale=alt.Scale(type='log'),axis=None),
                                   y=alt.Y('total_deaths:Q',scale=alt.Scale(type='log'),axis = None),
                                   size=alt.Size('new_cases',legend = alt.Legend(orient='top-left')),
                                   color = alt.condition(click1,alt.value('orange'),alt.value('lightgray')),
                                   tooltip = ['location','new_cases']
                                                             ).properties(width=350, height=350).add_selection(click1)
    
    fig2 = alt.Chart(df4).mark_bar().encode(x=alt.X('new_cases'),
                                   y=alt.Y('location',sort='-x',axis=None),
                                   tooltip = 'location',
                                    color = alt.condition(click1,
                                                          alt.Color('location:N',legend=None,scale=alt.Scale(scheme='set1')),
                                                          alt.value('lightgray'))
                                           ).properties(width=700,height=350).add_selection(click1)
    
    text = alt.Chart(df4).mark_text(x=350,y=300,#color = 'white'
                                   ).encode(text=alt.condition(click1,alt.Text('location:N'),alt.value('1')),
                                            color = alt.condition(click1,
                                                                  alt.value('white'),
                                                                  alt.value('black'))

                                           ).properties(width=700,height=350
                                                       ).transform_calculate(label='datum.location')
    
    ban = alt.Chart(df4).mark_image(width=50,x=600,y=300
                                    ).encode(url='flag',opacity = alt.condition(click1,
                                                                  alt.value(1),
                                                                  alt.value(0))

                                           ).properties(width=700,height=350
                                                       )
    
    st.altair_chart((fig1|(fig2+text+ban)).configure_axis(grid=False).configure_view(strokeWidth=0))'''