import streamlit as st
import pandas as pd
import datetime
import altair as alt
from vega_datasets import data

### Meus arquivos

import auxilio
import mapa
import graficos

### Configurações Página

st.set_page_config(page_title='COVID-WORLD',
                   page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/facebook/65/globe-with-meridians_1f310.png',
                   layout="wide")
 

### Dados

@st.cache
def dados():
    df=pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    #df = pd.read_csv('C:/Users/carlo/Desktop/Visualização/COVID/data.csv')
    ISO = pd.read_csv('https://raw.githubusercontent.com/stefangabos/world_countries/master/data/en/countries.csv')
    #ISO = pd.read_csv('C:/Users/carlo/Desktop/Visualização/COVID/ISO.csv')
    ISO['alpha3']=[a.upper() for a in ISO['alpha3']]
    #ISO['flag']=['https://raw.githubusercontent.com/hampusborgos/country-flags/main/png100px/'+a+'.png' for a in ISO['alpha2']]
    ISO['flag']=['https://raw.githubusercontent.com/csmoore/country-flag-icons/master/country-flags-4x3-png/'+a+'.png' for a in ISO['alpha2']]
    df2=df.merge(ISO[['id','alpha3','flag']].rename(columns={'alpha3':'iso_code'}),how='inner',on='iso_code')
    return df2

# Primeiro ambiente ...
l0c1,l0c2= st.columns([3,1])
l0c1.markdown('# COVID')
P1 = l0c2.selectbox("",
     ('Cases', 'Deaths', 'Vaccination', 'Mundial','The Vis'))



### Várias faces ...

## Face 0 - CASOS      ##################################################################################################################################

if P1 == 'Cases':
    ## Linha 1 -> 2 colunas | SelectBox | Mapa | Lista |
    # face: 0 / linha: 1 / coluna:[1:3]
    
    b0, b, f0l1c1, b ,f0l1c2, f0l1c3,b= st.columns([2,2,5,1,1.5,3,1])
    NT = b0.selectbox("Total or New",('New cases','Total cases'))
    
    menu = b0.selectbox("Continente",
    ("Africa", "Europe", "South America", 'North America', "Asia", "Oceania"),
                           )
    
    d = b0.date_input('Dia',value=datetime.date(2021, 12, 10),
                              min_value= datetime.date(2020, 1, 1),
                              max_value= datetime.date(2021, 12, 10) )
    
    l0c1.markdown(' \n ')
    
    if NT =='New cases': 
        nt = 'new_cases'
    else:
        nt='total_cases'
    df = dados()
    df1 = auxilio.clasifica_df(df,menu,d,nt)
    

    
    # Mapa
    m = mapa.mapa(df1,menu,nt)
    f0l1c1.altair_chart(m)
    
    #Lista
    for num in range(4):
        if len(df1)<num+1:
            break
        paises = df1.iloc[num]
        f0l1c2.image(paises['flag'],width=70)
        f0l1c2.write(f'\~~~ {num+1}º ~~~')
        if NT =='New cases':
            f0l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['new_cases'])), 
                          delta=round((paises['new_cases']-paises['new_cases_smoothed'])/paises['new_cases_smoothed'],5),delta_color="inverse")
        else:
            f0l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['total_cases'])), delta='{0:,}'.format(int(paises['new_cases'])) 
                          ,delta_color="inverse")
    
    # Linha 2
    b,f0l2c1,b=st.columns([5,24,1])
    
    #df para grafico 2
    df2 = df1.query(f'{nt}>0')
    
    # componente linha 2
    g1 = graficos.grafico1(df2,nt)
    f0l2c1.altair_chart(g1)
    
    
## Face 1 - Mortes   ##################################################################################################################################

if P1 == 'Deaths':
    ## Linha 1 -> 2 colunas | SelectBox | Mapa | Lista |
    # face: 1 / linha: 1 / coluna:[1:3]
    
    b0, b, f1l1c1, b ,f1l1c2, f1l1c3,b= st.columns([2,2,5,1,1.5,3,1])
    NT = b0.selectbox("Total or New",('New deaths','Total deaths'))
    
    menu = b0.selectbox("Continente",
    ("Africa", "Europe", "South America", 'North America', "Asia", "Oceania"),
                           )
    
    d = b0.date_input('Dia',value=datetime.date(2021, 12, 10),
                              min_value= datetime.date(2020, 1, 1),
                              max_value= datetime.date(2021, 12, 10) )
    
    l0c1.markdown(' \n ')
    
    if NT =='New deaths': 
        nt = 'new_deaths'
    else:
        nt='total_deaths'
    df = dados()
    df1 = auxilio.clasifica_df(df,menu,d,nt)
    
    
    # Mapa
    m = mapa.mapa(df1,menu,nt,'yelloworangered')
    f1l1c1.altair_chart(m)
    
    #Lista
    for num in range(4):
        if len(df1)<num+1:
            break
        paises = df1.iloc[num]
        f1l1c2.image(paises['flag'],width=70)
        f1l1c2.write(f'\~~~ {num+1}º ~~~')
        if NT =='New deaths':
            f1l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['new_deaths'])), 
                          delta=round((paises['new_deaths']-paises['new_deaths_smoothed'])/paises['new_deaths_smoothed'],5),delta_color="inverse")
        else:
            f1l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['total_deaths'])), 
                          delta='{0:,}'.format(int(paises['new_deaths'])),delta_color="inverse")

    # Linha 2
    b,f1l2c1,b=st.columns([5,24,1])
    
    #df para grafico 2
    df2 = df1.query(f'{nt}>0')
    
    # componente linha 2
    g1 = graficos.grafico1(df2,nt)
    f1l2c1.altair_chart(g1)
    
## Face 2 - Vacinação  ##################################################################################################################################

if P1 == 'Vaccination':
    ## Linha 1 -> 2 colunas | SelectBox | Mapa | Lista |
    # face: 2 / linha: 1 / coluna:[1:3]
    
    b0, b, f2l1c1, b ,f2l1c2, f2l1c3,b= st.columns([2,2,5,1,1.5,3,1])
    NT1 = b0.selectbox("Vaccinated or Fully",('People Vaccinated','People Fully Vacinated'))
    NT2 = b0.selectbox("Total or Per Hundred",('Total','Per Hundred'))
    
    menu = b0.selectbox("Continente",
    ("Africa", "Europe", "South America", 'North America', "Asia", "Oceania"),
                           )
    
    l0c1.markdown(' \n ')
    
    if NT1 =='People Vaccinated': 
        nt0 = 'people_vaccinated'
    else:
        nt0='people_fully_vaccinated'
    if NT2 == 'Per Hundred':
        nt = nt0 + '_per_hundred'
        logaritmo = False
    else:
        nt = nt0
        logaritmo = True
    df = dados()
    df1 = auxilio.faz_tabela_vacina(df,menu,nt)

    
    # Mapa
    m = mapa.mapa(df1,menu,nt,'yellowgreen')
    f2l1c1.altair_chart(m)
    

    
    #Lista
    for num in range(4):
        if len(df1)<num+1:
            break
        paises = df1.iloc[num]
        f2l1c2.image(paises['flag'],width=70)
        f2l1c2.write(f'\~~~ {num+1}º ~~~')
        if nt0 =='people_vaccinated':
            f2l1c3.metric(label=paises['location'], value= '{0:,}'.format(int(paises['people_vaccinated'])),
                          delta=str(paises['people_vaccinated_per_hundred'])+'%',delta_color="normal")
        else:
            f2l1c3.metric(label=paises['location'], value= '{0:,}'.format(int(paises['people_fully_vaccinated'])),
                          delta=str(paises['people_fully_vaccinated_per_hundred'])+'%',delta_color="normal")


   # Linha 2
    b,f2l2c1,b=st.columns([5,24,1])
    
    # linha 3
    if nt =='Total deaths': 
        b,f2l3c1,b=st.columns([13,16,1])
        logaritmo1 = f2l3c1.checkbox('log scale')
    else:
        logaritmo1 = False
    
    # componente linha 2
    g1 = graficos.grafico2(df1,nt,nt0,logaritmo)
    f2l2c1.altair_chart(g1)