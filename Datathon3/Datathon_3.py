import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn import preprocessing

df_data=pd.read_csv('archive/covid_19_data.csv')

# df_data.head()

# df_data.tail()


countries=list(set(df_data['Country/Region'].tolist()))


# len(countries)


# len(df_data)


df_dates=df_data.groupby(['ObservationDate'])

dates=list(set(df_data['ObservationDate'].tolist()))

# len(dates)

def f(st,column,add):
    country_time={}
    country_time_sqrt={}
    for country in countries:
        country_time[country]=[0]*len(dates)
        country_time_sqrt[country]=[0]*len(dates)

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

    df_for_matrix = pd.DataFrame(country_time)

    l=[]
    for column in df_for_matrix.columns:
        if(max(df_for_matrix[column])==0):
            l.append(column)

    #Removing columns which have only zeros
    df_for_matrix.drop(l,inplace=True,axis=1)
    labels=df_for_matrix.columns


    #Normalize the matrix
    x = df_for_matrix.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_for_matrix = pd.DataFrame(x_scaled)


    c=df_for_matrix.corr()

    for index,row in c.iterrows():
        for column in c.columns:
            if(row[column]<0.95):
                row[column]=0
            else:
                row[column]=1

    G=nx.Graph()

    adj_mat=c.to_numpy()
    adj_mat=np.matrix(adj_mat)
#     for i in range(0,len(adj_mat)):
#         for j in range((i+1),len(adj_mat[i])):
#             if(adj_mat[i][j]!=0):
#                 G.add_edge(i,j,weight=adj_mat[i][j])



    G=nx.from_numpy_matrix(adj_mat)
    mapping=dict(zip(G,list(labels)))
    G = nx.relabel_nodes(G, mapping)
    s="cumu_difference_0.95_sqrt/Confirmed/test_"+str(st)+".gexf"
    nx.write_gexf(G, s)

for i in range(0,24,1):
    f(i*10,'Confirmed',10)
