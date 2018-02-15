# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:45:00 2018
makes map of both eMOLT and FSRS sites >1 year
@author: Xiaoxu
Modifications by JiM and Xiaoxu
"""
import pandas as pd
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
def dm2dd(lat,lon):
    """
    convert lat, lon from decimal degrees,minutes to decimal degrees
    """
    (a,b)=divmod(float(lat),100.)   
    aa=int(a)
    bb=float(b)
    lat_value=aa+bb/60.

    if float(lon)<0:
        (c,d)=divmod(abs(float(lon)),100.)
        cc=int(c)
        dd=float(d)
        lon_value=cc+(dd/60.)
        lon_value=-lon_value
    else:
        (c,d)=divmod(float(lon),100.)
        cc=int(c)
        dd=float(d)
        lon_value=cc+(dd/60.)
    return lat_value, -lon_value
#### HARDCODES  #####
case=''#'_MAB'
projec='merc'
gbox=[-74,-58,39,48]
#####################
df=pd.read_csv('sqldump_sites'+case+'.dat',index_col=2,delim_whitespace=True)# eMOLT sites > 1year from JiM
dfh=pd.read_csv('fsrs_sites.csv') # getfsrs.py output where sites are > 1year and with 1km
fig = plt.figure()
a=fig.add_subplot(1,1,1)
# emolt site
Lon,Lat=[],[]
for k in range(len(df)):
    if int(df['MAXD'][k][-4:])-int(df['MIND'][k][-4:])>0:
      la=df['LAT_DDMM'][k]
      lo=df['LON_DDMM'][k]
      [la,lo]=dm2dd(la,lo)
      Lon.append(lo)
      Lat.append(la)
my_map = Basemap(projection=projec,
    resolution = 'h', area_thresh = 0.3,
    llcrnrlon=gbox[0], llcrnrlat=gbox[2],
    urcrnrlon=gbox[1], urcrnrlat=gbox[3]) 
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'grey')
my_map.drawmapboundary() 
x,y=my_map(Lon,Lat)
my_map.plot(x, y, 'bo', markersize=4)
x,y=my_map(dfh['Longitude'].values,dfh['Latitude'].values)
my_map.plot(x, y, 'go', markersize=4)
label=["eMOLT","FSRS"]
a.legend(label,loc="lower right")
a.set_title('eMOLT sites (>1 year) and FSRS sites (>1 year)',fontsize=15)
my_map.drawparallels(np.arange(30,80,3),labels=[1,0,0,0])
my_map.drawmeridians(np.arange(-180,180,3),labels=[1,1,0,1])
plt.savefig("plot_eMOLT_FSRS_more_than_1_year.png")
plt.show()
