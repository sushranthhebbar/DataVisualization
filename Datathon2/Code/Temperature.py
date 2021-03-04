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

with zipfile.ZipFile("../datathon2_data.zip") as z:
   with z.open("OneDrive_1_12-09-2020/PotentialTemperature_3D/135_30_Oct_2005.txt") as f:
    for i,line in enumerate(f):
        if(i<9):
            continue
        else:
            df=pd.read_csv(f)


lon=df['LON'].unique().tolist()
lat=df['LAT'].unique().tolist()
height=df['DEP'].unique().tolist()
bad_flag=df['TEMP'][0]
df=df.replace([bad_flag],50000)
m=min(df['TEMP'])
df=df.replace([50000],m)
df.head()
df_z=df.groupby('DEP')
mean_z_list=[]
for z in range(5,105,10):
    curr_df=df_z.get_group(z)
    curr_mean=curr_df['TEMP'].mean()
    mean_z_list.append(curr_mean)

dep=[]
for z in range(5,105,10):
    dep.append(z)

fig,ax=plt.subplots()

ax.set_title('Temperature vs Depth ',pad=20)
ax.set_xlabel('Temperature in C',labelpad=10)
ax.xaxis.set_label_position('top')
ax.set_ylabel('Depth in (m)')
ax.scatter(mean_z_list,dep)
ax.xaxis.tick_top()
ax.invert_yaxis()

# ax.set_xticklabels(mean_z_list)
# ax.set_yticklabels(dep)
# start, end = ax.get_xlim()


# ax.xaxis.set_ticks(np.arange(22, 25, 0.4))

# start, end = ax.get_ylim()
# print(start,end)
# ax.yaxis.set_ticks(np.arange(5, 225, 30))

plt.grid()
plt.show()

def get_the_slice(x,y,z, surfacecolor):
    return go.Surface(x=x,y=y,z=z,surfacecolor=surfacecolor,coloraxis='coloraxis')

def get_lims_colors(surfacecolor):# color limits for a slice
    return np.min(surfacecolor), np.max(surfacecolor)

def colorax(vmin, vmax):
    return dict(cmin=vmin,
                cmax=vmax)
x=np.asarray(lon)
y=np.asarray(lat)

x,y=np.meshgrid(x,y)

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

frames=[]
for k in tqdm(range(5,105,10)):
    z=-k*np.ones((y.shape[0],x.shape[1]))
    surfcolor=df_z.get_group(k)['TEMP'].tolist()
    surfcolor=np.asarray(surfcolor)
    surfcolor=np.reshape(surfcolor,(z.shape))
    slice_z=get_the_slice(x,y,z,surfcolor)
    s=k/5

    frames.append(go.Frame(data=slice_z,name=str((s-1)/2)))

fig=go.Figure(frames=frames)

z_5=-5*np.ones((y.shape[0],x.shape[1]))
surfcolor_z_5=df_z.get_group(5)['TEMP'].tolist()
surfcolor_z_5=np.asarray(surfcolor_z_5)
surfcolor_z_5=np.reshape(surfcolor_z_5,(z_5.shape))
slice_z_5=get_the_slice(x,y,z_5,surfcolor_z_5)

sminz, smaxz = get_lims_colors(surfcolor_z_5)

sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]

fig.add_trace(slice_z_5)
fig.update_layout(
         title='Slices across depth for temperature (in Celsius)',
         width=600,
         height=600,
         scene=dict(
                    zaxis=dict(range=[-105, 0], autorange=False),
                    aspectratio=dict(x=1, y=1, z=1),
                    ),
         updatemenus = [
            {
                "buttons": [
                    {
                        "args": [None, frame_args(50)],
                        "label": "&#9654;", # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;", # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
         ],
         sliders=sliders,
         coloraxis=dict(colorscale='thermal',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(sminz, smaxz))
)

fig.show()

offline.plot(fig, auto_open=True, image_width=2000, image_height=1000,
              filename='Media/Interactive/Temperature/temperature_z.html', validate=True)

index_names = df[(df['LAT']>(6.12495)) | (df['LON']<51.25) | (df['LON']>93.25) | (df['DEP']>95)].index

df.drop(index_names,inplace=True)
df_x=df.groupby('LON')

mean_x_list=[]
for i in range(42,127):
    curr_df = df_x.get_group(lon[i])
    m=curr_df['TEMP'].mean()
    mean_x_list.append(m)

fig,ax=plt.subplots()

ax.set_title(' Mean of temperature versus longitude ',pad=20)
ax.set_xlabel('Longitude',labelpad=10)
# ax.xaxis.set_label_position('top')
ax.set_ylabel('Temperature in C')
ax.scatter(lon[42:127],mean_x_list)
# ax.xaxis.tick_top()
# ax.invert_yaxis()

# ax.set_xticklabels(mean_z_list)
# ax.set_yticklabels(dep)
# start, end = ax.get_xlim()


# ax.xaxis.set_ticks(np.arange(22, 25, 0.4))

# start, end = ax.get_ylim()
# print(start,end)
# ax.yaxis.set_ticks(np.arange(5, 225, 30))

plt.grid()
plt.show()

y=lat[:119]
y=np.asarray(y)
z=np.linspace(-95,-5,10)
y,z = np.meshgrid(y,z)
x_start=51.25*np.ones((z.shape[0],z.shape[1]))
frames=[]
for k in tqdm(range(42,127)):
    x=lon[k]*np.ones((z.shape[0],z.shape[1]))
#     z=-k*np.ones((y.shape[0],x.shape[1]))
    surfcolor=df_x.get_group(lon[k])['TEMP'].tolist()
    surfcolor=np.asarray(surfcolor)
    surfcolor=np.reshape(surfcolor,(z.shape))
    slice_x=get_the_slice(x,y,z,surfcolor)
    n=k-41
    frames.append(go.Frame(data=slice_x,name=str(n)))

surfcolor_start=df_x.get_group(51.25)['TEMP'].tolist()
surfcolor_start=np.asarray(surfcolor_start)
surfcolor_start=np.reshape(surfcolor_start,(z.shape))
slice_x=get_the_slice(x_start,y,z,surfcolor_start)

sminz, smaxz = get_lims_colors(surfcolor_start)
fig=go.Figure(frames=frames)

sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]

fig.add_trace(slice_x)
fig.update_layout(
         title='Slices across longitude for temperature (in Celsius)',
         width=600,
         height=600,
         scene=dict(
                    zaxis=dict(range=[-105, 0], autorange=False),
                    xaxis=dict(range=[50,100],autorange=False),
                    aspectratio=dict(x=1, y=1, z=1),
                    ),
         updatemenus = [
            {
                "buttons": [
                    {
                        "args": [None, frame_args(10)],
                        "label": "&#9654;", # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;", # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
         ],
         sliders=sliders,
         coloraxis=dict(colorscale='thermal',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(sminz, smaxz))
)

fig.show()

offline.plot(fig, auto_open=True, image = 'png', image_filename="" ,image_width=2000, image_height=1000,
 filename='Media/Interactive/Temperature/temperature_x.html', validate=True)

df_y=df.groupby('LAT')
mean_y_list=[]
for i in range(0,118):
    curr_df = df_y.get_group(lat[i])
    m=curr_df['TEMP'].mean()
    mean_y_list.append(m)


fig,ax=plt.subplots()

ax.set_title('Mean of temperature vs latitude ',pad=20)
ax.set_xlabel('Temperature in C',labelpad=10)
# ax.xaxis.set_label_position('top')
ax.set_ylabel('Latitude')
ax.scatter(mean_y_list,lat[:118])
# ax.xaxis.tick_top()
# ax.invert_yaxis()

# ax.set_xticklabels(mean_z_list)
# ax.set_yticklabels(dep)
# start, end = ax.get_xlim()


# ax.xaxis.set_ticks(np.arange(22, 25, 0.4))

# start, end = ax.get_ylim()
# print(start,end)
# ax.yaxis.set_ticks(np.arange(5, 225, 30))

plt.grid()
plt.show()


x=np.asarray(lon[42:127])
z=np.linspace(-95,-5,10)
x,z=np.meshgrid(x,z)
frames=[]
for k in tqdm(range(118)):
    y=lat[k]*np.ones((z.shape[0],z.shape[1]))
#     z=-k*np.ones((y.shape[0],x.shape[1]))
    surfcolor=df_y.get_group(lat[k])['TEMP'].tolist()
    surfcolor=np.asarray(surfcolor)
    surfcolor=np.reshape(surfcolor,(z.shape))
    slice_y=get_the_slice(x,y,z,surfcolor)
    n=k
    frames.append(go.Frame(data=slice_y,name=str(n)))

y_start=(-29.7509)*np.ones((z.shape[0],z.shape[1]))

surfcolor_start=df_y.get_group(-29.7509)['TEMP'].tolist()
surfcolor_start=np.asarray(surfcolor_start)
surfcolor_start=np.reshape(surfcolor_start,(z.shape))

slice_y=get_the_slice(x,y_start,z,surfcolor_start)

sminz, smaxz = get_lims_colors(surfcolor_start)
fig=go.Figure(frames=frames)

sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]


fig.add_trace(slice_y)
fig.update_layout(
         title='Slices across latitude for temperature (in Celsius)',
         width=600,
         height=600,
         scene=dict(
                    zaxis=dict(range=[-105, 0], autorange=False),
                    xaxis=dict(range=[50,100],autorange=False),
                    yaxis=dict(range=[-30,10],autorange=False),
                    aspectratio=dict(x=1, y=1, z=1),
                    ),
         updatemenus = [
            {
                "buttons": [
                    {
                        "args": [None, frame_args(0)],
                        "label": "&#9654;", # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;", # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
         ],
         sliders=sliders,
         coloraxis=dict(colorscale='thermal',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(16, 28))
)

fig.show()

offline.plot(fig, auto_open=True, image = 'png', image_filename="" ,image_width=2000, image_height=1000,
              filename='Media/Interactive/Temperature/temperature_y.html', validate=True)
