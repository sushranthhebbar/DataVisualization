import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('unece.csv')

df['Total females'] = df['Population aged 0-14, female'] + df['Population aged 15-64, female'] + df['Population aged 64+, female']


df.replace(to_replace ="The former Yugoslav Republic of Macedonia",
                 value ="Macedonia",inplace=True)

df.replace(to_replace ="Moldova, Republic of",
                 value ="Moldova",inplace=True)


countries = np.sort(list(set(df['Country'])))

conti_dict = {'AS':['Georgia',
  'Turkmenistan',
  'Israel',
  'Azerbaijan',
  'Armenia',
  'Kazakhstan',
  'Kyrgyzstan',
  'Cyprus',
  'Turkey',
  'Uzbekistan',
  'Tajikistan'],'NA':['Canada', 'United States']}

conti_dict['WE'] = ['Belgium','Denmark','Finland','France', 'Germany', 'Iceland','Ireland','Italy','Luxembourg','Malta','Netherlands','Norway','Portugal','Spain', 'Sweden','Switzerland','United Kingdom']
conti_dict['EE'] = ['Albania', 'Austria','Belarus','Bosnia and Herzegovina','Bulgaria','Croatia', 'Czechia','Estonia', 'Greece', 'Hungary','Latvia','Lithuania','Macedonia', 'Moldova','Montenegro','Poland','Romania','Russian Federation','Serbia','Slovakia', 'Slovenia','Ukraine']

prev = conti_dict

df_countries = df.groupby('Country')

parallel_columns = ['Total population, male (%)','Total population, female (%)','Life expectancy at birth, women','Life expectancy at birth, men', 'Total fertility rate']

hie_column = ['Total females','Total fertility rate']

#The below function removes countries from the dictionary d if they have more missing values than thresh with respect to the variable column
#The thresh value is either 2 or mode of the list n if mode is less than 2
def f(column,d):
    n=[]
    for country in countries:
        df_country = df_countries.get_group(country)
        n.append(df_country[column].isna().sum())
    mod = max(set(n), key=n.count)
    thresh = min(2,mod)
#     m=np.mean(n)
#     print(m)
#     print(n)
#     print(len(n))
#     return
    for i in range(len(n)):
        if(n[i]>thresh):
            n[i]=0
        else:
            n[i]=1
    for i in range(len(countries)):
        country = countries[i]
        if(n[i]==0):
            for k in d.keys():
                l = d[k]
                if(country in l):
                    d[k].remove(country)
                    break
    return d


for column in parallel_columns:
    prev = f(column,prev)

print(len(prev['EE']),
len(prev['WE']),
len(prev['NA']),
len(prev['AS']))


df_columns = ['Time','Region','Country','Color','Total population, male (%)','Total population, female (%)','Life expectancy at birth, women','Life expectancy at birth, men', 'Total fertility rate']

hie_columns = ['Time','Region','Country', 'Color' ,'Total females','Total fertility rate']

hie = pd.DataFrame(columns=hie_columns)

mv=pd.DataFrame(columns=df_columns)

time = list(np.arange(2000,2017))

color={'AS':0,'NA':1,'WE':2,'EE':3}

#This function adds rows to the dataframes.
def g(prev):
    cnt=0
    for t in time:
        for k in prev.keys():
            for country in prev[k]:
                row=[]
                row.append(t)
                row.append(k)
                row.append(country)
                row.append(color[k])
                for column in parallel_columns:
                    df_country = df_countries.get_group(country)
                    m = df_country[column].mean()
                    x=df_country.replace(to_replace=(np.nan),value=m)
                    v=float(x[x['Year']==(t)][column])
                    row.append(v)
    #                 print(x['Total fertility rate'])
    #                 print(x['Year'==t])
    #                 print(v)
    #                 y=x[x['Year']==t][column]
    #                 print(y)
    #                 break
    #                 s=s+v
    #             cnt=cnt+1
    #             print(cnt)
    #             s=s/len(prev[k])
    #             print(s)
#                 print(row)
                mv.loc[cnt]=row
                cnt=cnt+1

g(prev)

mv_time=mv.groupby('Time')

mv_time_2010 = mv_time.get_group(2010)

fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = list(mv_time_2010['Color']),
                   colorscale = 'thermal',
                   showscale = True),
        dimensions = list([
            dict(range=[1.0,100.0],
                 label = "male(%)", values = mv_time_2010['Total population, male (%)']),
            dict(range=[1.0,100.0],
                 label = 'female(%)', values = mv_time_2010['Total population, female (%)']),
            dict(tickvals = [0,1,2,3],
                 ticktext = ['AS','NA','WE','EE'],
                 constraintrange = [1,1.5],
                 label = 'Region', values = mv_time_2010['Color']),
            dict(range=[1.0,100.0],
                 label = 'Life expectancy at birth, women', values = mv_time_2010['Life expectancy at birth, women']),
            dict(range=[1.0,100.0],
                 label = 'Life expectancy at birth, men', values = mv_time_2010['Life expectancy at birth, men']),
            dict(range=[1.0,3.0],
                 label = 'Fertility', values = mv_time_2010['Total fertility rate'])
            ])
    )
)
fig.show()

mv_time_2004 = mv_time.get_group(2004)

fig_2004 = go.Figure(data=
    go.Parcoords(
        line = dict(color = list(mv_time_2004['Color']),
                   colorscale = 'thermal',
                   showscale = True),
        dimensions = list([
            dict(range=[1.0,100.0],
                 label = "male(%)", values = mv_time_2004['Total population, male (%)']),
            dict(range=[1.0,100.0],
                 label = 'female(%)', values = mv_time_2004['Total population, female (%)']),
            dict(tickvals = [0,1,2,3],
                 ticktext = ['AS','NA','WE','EE'],
                 constraintrange = [1,1.5],
                 label = 'Region', values = mv_time_2004['Color']),
            dict(range=[1.0,100.0],
                 label = 'Life expectancy at birth, women', values = mv_time_2004['Life expectancy at birth, women']),
            dict(range=[1.0,100.0],
                 label = 'Life expectancy at birth, men', values = mv_time_2004['Life expectancy at birth, men']),
            dict(range=[1.0,3.0],
                 label = 'Fertility', values = mv_time_2004['Total fertility rate'])
            ])
    )
)
fig_2004.show()

mv_time_2016 = mv_time.get_group(2016)

fig_2016 = go.Figure(data=
    go.Parcoords(
        line = dict(color = list(mv_time_2016['Color']),
                   colorscale = 'thermal',
                   showscale = True),
        dimensions = list([
            dict(range=[1.0,100.0],
                 label = "male(%)", values = mv_time_2016['Total population, male (%)']),
            dict(range=[1.0,100.0],
                 label = 'female(%)', values = mv_time_2016['Total population, female (%)']),
            dict(tickvals = [0,1,2,3],
                 ticktext = ['AS','NA','WE','EE'],
                 constraintrange = [1,1.5],
                 label = 'Region', values = mv_time_2016['Color']),
            dict(range=[1.0,100.0],
                 label = 'Life expectancy at birth, women', values = mv_time_2016['Life expectancy at birth, women']),
            dict(range=[1.0,100.0],
                 label = 'Life expectancy at birth, men', values = mv_time_2016['Life expectancy at birth, men']),
            dict(range=[1.0,3.0],
                 label = 'Fertility', values = mv_time_2016['Total fertility rate'])
            ])
    )
)
fig_2016.show()

labels={'Total population, male (%)' : 'male(%)', 'Total population, female (%)' : 'female(%)', 'Life expectancy at birth, women':'women_birth_rate', 'Life expectancy at birth, men': 'men_birth_rate','Total fertility rate':'fertility'}

fig_1 = px.scatter_matrix(mv_time_2010,
    dimensions=['Total population, male (%)','Total population, female (%)','Life expectancy at birth, women','Life expectancy at birth, men', 'Total fertility rate'],
    color="Region",labels=labels,width=800,height=800)
fig_1.update_traces(diagonal_visible=False)
fig_1.show()

fig = px.sunburst(hie, path=['Time', 'Region', 'Country'], values='Total females',color='Total fertility rate',
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(hie['Total fertility rate'], weights=hie['Total females']))
fig.show()


tfig = px.treemap(hie, path=['Time', 'Region', 'Country'], values='Total females',color='Total fertility rate',
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(hie['Total fertility rate'], weights=hie['Total females']))
tfig.show()
