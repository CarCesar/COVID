import altair as alt

import auxilio


# Case e Deaths
def grafico1(df,col):
    t = len(df)
    if t<30:
        t=30
    
    click1 = alt.selection_multi(fields=['location'],empty='none')
    
    # scatter
    fig1 = alt.Chart(df).mark_circle(color = 'orange').encode(x=alt.X('total_cases:Q',scale=alt.Scale(type='log'),axis=alt.Axis(ticks = False,
                                                                                   labels = True , labelOpacity = 0.5, labelAngle=-90,labelFontSize=8,
                                                                                   domain = True,domainOpacity = 0.5, grid = False, titleFontSize=10,
                                                                                   titleFont='Courier',titleOpacity=0.5,
                                                                                   title = 'Total Cases (log)')),
                                   y=alt.Y('total_deaths:Q',scale=alt.Scale(type='log'),axis=alt.Axis(ticks = False,
                                                                                   labels = True , labelOpacity = 0.5,labelFontSize=8,
                                                                                   domain = True,domainOpacity = 0.5, grid = False,titleFontSize=10,
                                                                                   titleFont='Courier',titleOpacity=0.5,
                                                                                   title = 'Total Deaths (log)')),#axis=None
                                   size=alt.Size(f'{col}',legend = alt.Legend(orient='top-left',titleFont='Courier',
                                                                              title=auxilio.titulo(col),titleOpacity=0.8,
                                                                              labelOpacity=0.5)),
                                   color = alt.condition(click1,alt.value('#F8202A'),alt.value('#696662')),
                                   opacity = alt.condition(click1,alt.value(1), alt.value(.3)),
                                   tooltip = ['location',f'{col}']
                                                             ).properties(width=350, height=400).add_selection(click1)
    
    # Total cases
    text1_1 = alt.Chart(df).mark_text(align='right',x=350,y=300,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=350,height=400
                                                       ).transform_calculate(label='"TOTAL CASES:"')
    
    # numero total cases
    text1_2 = alt.Chart(df).mark_text(align='right',x=345,y=325,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text('total_cases:Q',format=',d'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    
    #Total Deaths
    text1_3 = alt.Chart(df).mark_text(align='right',x=350,y=350,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=350,height=400
                                                       ).transform_calculate(label='"TOTAL DEATHS:"')
    
    #Numero de total de mortos
    text1_4 = alt.Chart(df).mark_text(align='right',x=345,y=375,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text('total_deaths:Q',format=',d'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    
    # barras
    fig2 = alt.Chart(df).mark_bar().encode(x=alt.X(f'{col}',scale=alt.Scale(type='log'),axis=alt.Axis(
                                                                                   labels = True ,titleFontSize=13,
                                                                                   titleFont='Courier',titleOpacity=0.8,labelOpacity=0.8,
                                                                                   domain = True,domainOpacity = 0.5,
                                                                                    title = auxilio.titulo(col)+" (log)")),
                                       y=alt.Y('location',sort='-x',axis=None),
                                       tooltip = 'location',
                                        color = alt.condition(click1,
                                                              alt.value('#F8202A'),
                                                              alt.value('#696662'))
                                               ).properties(width=700,height=400)#.add_selection(click1)
   
    
    ###### Nome nas barras...
    fig3 = alt.Chart(df).mark_text(size = 400/(t+10),color='white',align = 'left',x=5,font='Courier').encode(
                                        y = alt.Y('location:N',sort=alt.EncodingSortField(field=f'{col}',order='descending')),
                                       #y=alt.Y('location',sort='-x',axis=alt.Axis(labels = False , domain = False,title=None,tickSize=8,tickOpacity=0.1)),
                                       #tooltip = 'location',
                                       text = alt.Text('iso_code:N'),
                                        color = alt.condition(click1,
                                                              alt.value('white'),
                                                              alt.value('white')),
                                               ).properties(width=700,height=400)
    
    ##### Nome Pais
    text = alt.Chart(df).mark_text(align='right',x=698,y=286,color = 'white',font='Courier',fontSize=20
                                   ).encode(text=alt.condition(click1,alt.Text('location:N'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    
    text2_1 = alt.Chart(df).mark_text(align='right',x=698,y=322,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text(f'{col}:Q',format=',d'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    
    text2_2 = alt.Chart(df).mark_text(align='right',x=698,y=304,color = 'white',font='Courier',fontSize=12
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       ).transform_calculate(label=f'"{auxilio.titulo(col).upper()}:"')
    
    ##### Bandeira
    ban = alt.Chart(df).mark_image(width=80,x=660,y=328
                                    ).encode(url='flag',opacity = alt.condition(click1,
                                                                  alt.value(1),
                                                                  alt.value(0))
                                            ).properties(width=700,height=400)
    
    barnome = (fig2+fig3).add_selection(click1)
    
    return ((fig1+text1_1+text1_2+text1_3+text1_4)|(barnome+text+ban+text2_1+text2_2)).configure_axis(grid=False).configure_view(strokeWidth=0
                                    )#.properties(title = auxilio.titulo(col)).configure_title(font='Courier',fontSize=25)
    #(fig4 + fig2+text+ban+fig3).add_selection(click1)

###########################################################################################################################################################
###########################################################################################################################################################
# Vacination
def grafico2(df,col,nt,logaritmo):
    t = len(df)
    if t<30:
        t=30
    click1 = alt.selection_multi(fields=['location'],empty='none')
    fig1 = alt.Chart(df, ).mark_circle(color = 'orange').encode(x=alt.X('date',
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
                                                             ).properties(width=350, height=400).add_selection(click1)
    ############################### TOTAL OU % #######################################################################################################
    if logaritmo:
        fig2 = alt.Chart(df).mark_bar().encode(x=alt.X(f'{col}',axis=alt.Axis(title = auxilio.titulo(col)+' (log)',domain=False,labelAngle = -90,
                                                                              ),scale=alt.Scale(type='log')),
                                       y=alt.Y('location',sort='-x',axis=alt.Axis(labels = False , domain = False,title=None,tickSize=8,tickOpacity=0.1)),
                                       tooltip = 'location',
                                        color = alt.condition(click1,
                                                              alt.value('#055916'),
                                                              alt.value('lightgray'))
                                               ).properties(width=700,height=400).add_selection(click1)
    else:
        fig2 = alt.Chart(df).mark_bar().encode(x=alt.X(f'{col}',axis=alt.Axis(title = auxilio.titulo(col),domain=False)),
                                       y=alt.Y('location',sort='-x',axis=alt.Axis(labels = False , domain = False,title=None,tickSize=8,tickOpacity=0.1)),
                                       tooltip = 'location',
                                        color = alt.condition(click1,
                                                              alt.value('#055916'),
                                                              alt.value('lightgray'))
                                               ).properties(width=700,height=400).add_selection(click1)
        
    ############################## Escrita..... #####################################################################################################
    
    ###### Nome nas barras...
    fig3 = alt.Chart(df).mark_text(size = 400/(t+10),color='white',align = 'left',x=5,font='Courier').encode(
                                        y = alt.Y('location:N',sort=alt.EncodingSortField(field=f'{col}',order='descending')),
                                       #y=alt.Y('location',sort='-x',axis=alt.Axis(labels = False , domain = False,title=None,tickSize=8,tickOpacity=0.1)),
                                       #tooltip = 'location',
                                       text = alt.Text('iso_code:N'),
                                        color = alt.condition(click1,
                                                              alt.value('white'),
                                                              alt.value('black')),
                                               ).properties(width=700,height=400)#.add_selection(click1)
    
    ###### Nome Pais
    text = alt.Chart(df).mark_text(align='right',x=698,y=286,color = 'white',font='Courier',fontSize=20
                                   ).encode(text=alt.condition(click1,alt.Text('location:N'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    
    ###### Data
    text0 = alt.Chart(df).mark_text(align='right',x=698,y=270,color = 'white',font='Courier',fontSize=10
                                   ).encode(text=alt.condition(click1,alt.Text('date:N'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    
    ##### Quantidade vacinados
    text1 = alt.Chart(df).mark_text(align='right',x=635,y=304,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text(f'{nt}:Q',format=',d'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       )
    ##### Quantidade vacinados parte 2
    text3 = alt.Chart(df).mark_text(align='right',x=698,y=304,color = 'white',font='Courier',fontSize=15
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       ).transform_calculate(label='"people"')
    
    nt0 = nt + '_per_hundred'
    
    ##### Porcentagem de vacinados
    text2 = alt.Chart(df).mark_text(align='right',x=698,y=322,color = 'white',fontSize=15,font='Courier'
                                   ).encode(text=alt.condition(click1,alt.Text('label:N'),alt.value('')),
                                           ).properties(width=700,height=400
                                                       ).transform_calculate(label=f'datum.{nt0} + " %"')
    
    ##### Bandeira
    ban = alt.Chart(df).mark_image(width=80,x=660,y=328
                                    ).encode(url='flag',opacity = alt.condition(click1,
                                                                  alt.value(1),
                                                                  alt.value(0))
                                            ).properties(width=700,height=400)
    
    ###########    Retorno... ##############
    return (fig1|(fig2+fig3+text+text0+text1+text2+ban+text3)).configure_axis(grid=False).configure_view(strokeWidth=0).properties(
    title = auxilio.titulo(col)
)