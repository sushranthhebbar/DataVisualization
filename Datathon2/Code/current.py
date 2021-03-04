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

with zipfile.ZipFile("../datathon2_currents.zip") as z:
    with z.open("Currents/meridional-current_3D/073_24_Dec_2004.txt") as f:
        for i,line in enumerate(f):
            if(i<9):
                continue
            else:
                meri=pd.read_csv(f)
    with z.open("Currents/zonal-current_3D/073_24_Dec_2004.txt") as f:
        for i,line in enumerate(f):
            if(i<9):
                continue
            else:
                zono=pd.read_csv(f)


lon=meri['LON'].unique().tolist()
lat=meri['LAT'].unique().tolist()
height=meri['DEP'].unique().tolist()
bad_flag=meri['V'][0]
meri=meri.replace([bad_flag],0)
bad_flag=zono['U'][0]
zono=zono.replace([bad_flag],0)
zono_z=zono.groupby('DEP')
meri_z=meri.groupby('DEP')



mean_z_list=[]
for z in range(5,105,10):
    curr_u_df=zono_z.get_group(z)
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_z.get_group(z)
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    s=np.sqrt(s)

    curr_mean=s.mean()
    mean_z_list.append(curr_mean)

dep=[]
for z in range(5,105,10):
    dep.append(z)

fig,ax=plt.subplots()

ax.set_title('Speed of currents vs Depth ',pad=20)
ax.set_xlabel('Speed in m/s',labelpad=10)
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

    curr_u_df=zono_z.get_group(k)
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_z.get_group(k)
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    surfcolor=np.sqrt(s)



#     surfcolor=df_z.get_group(k)['TEMP'].tolist()
#     surfcolor=np.asarray(surfcolor)
    surfcolor=np.reshape(surfcolor,(z.shape))
    slice_z=get_the_slice(x,y,z,surfcolor)
    s=k/5

    frames.append(go.Frame(data=slice_z,name=str((s-1)/2)))

fig=go.Figure(frames=frames)

z_5=-5*np.ones((y.shape[0],x.shape[1]))

curr_u_df=zono_z.get_group(5)
curr_u=np.asarray(curr_u_df['U'].tolist())

curr_v_df=meri_z.get_group(5)
curr_v=np.asarray(curr_v_df['V'].tolist())

s=(curr_u*curr_u)+(curr_v*curr_v)
surfcolor_z_5=np.sqrt(s)



#     surfcolor=df_z.get_group(k)['TEMP'].tolist()
#     surfcolor=np.asarray(surfcolor)
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
         title='Slices across depth for speed of currents (in m/s)',
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
         coloraxis=dict(colorscale='speed',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(sminz, smaxz))
)

fig.show()

offline.plot(fig, auto_open=True, image_width=2000, image_height=1000,
              filename='Media/Interactive/Currents/currents_z.html', validate=True)

index_names = meri[(meri['LAT']>(6.12495)) | (meri['LON']<51.25) | (meri['LON']>93.25) | (meri['DEP']>95)].index
meri.drop(index_names,inplace=True)

index_names = zono[(zono['LAT']>(6.12495)) | (zono['LON']<51.25) | (zono['LON']>93.25) | (zono['DEP']>95)].index
zono.drop(index_names,inplace=True)


zono_x=zono.groupby('LON')
meri_x=meri.groupby('LON')

mean_x_list=[]
for i in range(43,127):
    print(lon[i])
    curr_u_df=zono_x.get_group(lon[i])
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_x.get_group(lon[i])
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    s=np.sqrt(s)

    curr_mean=s.mean()
    mean_x_list.append(curr_mean)



fig,ax=plt.subplots()

ax.set_title('Mean of current speed vs longitude ',pad=20)
ax.set_xlabel('Longitude',labelpad=10)
# ax.xaxis.set_label_position('top')
ax.set_ylabel('Speed in m/s')
ax.scatter(lon[43:127],mean_x_list)
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
x_start=51.5*np.ones((z.shape[0],z.shape[1]))

frames=[]
for k in tqdm(range(43,127)):
    x=lon[k]*np.ones((z.shape[0],z.shape[1]))
#     z=-k*np.ones((y.shape[0],x.shape[1]))
    curr_u_df=zono_x.get_group(lon[k])
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_x.get_group(lon[k])
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    surfcolor=np.sqrt(s)





#     surfcolor=df_x.get_group(lon[k])['TEMP'].tolist()
#     surfcolor=np.asarray(surfcolor)
    surfcolor=np.reshape(surfcolor,(z.shape))
    slice_x=get_the_slice(x,y,z,surfcolor)
    n=k-41
    frames.append(go.Frame(data=slice_x,name=str(n)))

curr_u_df=zono_x.get_group(51.5)
curr_u=np.asarray(curr_u_df['U'].tolist())

curr_v_df=meri_x.get_group(51.5)
curr_v=np.asarray(curr_v_df['V'].tolist())

s=(curr_u*curr_u)+(curr_v*curr_v)
surfcolor_start=np.sqrt(s)



#     surfcolor=df_z.get_group(k)['TEMP'].tolist()
#     surfcolor=np.asarray(surfcolor)
surfcolor_start=np.reshape(surfcolor_start,(z.shape))




# surfcolor_start=df_x.get_group(51.25)['TEMP'].tolist()
# surfcolor_start=np.asarray(surfcolor_start)
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
         title='Slices across longitude for speed of currents (in m/s)',
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
         coloraxis=dict(colorscale='speed',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(sminz, smaxz))
)

fig.show()

offline.plot(fig, auto_open=True, image_width=2000, image_height=1000,
              filename='Media/Interactive/Currents/current_x.html', validate=True)

zono_y=zono.groupby('LAT')
meri_y=meri.groupby('LAT')
mean_y_list=[]
for i in range(0,118):

    curr_u_df=zono_y.get_group(lat[i])
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_y.get_group(lat[i])
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    s=np.sqrt(s)

    curr_mean=s.mean()
    mean_y_list.append(curr_mean)



fig,ax=plt.subplots()

ax.set_title('Mean of current speed vs latitude ',pad=20)
ax.set_xlabel('Speed in m/s',labelpad=10)
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

x=np.asarray(lon[43:127])
z=np.linspace(-95,-5,10)
x,z=np.meshgrid(x,z)

frames=[]
for k in tqdm(range(118)):
    y=lat[k]*np.ones((z.shape[0],z.shape[1]))
#     z=-k*np.ones((y.shape[0],x.shape[1]))

    curr_u_df=zono_y.get_group(lat[k])
    curr_u=np.asarray(curr_u_df['U'].tolist())

    curr_v_df=meri_y.get_group(lat[k])
    curr_v=np.asarray(curr_v_df['V'].tolist())

    s=(curr_u*curr_u)+(curr_v*curr_v)
    surfcolor=np.sqrt(s)





#     surfcolor=df_y.get_group(lat[k])['TEMP'].tolist()
#     surfcolor=np.asarray(surfcolor)
    surfcolor=np.reshape(surfcolor,(z.shape))
    slice_y=get_the_slice(x,y,z,surfcolor)
    n=k
    frames.append(go.Frame(data=slice_y,name=str(n)))

y_start=(-30.0005)*np.ones((z.shape[0],z.shape[1]))

curr_u_df=zono_y.get_group(-30.0005)
curr_u=np.asarray(curr_u_df['U'].tolist())

curr_v_df=meri_y.get_group(-30.0005)
curr_v=np.asarray(curr_v_df['V'].tolist())

s=(curr_u*curr_u)+(curr_v*curr_v)
surfcolor_start=np.sqrt(s)




# surfcolor_start=df_y.get_group(-30.0005)['TEMP'].tolist()
# surfcolor_start=np.asarray(surfcolor_start)
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
         title='Slices across latitude for speed of current (in m/s)',
         width=600,
         height=600,
         scene=dict(
                    zaxis=dict(range=[-105, 0], autorange=False),
                    xaxis=dict(range=[50,100],autorange=False),
                    yaxis=dict(range=[-32,10],autorange=False),
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
         coloraxis=dict(colorscale='speed',
                        colorbar_thickness=25,
                        colorbar_len=0.75,
                        **colorax(sminz, 2))
)

fig.show()


offline.plot(fig, auto_open=True, image_width=2000, image_height=1000,
              filename='Media/Interactive/Currents/current_y.html', validate=True)        
