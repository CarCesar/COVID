import altair as alt

import auxilio

def grafico1(df,col,logaritmo = False):
    click1 = alt.selection_multi(fields=['location'],empty='none')
    fig1 = alt.Chart(df).mark_circle(color = 'orange').encode(x=alt.X('total_cases:Q',scale=alt.Scale(type='log'),axis=None),
                                   y=alt.Y('total_deaths:Q',scale=alt.Scale(type='log',zero=True),axis=None),#axis=None
                                   size=alt.Size(f'{col}',legend = alt.Legend(orient='top-left')),
                                   color = alt.condition(click1,alt.value('#F8202A'),alt.value('lightgray')),
                                   tooltip = ['location',f'{col}']
                                                             ).properties(width=350, height=350).add_selection(click1)
    if logaritmo:
        fig2 = alt.Chart(df).mark_bar().encode(x=alt.X(f'{col}',scale=alt.Scale(type='log')),
                                       y=alt.Y('location',sort='-x',axis=None),
                                       tooltip = 'location',
                                        color = alt.condition(click1,
                                                              alt.value('#F8202A'),
                                                              alt.value('lightgray'))
                                               ).properties(width=700,height=350).add_selection(click1)
    else:
        fig2 = alt.Chart(df).mark_bar().encode(x=alt.X(f'{col}'),
                                       y=alt.Y('location',sort='-x',axis=None),
                                       tooltip = 'location',
                                        color = alt.condition(click1,
                                                              alt.value('#F8202A'),
                                                              alt.value('lightgray'))
                                               ).properties(width=700,height=350).add_selection(click1)
    
    text = alt.Chart(df).mark_text(x=350,y=300,color = 'white'
                                   ).encode(text=alt.condition(click1,alt.Text('location:N'),alt.value('')),
                                           ).properties(width=700,height=350
                                                       ).transform_calculate(label='datum.location')
    
    ban = alt.Chart(df).mark_image(width=50,x=600,y=300
                                    ).encode(url='flag',opacity = alt.condition(click1,
                                                                  alt.value(1),
                                                                  alt.value(0))

                                           ).properties(width=700,height=350
                                                       )
    
    return (fig1|(fig2+text+ban)).configure_axis(grid=False).configure_view(strokeWidth=0)


def grafico2(df,col,nt):
    click1 = alt.selection_multi(fields=['location'],empty='none')
    fig1 = alt.Chart(df).mark_circle(color = 'orange').encode(x=alt.X('date',
                                                                     #scale=alt.Scale(type='log',domain = ['min(x)','max(x)']),
                                                                     axis=alt.Axis(ticks = False,
                                                                                   labels = True , domain = False, grid = True,
                                                                                   gridOpacity=0.2,
                                                                                   title = auxilio.titulo('Date'))),
                                   y=alt.Y('location',
                                           sort='-size',
                                           scale=alt.Scale(type='log',zero=True),
                                           axis=alt.Axis(ticks = False, grid = True, gridOpacity = 0.1,
                                                         labels = False , domain = False,
                                                         title = auxilio.titulo('Country'))),
                                   size=alt.Size(f'{col}',legend = alt.Legend(orient='top-left',
                                                                              title=None,
                                                                              labelFontSize=8)),
                                   color = alt.condition(click1,alt.value('#055916'),alt.value('lightgray')),
                                   opacity = alt.condition(click1,alt.value(1), alt.value(.3)),
                                   tooltip = ['location',f'{col}']
                                                             ).properties(width=350, height=350).add_selection(click1)

    fig2 = alt.Chart(df).mark_bar().encode(x=alt.X(f'{col}',axis=alt.Axis(title = auxilio.titulo(col),domain=False)),
                                       y=alt.Y('location',sort='-x',axis=alt.Axis(labels = False , domain = False,title=None,tickSize=8,tickOpacity=0.1)),
                                       tooltip = 'location',
                                        color = alt.condition(click1,
                                                              alt.value('#055916'),
                                                              alt.value('lightgray'))
                                               ).properties(width=700,height=350).add_selection(click1)
    
    text = alt.Chart(df).mark_text(align='right',x=698,y=246,color = 'white',font='Courier',fontSize=20
                                   ).encode(text=alt.condition(click1,alt.Text('location:N'),alt.value('')),
                                           ).properties(width=700,height=350
                                                       ).transform_calculate(label='datum.location + " oi"')
    
    text0 = alt.Chart(df).mark_text(align='right',x=698,y=230,color = 'white',font='Courier',fontSize=10
                                   ).encode(text=alt.condition(click1,alt.Text('date:N'),alt.value('')),
                                           ).properties(width=700,height=350
                                                       ).transform_calculate(label='datum.location + " oi"')
    
    text1 = alt.Chart(df).mark_text(align='right',x=698,y=264,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=700,height=350
                                                       ).transform_calculate(label=f'datum.{nt} + " people"')
    
    nt0 = nt + '_per_hundred'
    
    text2 = alt.Chart(df).mark_text(align='right',x=698,y=280,color = 'white',fontSize=15,font='Courier'
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=700,height=350
                                                       ).transform_calculate(label=f'datum.{nt0} + " %"')
    
    ban = alt.Chart(df).mark_image(width=80,x=660,y=290
                                    ).encode(url='flag',opacity = alt.condition(click1,
                                                                  alt.value(1),
                                                                  alt.value(0))
                                            ).properties(width=700,height=350)
    
    return (fig1|(fig2+text+text0+text1+text2+ban)).configure_axis(grid=False).configure_view(strokeWidth=0)