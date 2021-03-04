import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn import preprocessing
from scipy.spatial.distance import squareform,pdist

df_data=pd.read_csv('../Data_Visulization_3/archive/covid_19_data.csv')

# df_data.head()

countries=list(set(df_data['Country/Region'].tolist()))

# len(countries)

df_dates=df_data.groupby(['ObservationDate'])

dates=list(set(df_data['ObservationDate'].tolist()))

def f(st,column,add):

    prev_dict= { country : 0 for country in countries}

    country_time={}
    country_time_sqrt={}
    for country in countries:
        country_time[country]=[0]*add
        country_time_sqrt[country]=[0]*add

    end=len(dates)

    for i in tqdm(range(st,min(st+add,end),1)):
        df_date = df_dates.get_group(dates[i])
        curr_dict= { country : 0 for country in countries}
        for index,row in df_date.iterrows():
            country=row['Country/Region']
            curr_dict[country]+=row[column]
        for country in countries:
            country_time[country][i]= curr_dict[country]
            if(i==0):
                country_time_sqrt[country][i]=np.sqrt(country_time[country][i])
            else:
                country_time_sqrt[country][i]=np.sqrt(country_time[country][i])-np.sqrt(country_time_sqrt[country][i-1])
                if(country_time_sqrt[country][i]<0):
                    country_time_sqrt[country][i]=0
#         prev_dict=curr_dict
    df_for_matrix = pd.DataFrame(country_time_sqrt)

    l=[]
    for column in df_for_matrix.columns:
        if(max(df_for_matrix[column])==0):
            l.append(column)

    df_for_matrix.drop(l,inplace=True,axis=1)
    labels=df_for_matrix.columns

    x = df_for_matrix.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_for_matrix = pd.DataFrame(x_scaled)
    df_for_matrix = df_for_matrix.transpose()



    pairwise = pd.DataFrame(
    squareform(pdist( df_for_matrix)),
    columns =  df_for_matrix.index,
    index =  df_for_matrix.index
    )
    return pairwise,labels



z=f(0,'Confirmed',200)

x=z[0]

y=list(z[1])


mapping=dict(zip(list(range(191)),y))


np.savetxt('in.txt', x.values, fmt='%f', delimiter="\t")
