import altair as alt

cor=['#13A891','#F09001','#9653F5','#34A52B','#F52232','#F5C129']

def vaq1(df):
    # Seletor de continente
    click = alt.selection_multi(fields=['continent'])
    
    # Base
    danone = alt.Chart(df)
    
    #escalas
    xscale = alt.Scale(domain=(0, 100))
    yscale = alt.Scale(domain=(0, 100))
    
    # heatmap
    retas= danone.mark_rect().encode(x = alt.X('people_vaccinated_per_hundred',bin=True,scale=xscale,axis = alt.Axis(titleFont='Courier',
                                                                                                                          title='People Vaccinated (%)')),
                                     y = alt.Y('people_fully_vaccinated_per_hundred',bin=True,scale=yscale,axis = alt.Axis(titleFont='Courier',
                                                                                                                        title='People Fully Vaccinated (%)')),
                                     color= alt.Color('count()',legend=alt.Legend(orient='bottom-right',titleFont='Courier'))).properties(width=400,height=400
                                                                                                                     ).transform_filter(click)
    
    # scater plot 
    point = danone.mark_circle(stroke='black',strokeWidth=0.7).encode(
        alt.X('people_vaccinated_per_hundred', scale=xscale,axis=alt.Axis(grid=True,domain=False,title=None,labels=False,ticks=False)),
        alt.Y('people_fully_vaccinated_per_hundred', scale=yscale,axis=alt.Axis(grid=True,domain=False,title=None,labels=False,ticks=False)),
        color=alt.Color('continent',legend=None,scale=alt.Scale(range=cor)),#scheme='dark2')),
        opacity=alt.condition(click,alt.value(1),alt.value(.1)),
        size = alt.Size('people_fully_vaccinated',scale=alt.Scale(type='log',
                                                                  range=(1,175)),legend=alt.Legend(orient='right',title='Fully Vaccinated - log',
                                                                                                   titleFont='Courier',labelFont='Courier'))
    ).properties(width=400,height=400)
    
    # tooltips scater
    point1 = point.encode(opacity=alt.value(0),tooltip=['location',
                                                        alt.Tooltip('people_vaccinated_per_hundred',title='Vaccinated %'),
                                                        alt.Tooltip('people_fully_vaccinated_per_hundred',title='FULL vac. %'),
                                                        alt.Tooltip('people_fully_vaccinated',title='FULL vac'),'date']).transform_filter(click)
    # scater + tooltips
    points=(point+point1).add_selection(click)
    
    
    # legendas
    l1 = danone.mark_rect().encode(y=alt.Y('continent',axis=alt.Axis(domain = False,ticks=False,
                                                                              orient='left',labelFont='Courier',
                                                                              title=None)),
                                                                              color=alt.condition(click,
                                                                                                  alt.Color('continent:N',legend=None,
                                                                                                            scale=alt.Scale(range=cor)),#scheme='dark2')),
                                                                                                  alt.value('lightgray'))
                                                                              ).properties(width=400,height=100,).add_selection(click)
    
    l2 = danone.mark_rect().encode(x=alt.X('continent:N',scale = alt.Scale(),
                                           axis=alt.Axis(domain = False,ticks=False,
                                                                              orient='bottom',labelFont='Courier',
                                                                              title=None)),
                                                                              color=alt.condition(click,
                                                                                                  alt.Color('continent:N',legend=None,
                                                                                                            scale=alt.Scale(range=cor)),#scheme='dark2')),
                                                                                                  alt.value('lightgray'))
                                                                              ).properties(width=100,height=400,).add_selection(click)
    
    # marquinhas
    x_ticks = danone.mark_tick(color = 'lightgrey').encode(
        alt.X('people_vaccinated_per_hundred', axis=alt.Axis(labels=False, domain=False, ticks=False,title=None),scale=xscale),
        alt.Y('continent', title='', axis=alt.Axis(labels=True, domain=False, ticks=False,title=None)),
    )
    
    y_ticks = danone.mark_tick(color = 'lightgrey').encode(
        alt.X('continent', title='', axis=alt.Axis(labels=True, domain=False, ticks=False,title=None)),
        alt.Y('people_fully_vaccinated_per_hundred', axis=alt.Axis(labels=False, domain=False, ticks=False,title=None),scale=yscale),
    )
    
    
    return alt.vconcat((l1 + x_ticks),
                       alt.hconcat((retas+points).resolve_scale(x = 'independent',y='independent'),
                                   (l2+y_ticks),spacing=0),
                       spacing=0).properties(title='Vaccine around the World').configure_view(strokeWidth=0
                                                ).configure_title(fontSize=30,
                                                                  font='Courier',
                                                                  anchor='end',
                                                                  color='gray',
                                                                  orient='left'
                                                                 )