def clasifica_df(df,menu,d,NT):
    df_faz_dash = df.query(f'date == "{d}" and continent== "{menu}"') 
    if NT == 'New cases':
        df_faz_dash = df_faz_dash.sort_values(by=['new_cases'],ascending=False)
    if NT == 'Total cases':
        df_faz_dash = df_faz_dash.sort_values(by=['total_cases'],ascending=False)
    if NT == 'New deaths':
        df_faz_dash = df_faz_dash.sort_values(by=['new_deaths'],ascending=False)
    if NT == 'Total deaths':
        df_faz_dash = df_faz_dash.sort_values(by=['total_deaths'],ascending=False)
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