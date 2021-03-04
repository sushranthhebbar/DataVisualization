#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import zipfile
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from tqdm import tqdm
import plotly
import plotly.graph_objects as go

import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
import os

zono_base='Currents/zonal-current_3D/'

meri_base='Currents/meridional-current_3D/'

def get_the_slice(x,y,z, surfacecolor):
    return go.Surface(x=x,y=y,z=z,surfacecolor=surfacecolor,coloraxis='coloraxis')

def get_lims_colors(surfacecolor):# color limits for a slice
    return np.min(surfacecolor), np.max(surfacecolor)

def colorax(vmin, vmax):
    return dict(cmin=vmin,cmax=vmax)


coloraxis=dict(colorscale='speed',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(32, 38))

t=['069_04_Dec_2004.txt', '070_09_Dec_2004.txt', '071_14_Dec_2004.txt', '072_19_Dec_2004.txt', '073_24_Dec_2004.txt', '074_29_Dec_2004.txt', '075_03_Jan_2005.txt', '076_08_Jan_2005.txt', '077_13_Jan_2005.txt']


vmin=50000
vmax=-50000

data_slider=[]
for i in tqdm(range(len(t))):
#     print(p)
    p=t[i]
    meri_path=meri_base+p
    zono_path=zono_base+p
#     print(full_path)
    with zipfile.ZipFile("../datathon2_currents.zip") as z:
        with z.open(meri_path) as f:
            for i,line in enumerate(f):
                if(i<9):
                    continue
                else:
                    meri=pd.read_csv(f)
    with zipfile.ZipFile("../datathon2_currents.zip") as z:
        with z.open(zono_path) as f:
            for i,line in enumerate(f):
                if(i<9):
                    continue
                else:
                    zono=pd.read_csv(f)
#     print(df.head())

    lon=meri['LON'].unique().tolist()
    lat=meri['LAT'].unique().tolist()


    bad_flag=meri['V'][0]
    meri=meri.replace([bad_flag],0)
    bad_flag=zono['U'][0]
    zono=zono.replace([bad_flag],0)
    index_names = meri[(meri['LAT']>(6.12495)) | (meri['LON']<51.25) | (meri['LON']>93.25) | (meri['DEP']>95)].index
    meri.drop(index_names,inplace=True)
    index_names = zono[(zono['LAT']>(6.12495)) | (zono['LON']<51.25) | (zono['LON']>93.25) | (zono['DEP']>95)].index
    zono.drop(index_names,inplace=True)

    zono_z=zono.groupby('DEP')
    meri_z=meri.groupby('DEP')

    zono_x=zono.groupby('LON')
    meri_x=meri.groupby('LON')

    zono_y=zono.groupby('LAT')
    meri_y=meri.groupby('LAT')

    x=np.asarray(lon[43:127])
    y=np.asarray(lat[:119])

    x,y=np.meshgrid(x,y)

    z_45=-45*np.ones((y.shape[0],x.shape[1]))



    curr_u_df=zono_z.get_group(45)
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_z.get_group(45)
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    surfcolor_z=np.sqrt(s)

    surfcolor_z=np.reshape(surfcolor_z,(z_45.shape))
    slice_z=get_the_slice(x,y,z_45,surfcolor_z)


    y=np.asarray(lat[:119])
    z=np.linspace(-95,-5,10)

    y,z=np.meshgrid(y,z)

    x_75=75.5*np.ones((z.shape[0],z.shape[1]))

    curr_u_df=zono_x.get_group(75.5)
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_x.get_group(75.5)
    curr_v=np.asarray(curr_v_df['V'].tolist())


    s=(curr_u*curr_u)+(curr_v*curr_v)
    surfcolor_x=np.sqrt(s)


    surfcolor_x=np.reshape(surfcolor_x,(z.shape))
    slice_x = get_the_slice(x_75,y,z,surfcolor_x)


    x=np.asarray(lon[43:127])
    z=np.linspace(-95,-5,10)

    x,z=np.meshgrid(x,z)

    y_0=np.zeros((z.shape[0],z.shape[1]))


    curr_u_df=zono_y.get_group(0)
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_y.get_group(0)
    curr_v=np.asarray(curr_v_df['V'].tolist())


    s=(curr_u*curr_u)+(curr_v*curr_v)

    surfcolor_y=np.sqrt(s)


    surfcolor_y=np.reshape(surfcolor_y,(z.shape))
    slice_y=get_the_slice(x,y_0,z,surfcolor_y)



    sminz, smaxz = get_lims_colors(surfcolor_z)
    sminx, smaxx = get_lims_colors(surfcolor_x)
    sminy, smaxy = get_lims_colors(surfcolor_y)
    vmin=min(sminz,sminx,sminy,vmin)
    vmax=max(smaxz,smaxx,smaxy,vmax)


#     df=df.replace([bad_flag],0)
#     df_z=df.groupby('DEP')
#     surfcolor_z_5=df_z.get_group(5)['SALT'].tolist()
#     surfcolor_z_5=np.asarray(surfcolor_z_5)
#     surfcolor_z_5=np.reshape(surfcolor_z_5,(z_5.shape))
#     slice_z_5=get_the_slice(x,y,z_5,surfcolor_z_5)

#     data_slider_x.append(slice_x)
#     data_slider_y.append(slice_y)
#     data_slider_z.append(slice_z)
    data_slider.append(slice_x)
    data_slider.append(slice_y)
    data_slider.append(slice_z)
#     print(slice_z_5)
#     fig = dict(data=[slice_z_5], layout=layout)
#     plotly.offline.iplot(fig)
#     break


steps = []
print(len(data_slider))
i=0
while(i<len(data_slider)):
# for i in range(len(data_slider)):
    j=int((i/3))
    val=t[j]
    val=val[4:15]
    step = dict(method='restyle',
                args=['visible', [False] * len(data_slider)],
                label=val)

    step['args'][1][i] = True
    step['args'][1][i+1] = True
    step['args'][1][i+2] = True
    steps.append(step)
    i=i+3

sliders = [dict(active=0, pad={"t": 1}, steps=steps)]


layout = dict(
    title = 'Plot of current speed from Dec-2004 to Jan-2005',
    title_x=0.5,
    scene=dict(
                    zaxis=dict(range=[-95, 0], autorange=False),
                    xaxis=dict(range=[50,100],autorange=False),
                    yaxis=dict(range=[-32,10],autorange=False),
                    aspectratio=dict(x=1, y=1, z=1),
                ),
         coloraxis=dict(colorscale='speed',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(vmin, vmax)),
    sliders=sliders,
    width=600,
    height=600
)

fig = dict(data = data_slider,layout = layout)

plotly.offline.iplot(fig)

offline.plot(fig, auto_open=True ,image_width=2000, image_height=1000,
              filename='Media/Interactive/Currents/current_across_time.html', validate=True)
