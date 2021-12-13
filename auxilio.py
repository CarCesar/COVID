import pandas as pd

def clasifica_df(df,menu,d,NT):
    df_faz_dash = df.query(f'date == "{d}" and continent== "{menu}"') 
    df_faz_dash = df_faz_dash.sort_values(by=[NT],ascending=False)
    return df_faz_dash

def faz_tabela_vacina(df,menu,nt):
    df1 = df.query(f'continent== "{menu}"') 
    df2 = df1[df1['people_fully_vaccinated' ].notna()]
    df3 = df2[['location','iso_code','date','people_fully_vaccinated',
               'people_fully_vaccinated_per_hundred','people_vaccinated','people_vaccinated_per_hundred','flag','continent','id']]
    df4 = df3.groupby(['location']).max().reset_index()
    #df4['date'] = df4['date'].astype('datetime64')
    df5 = df4.sort_values(by=[nt],ascending=False)
    return(df5)
        
def titulo(frase):
    a = frase.split("_")
    b = " ".join(a).title()
    return b

def tabela_group_continente(df):
    a = df[['location','date','new_cases','new_deaths','population']][df['location'].isin(['South America','Africa','Europe',
                                                                                           'Asia','Oceania','North America'])]
    a.date = a.date.astype('datetime64')
    a['continent'] = a['location']
    source = a.groupby([pd.Grouper(key="date", freq="1M"),"location",'population','continent']).sum().reset_index()
    source['new_deaths_by_population']=source.new_deaths/source.population * 10**6
    source['new_cases_by_population']=source.new_cases/source.population * 10**6
    return source

def tabela_group_pais(df):
    a = df[['location','date','new_cases','new_deaths','population']][~df['location'].isin(['South America','Africa','Europe',
                                                                                           'Asia','Oceania','North America'])]
    a.date = a.date.astype('datetime64')
    source = a.groupby([pd.Grouper(key="date", freq="1M"),"location",'population']).sum().reset_index()
    source['new_deaths_by_population']=source.new_deaths/source.population * 10**6
    source['new_cases_by_population']=source.new_cases/source.population * 10**6
    return source

def tabela_extra(df1):
    df2 = df1[df1['people_fully_vaccinated' ].notna()]
    df3 = df2[['location','iso_code','date','people_fully_vaccinated',
               'people_fully_vaccinated_per_hundred','people_vaccinated','people_vaccinated_per_hundred','flag','continent','id']]
    df4 = df3.groupby(['location']).max().reset_index()
    #df4['date'] = df4['date'].astype('datetime64')
    #df5 = df4.sort_values(by=[nt],ascending=False)
    return(df4)