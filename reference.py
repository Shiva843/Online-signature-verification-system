import pandas as pd
import math
import numpy as np
from scipy.ndimage import gaussian_filter1d
from sklearn.preprocessing import StandardScaler


#Normalization
def normalised_coordinates(x_cord,y_cord,time):
    #centre of mass
    xg=sum(x_cord)/(time[len(time)-1]-time[0])
    yg=sum(y_cord)/(time[len(time)-1]-time[0])
    # print ("centre of mass : ",xg,yg)

    x_new,y_new=[],[]
    #Normalized cordinates

    #new x cordinates
    for i in x_cord:
        x_new.append(i-xg)

    #new y cordinates
    for j in y_cord:
        y_new.append(j-yg)
    return x_new,y_new

#Smoothing - Gaussian filter
def gaussian_filter(x,y):
    x_filtered=gaussian_filter1d(x, 1)
    y_filtered=gaussian_filter1d(y, 1)
    return x_filtered,y_filtered

#speed
def speed(x,y,t):
    vx,vy,vxy=[],[],[]
    vx.append(x[0]/t[0])
    vy.append(y[0]/t[0])
    for i in range(1,len(x)):
        vx.append((x[i]-x[i-1])/(t[i]-t[i-1]))
        vy.append((y[i]-y[i-1])/(t[i]-t[i-1]))
    for i in range(0,len(vx)):
        vxy.append(math.sqrt(pow(vx[i],2) + pow(vy[i],2)))
    return vx,vy,vxy

def critical_points(y,t):
    v_star=[]
    first=0
    i,j=0,1
    temp=0
    if y[0]<=y[1]:
        temp=2
    else:
        temp=1
    #for decreasing fun :-- temp=1
    #for increasing fun :-- temp=2
    while(j<len(y)-1):
        if temp==2:
            if y[j]>y[j+1]:
                a=i
                b=j
                if first==0:
                    v_star.append((y[j]-y[i])/(t[j]-t[i]))
                    first=1
                while(a!=b):
                    v_star.append((y[j]-y[i])/(t[j]-t[i]))
                    a+=1
                i=j
                temp=1
        else:
            if y[j]<y[j+1]:
                a=i
                b=j
                if first==0:
                    v_star.append((y[j]-y[i])/(t[j]-t[i]))
                    first=1
                while(a!=b):
                    v_star.append((y[j]-y[i])/(t[j]-t[i]))
                    a+=1
                i=j
                temp=2
        j+=1
    a=i
    b=j
    while(a!=b):
        v_star.append((y[j]-y[i])/(t[j]-t[i]))
        a+=1
    return v_star

#Acceleration
def acceleration(vx,vy,t):
    ax,ay=[],[]
    ax.append(vx[0]/t[0])
    ay.append(vy[0]/t[0])
    for i in range(1,len(vx)):
        ax.append((vx[i]-vx[i-1])/(t[i]-t[i-1]))
        ay.append((vy[i]-vy[i-1])/(t[i]-t[i-1]))
    return ax,ay

#derivatives
def derivatives(x,y,p,t):
    for i in range(len(x)-1):
        if x[i]==x[i+1]:
            x[i]+=1
    dt,dx,dy=[],[],[]
    dt.append(p[0]/t[0])
    dx.append(p[0]/x[0])
    dy.append(p[0]/y[0])
    for i in range(1,len(t)):
        dt.append((p[i]-p[i-1])/(t[i]-t[i-1]))
        if x[i]==x[i-1]:
            x[i]+=1
        dx.append((p[i]-p[i-1])/(x[i]-x[i-1]))
        dy.append((p[i]-p[i-1])/(y[i]-y[i-1]))
    return dt,dx,dy


def load_file(file):
    df = pd.read_csv(file, skiprows=1, sep=" ",header=None, names=["x", "y", "time","button", "azimuth", "altitude", "pressure"])
    x_cord=df['x']
    y_cord=df['y']
    time=df['time']
    for i in range(len(time)-1):
        if time[i]==time[i+1]:
            time[i]+=1
    button=df['button']
    azimuth=df['azimuth']
    altitude=df['altitude']
    pen_pressure=df['pressure']

    return x_cord,y_cord,time,button,azimuth,altitude,pen_pressure

def features_normalization(feature):
    
    new_features=np.array(feature).T.tolist()
    # print(feature)
    normalized_features=StandardScaler().fit_transform(new_features)
    # normalized_features.shape()
    # print (np.array(normalized_features).T.tolist())
    return np.array(normalized_features).T.tolist()[0]

    
    

def reference_features_list(file):

    x_cord,y_cord,time,button,azimuth,altitude,pen_pressure=load_file(file)
    x_new,y_new=normalised_coordinates(x_cord,y_cord,time)
    x_filtered,y_filtered=gaussian_filter(x_new,y_new)
    # #features extraction

    vx,vy,vxy=speed(x_filtered,y_filtered,time)
    vy_star=critical_points(y_filtered,time)
    # print (vy_star)
    ax,ay=acceleration(vx,vy,time)
    dp_t, dp_x, dp_y=derivatives(x_filtered,y_filtered,pen_pressure,time)

    # make a new dataframe
    # reference_normalised_features=feature_normalisation(pen_pressure,altitude,azimuth,vx,vy,vxy,vy_star,ax,ay,dp_t,dp_x,dp_y)
    # print(normalised_features)
    # return normalised_features

    
    reference_list=[]
    reference_list.append(features_normalization([pen_pressure]))
    reference_list.append(features_normalization([altitude]))
    reference_list.append(features_normalization([azimuth]))
    reference_list.append(features_normalization([vx]))
    reference_list.append(features_normalization([vy]))
    reference_list.append(features_normalization([vxy]))
    reference_list.append(features_normalization([vy_star]))
    reference_list.append(features_normalization([ax]))
    reference_list.append(features_normalization([ay]))
    reference_list.append(features_normalization([dp_t]))
    reference_list.append(features_normalization([dp_x]))
    reference_list.append(features_normalization([dp_y]))
    return reference_list
