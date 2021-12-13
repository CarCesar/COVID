import streamlit as st
import pandas as pd
import datetime
import altair as alt
from vega_datasets import data

### Meus arquivos

import auxilio
import mapa
import graficos
import mundial
import vac

### Configurações Página

st.set_page_config(page_title='COVID-WORLD',
                   page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/facebook/65/globe-with-meridians_1f310.png',
                   layout="wide")
 

### Dados
@st.cache
def dadosInteiros():
    df=pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    #df = pd.read_csv('C:/Users/carlo/Desktop/Visualização/COVID/data.csv')
    ISO = pd.read_csv('https://raw.githubusercontent.com/stefangabos/world_countries/master/data/en/countries.csv')
    #ISO = pd.read_csv('C:/Users/carlo/Desktop/Visualização/COVID/ISO.csv')
    ISO['alpha3']=[a.upper() for a in ISO['alpha3']]
    #ISO['flag']=['https://raw.githubusercontent.com/hampusborgos/country-flags/main/png100px/'+a+'.png' for a in ISO['alpha2']]
    ISO['flag']=['https://raw.githubusercontent.com/csmoore/country-flag-icons/master/country-flags-4x3-png/'+a+'.png' for a in ISO['alpha2']]
    df2=df.merge(ISO[['id','alpha3','flag']].rename(columns={'alpha3':'iso_code'}),how='left',on='iso_code')
    return df2

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
     ('Boletim', 'Mundial','Vaccine','The Vis'))

if P1 == 'Boletim':
    b0, b, l1c1, b ,l1c2, l1c3,b= st.columns([2,2,5,1,1.5,3,1])
    P2 = b0.selectbox('TYPE:',['Cases', 'Deaths', 'Vaccination'])
    ### Várias faces ...

    ## Face 0 - CASOS      ##################################################################################################################################

    if P2 == 'Cases':
        ## Linha 1 -> 2 colunas | SelectBox | Mapa | Lista |
        # face: 0 / linha: 1 / coluna:[1:3]


        NT = b0.selectbox("Total or New",('New cases','Total cases'))

        menu = b0.selectbox("Continente",
        ("Africa", "Europe", "South America", 'North America', "Asia", "Oceania"),
                               )

        d = b0.date_input('Dia',value=datetime.date(2021, 12, 1),
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
        l1c1.altair_chart(m)

        #Lista
        for num in range(4):
            if len(df1)<num+1:
                break
            paises = df1.iloc[num]
            l1c2.image(paises['flag'],width=70)
            l1c2.write(f'\~~~ {num+1}º ~~~')
            if NT =='New cases':
                l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['new_cases'])), 
                              delta=round((paises['new_cases']-paises['new_cases_smoothed'])/paises['new_cases_smoothed'],5),delta_color="inverse")
            else:
                l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['total_cases'])), delta='{0:,}'.format(int(paises['new_cases'])) 
                              ,delta_color="inverse")

        # Linha 2
        b,f0l2c1,b=st.columns([5,24,1])

        #df para grafico 2
        df2 = df1.query(f'{nt}>0')

        # componente linha 2
        g1 = graficos.grafico1(df2,nt)
        f0l2c1.altair_chart(g1)


    ## Face 1 - Mortes   ##################################################################################################################################

    if P2 == 'Deaths':
        ## Linha 1 -> 2 colunas | SelectBox | Mapa | Lista |
        # face: 1 / linha: 1 / coluna:[1:3]

        #b0, b, f1l1c1, b ,f1l1c2, f1l1c3,b= st.columns([2,2,5,1,1.5,3,1])
        NT = b0.selectbox("Total or New",('New deaths','Total deaths'))

        menu = b0.selectbox("Continente",
        ("Africa", "Europe", "South America", 'North America', "Asia", "Oceania"),
                               )

        d = b0.date_input('Dia',value=datetime.date(2021, 12, 1),
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
        l1c1.altair_chart(m)

        #Lista
        for num in range(4):
            if len(df1)<num+1:
                break
            paises = df1.iloc[num]
            l1c2.image(paises['flag'],width=70)
            l1c2.write(f'\~~~ {num+1}º ~~~')
            if NT =='New deaths':
                l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['new_deaths'])), 
                              delta=round((paises['new_deaths']-paises['new_deaths_smoothed'])/paises['new_deaths_smoothed'],5),delta_color="inverse")
            else:
                l1c3.metric(label=paises['location'], value='{0:,}'.format(int(paises['total_deaths'])), 
                              delta='{0:,}'.format(int(paises['new_deaths'])),delta_color="inverse")

        # Linha 2
        b,f1l2c1,b=st.columns([5,24,1])

        #df para grafico 2
        df2 = df1.query(f'{nt}>0')

        # componente linha 2
        g1 = graficos.grafico1(df2,nt)
        f1l2c1.altair_chart(g1)

    ## Face 2 - Vacinação  ##################################################################################################################################

    if P2 == 'Vaccination':
        ## Linha 1 -> 2 colunas | SelectBox | Mapa | Lista |
        # face: 2 / linha: 1 / coluna:[1:3]

        #b0, b, f2l1c1, b ,f2l1c2, f2l1c3,b= st.columns([2,2,5,1,1.5,3,1])
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
        l1c1.altair_chart(m)



        #Lista
        for num in range(4):
            if len(df1)<num+1:
                break
            paises = df1.iloc[num]
            l1c2.image(paises['flag'],width=70)
            l1c2.write(f'\~~~ {num+1}º ~~~')
            if nt0 =='people_vaccinated':
                l1c3.metric(label=paises['location'], value= '{0:,}'.format(int(paises['people_vaccinated'])),
                              delta=str(paises['people_vaccinated_per_hundred'])+'%',delta_color="normal")
            else:
                l1c3.metric(label=paises['location'], value= '{0:,}'.format(int(paises['people_fully_vaccinated'])),
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
    
####################### Mundo #######################################
if P1=='Mundial':
    st.markdown(' ')
    mundial1,mundial2 = st.columns([1,2])
    df = dadosInteiros()
    df1 = df.query(f'date == "2021-12-09"') 
    df_cont = auxilio.tabela_group_continente(df)
    df_pais= auxilio.tabela_group_pais(df)
    selectMundial = mundial1.selectbox('Data',['New Deaths','New Deaths by Pop','New Cases','New Cases by Pop'])
    dicmunsel={'New Deaths':'new_deaths','New Deaths by Pop':'new_deaths_by_population','New Cases':'new_cases','New Cases by Pop':'new_cases_by_population'}
    mundial1.markdown(' ')
    cb=mundial.mapa_mundi(df1)
    mundial1.altair_chart(cb)
    if selectMundial in ['New Deaths by Pop','New Cases by Pop']:
        mundial1.markdown('''<div id = 'tudo' style='font-family: "Courier", Courier, monospace;'>Frequency in a million people</div>''',unsafe_allow_html=True)
    bc = mundial.bump_chart(df_cont,dicmunsel[selectMundial])
    mundial2.altair_chart(bc)
    
    
     
#################################################################################    
if P1=='Vaccine':
    df=dados()
    df=auxilio.tabela_extra(df)
    vac = vac.vaq1(df)
    st.markdown(' ')
    b,area,b=st.columns([1,3,1])
    area.altair_chart(vac)
    
    
    
    
    
################################## Escrita ######################################
if P1=='The Vis':
    st.markdown("""
    <div id = 'tudo' style='font-family: "Courier", Courier, monospace;'>
    <h2 id = 'h1' style='font-family: "Courier", Courier, monospace;'>O trabalho</h2>
    <div class = 'tr' style='font-family: "Courier", Courier, monospace;'>Este é meu trabalho  de Visualização da Informação do Mestrado em Modelagem Matematica da EMAP - FGV, com a professora Asla.</div>
        
    <h2 style='font-family: "Courier", Courier, monospace;'>A ideia</h2>
    <p style='font-family: "Courier", Courier, monospace;'>Minha ideia a principio foi pegar dados que tivessem dados temporais e espaciais pois eu queria muito utilizar mapa. Portanto, depois de algumas pesquisas resolvi pegar os dados de COVID pelo mundo.
    Depois de estudar um pouco sobre os dados cheguei a conclusão que teria 3 grandes grupos importantes <em>Casos</em>, <em>Mortes</em> e <em>Vacinação</em>.
    </p>

    <h3 style='font-family: "Courier", Courier, monospace;'>Casos</h3>
    <p style='font-family: "Courier", Courier, monospace;'>Dentro de casos teve 2 subgrupos que achei legal para fazer analise,<em>Novos Casos</em>, aonde a gente tem um nivel de como está a covid em determinado local em tal dia. 
        E <em>Total de Casos</em> aonde a gente vê como foi a covid em tal lugar até determinado dia.</p>
    <h3 style='font-family: "Courier", Courier, monospace;'>Mortes</h3>
    <p style='font-family: "Courier", Courier, monospace;'>Em mortes, novamente, foram 2 subgrupos que achei legal para fazer analise,<em>Novas Mortes</em>, em que a gente tem uma ideia de como a covid esta ceifando vidas em determinado local hoje, ou em tal dia. 
            E <em>Total de Mortes</em> aonde a gente vê quão devastador foi a covid em tal lugar até determinado dia.</p>
    <h3 style='font-family: "Courier", Courier, monospace;'>Vacinação</h3>
    <p style='font-family: "Courier", Courier, monospace;'>
        Aqui não seria possivel fazer uma analise relacionada aos vaicnados naquele dia, pois tinha vários dados faltantes. 
        Porém diferente dos demais, o objetivo é que toda a população seja vacinada e além disso, seja totalmente vacinada.
        Portanto, perdemos a variavel tempo, porém ganhamos as variaveis <em>Vacinadas</em> e <em>Totalmente Vacinadas</em>, e cada uma delas ainda pode ser a quantidade total ou um porcentagem da população total.
    </p>
    <h2 style='font-family: "Courier", Courier, monospace;'>Execução</h2>
    <h3 style='font-family: "Courier", Courier, monospace;'>Info</h3>
    </div>

    <style>
        h2{color:#AAAAFF}
        em{color:#CCCCFF}
        h3{color:#BBBBFF}
    </style>
    
    """,unsafe_allow_html=True)
    v1,v2 = st.columns(2)
    v1.markdown('''<p style='font-family: "FreeMono", monospace;'>Para começar, peguei os dados de casos, fiz os seletores de 'New Cases' ou 'Total Cases',  de Continente e de Data. Em seguida fiz um mapa onde representei os dados no espaço, do lado coloquei uma lista dos paises que tinham mais insidentes entre os dados selecionados. Quando selecionado 'New Cases', o número grande indica os novos casos naquele dia, e o númerozinho representa a taxa de crescimento, quando selecionado 'Total Cases', o número grande indica o total de casos registrados até aquele dia e número pequeno os novos casos daquele dia.
    Em seguida fiz um scater plot em que o x é o Total de Casos (log) e o y é o Total de Mortes (log), em ambos os casos preferi a escala log. O tamanho dos circulos representa a quantidade de Novos ou Total de Casos a depender de qual foi escolhido, do lado e interligado está um bar plot em no y estão os paises, enquanto no x está Total ou Novos Casos a depender da escolha, porém aqui, os dados estão em escala log. Ao escolher uma barra ou um circulo, os dados relacionados irão acendere definir varias informações.
    Todo o processo feito aqui foi repetido para Mortes com algumas edições nas cores.
    </p>
    ''',unsafe_allow_html=True)
    v2.image('casos.png')
    v3,v4=st.columns(2)
    v3.image('vac.png')
    v4.markdown("""<p style='font-family:"Courier", monospace;'>
    A ideia para Vacinação era fazer a mesma coisa que fiz para casos e para mortes, porém ao analisar os dados vi que não eram todos os dias que eram lançado os dados de todos os paises. Daria para fazer, mas eu teria que manipular os dados e não sei o trabalho mais facil do mundo. Além disso, toda a população de todo pais é para ser vacinada, além disso, totalmente vacinada. Então peguei os ultimos dados lançados de cada pais e fiz um mapa e uma lista muito parecidos, na lista aparecia os números de vacinados e a porcentagem da população que já se imunizou.
    Na hora de fazer os scater plot coloquei no eixo x a data do ultimo lançamento e no y os paises, o tamanho dos circulos é a quantia selecionada que também está representada no eixo x no gráfico de barras (se escolheu ver a quantia Total ele estará em log), no eixo y do grafico de barras estão os paises. Novamente, se selecionar um circulo ou uma barra dados do pais selecionado irão aparecer pela tela.
   </p>
    """,unsafe_allow_html=True)
    
    
    st.markdown("""<p style='font-family:"Courier", monospace;'>
    Após ter feito isso, achei que estava faltando algo mais relacionado com os dados temporais...
   </p>
   
   <h3 style='font-family: "Courier", Courier, monospace;'>Epicentro</h3>
   <p style='font-family:"Courier", monospace;'>
    Meio na dúvida do que fazer, pensei que seria legal algum grafico que permitisse uma analise temporal, nesse caso o melhor contexto que achei, além de ser um assunto bem amplo, é 'Qual o epicentro da pandemia?', sabemos que esse epicentro é fluido, hoje é um lugar, hoje pode ser outro totalmente diferente, então tentei resolver esse problema com a visualização. Para começar, me perguntei como vou definir que o continente epicentro da pandemia?  
   </p>
   
   <em style='font-family:"Courier", monospace;'>
    Será que seria o continente que tem mais casos em tal periodo de tempo?
   </em>
   <br>
   <br>
   <em style='font-family:"Courier", monospace;'>
     Ou será o pais que tem mais mortes?
   </em>
   <br>
   <br>
   <em style='font-family:"Courier", monospace;'>
    Será que é certo perguntar pelo mais, ou seria melhor perguntar pelo que tem mais incidencias dadas as populações?
   </em>
   <br>
   <br>
   <p style='font-family:"Courier", monospace;'>
    É... Achei todos os contextos validos. Então resolvi fazer um seletor onde o usuario pode selecionar. Falando da visualização propriamente dita, fiz um 'Bump Chart' e abaixo dele um 'Heapmap' com uma legenda que permite a seleção de um continente ao lado, eu queria utilizar o mapa como a legenda ligada que seleciona os continentes, porém após alguma pesquisa vi que ainda não é possivel, porém coloquei o mapa ao lado para dar um charme e ser uma legenda auxiliar.
    Ao selecionar um continente, as linhas dos outros continentes ficam mais claras evidenciando o continente escolhido, no heapmap os outros continentes somem e o grafico de barras que está no fundo fca mais visivel (Não sei se sobrecarrega a visualização, porém achei legal as cores em um primeiro plano e as linhas evidenciando as quantidades indicadas pelas cores no heapmap). A visualização foi essa:
   </p>
   
   <style>
        h2{color:#AAAAFF}
        em{color:#CCCCFF}
        h3{color:#BBBBFF}
    </style>
    """,unsafe_allow_html=True)
    
    b,v5,b=st.columns([1,2,1])
    v5.image('epi.png')
    
    st.markdown("""   
   <h3 style='font-family: "Courier", Courier, monospace;'>Vacinas</h3>
   <p style='font-family:"Courier", monospace;'>
    É muitas vezes ao vermos as notícias, tem algo relacionado com a OMS pedindo que os paises ricos tambem se solidarizem com os países mais pobres, principalmente os africanos. Então resolvi fazer essa visualização para ver como estão os paises de cada continente na vacinação. Para tal fiz um heatmap com sobreposição de um scater plot. Para finalizar coloquei as legendas aos lados e uma marquinha para cada pais na região do seu continente. Coloquei a interatividade ao clicar nas legendas do mapa.
   </p>
   
   <style>
        h2{color:#AAAAFF}
        em{color:#CCCCFF}
        h3{color:#BBBBFF}
    </style>
    """,unsafe_allow_html=True)
    
    b,v6,b=st.columns([1,2,1])
    v6.image('hep.png')
    
    v7,b,v8,v9=st.columns([20,1,10,8])
    
    v7.markdown("""   
   <h3 style='font-family: "Courier", Courier, monospace;'>Bibliografia</h3>
   <p style='font-family:"Courier", monospace;'>
    Para fazer esse trabalho eu utilizei as bibliotecas Streamlit e Altair de Python. E consegui os dados utilizados nesse trabalho em:
   </p>
   <a style='font-family:"Courier", monospace;' href='https://covid.ourworldindata.org/data/owid-covid-data.csv'>
    Our World in Data
   </a>
   <br>
   <a style='font-family:"Courier", monospace;' href='https://github.com/stefangabos/world_countries/blob/master/data/en/countries.csv'>
    ISO CODE
   </a>
   <br>
   <a style='font-family:"Courier", monospace;' href='https://github.com/csmoore/country-flag-icons/'>
    Bandeiras
   </a>
   
   <style>
        h2{color:#AAAAFF}
        em{color:#CCCCFF}
        h3{color:#BBBBFF}
    </style>
    """,unsafe_allow_html=True)
    
    v8.markdown("""   
   <h3 style='font-family: "Courier", Courier, monospace;'>Quem Fez?</h3>
   <p style='font-family:"Courier", monospace;'>
    Carlos César Fonseca é estudante do 4º periodo(2021-2) de Ciência de Dados da Emap - FGV.
   </p>
   <p style='font-family:"Courier", monospace;'>
    As vezes perdido, as vezes insano, mas no fundo com todo mundo é...
   </p>
   <p style='font-family:"Courier", monospace;'>
    A pessoa da foto...
   </p>
   
   <style>
        h2{color:#AAAAFF}
        em{color:#CCCCFF}
        h3{color:#BBBBFF}
    </style>
    """,unsafe_allow_html=True)
    
    v9.image('carl.jpeg')
st.markdown('''<style>
                    body{font-family: "Courier", Courier, monospace;}
                    [data-baseweb]{font-family: "Courier", Courier, monospace;}
                </style>''',unsafe_allow_html=True)
