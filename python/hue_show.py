from time import sleep
from phue import Bridge
import random
from numpy import zeros, ones
import numpy as np
import matplotlib.pyplot as plt
from tqdm import *
import requests as req
import pandas as pd
from rgb_cie import Converter


import click

c = Converter()
mapxy = lambda colormap: lambda val: c.rgbToCIE1931(*plt.get_cmap(colormap)(val)[:3])
    
def rgbl(l, R, G, B, transitiontime=0.1, brightness=254, DT=0.01):
    l.on = True
    l.brightness = brightness
    l.transitiontime = transitiontime
    l.xy = c.rgbToCIE1931(R, G, B)
    sleep(DT)    

def all_rgb(b, R, G, B, transitiontime=0.1, brightness=254, DT=0.01):
    #for i in range(4):
    for j in range(19):
        name = 'P%d'%(j+1)
        rgbl(b.lights_by_name[name], R, G, B, transitiontime, brightness, DT)
        #sleep(0.5)
    
def normal(b):
    all_rgb(b, 1.0, 1.0, 1.0)    

def init_bridge(ip=None):
    bridges = req.get('https://www.meethue.com/api/nupnp').json()
    if ip == None:
        selected = [x for x in bridges if '273a83' in x['id']][0]
        ip = selected['internalipaddress']
        print(selected)
    b = Bridge(ip) # Enter bridge IP here.

    #If running for the first time, press button on bridge and run with b.connect() uncommented
    b.connect()

    try:
        lights = b.lights
    except:
        lights = b.lights_by_name

    return b

        
    
def show(data, ip=None, cmap='hot', dt=0.01, b=None):    
    print(data, ip, cmap)
    if b == None:
        b = init_bridge(ip)

    df = pd.read_csv(data)

    # Associate a house to each lamps
    hs = [k for k in df.keys() if 'House' in k]
    j = 0
    P2H = {}
    for i in range(19):
        n = 'P%d'%(i+1)
        l =  b.lights_by_name[n]
        house_name = hs[j]
        j += 1
        if j >= len(hs):
            j = 0
        P2H[n] = house_name 
        
    normal(b)

    # Run the show
    cmxy = mapxy(cmap)
    for i in tqdm(range(30,70)):
        for j in range(19):
            try:
                name = 'P%d'%(j+1)
                l = b.lights_by_name[name]
                l.brightness = 254
                l.transitiontime = 10.0
                l.xy = cmxy(df[P2H[name]].iloc[i]/df['House 2'].max())
                #if not done[P2H[name]][i]:
                #    svalin_streams[P2H[name]].write(dict(x=i, y=df[P2H[name]].iloc[i]))
                #    #print(P2H[name], dict(x=df.index[i], y=df[P2H[name]].iloc[i]))
                #    done[P2H[name]][i] = True
                sleep(dt)
            except Exception as e:
                print(e)
    normal(b)
    
    
def run_game(speed, n_tours=1, ip=None, b=None):
    if b == None:
        b = init_bridge(ip)

    #speed = 10 #km/h
    distance = 7 #m between each lamp
    time = 7 / (speed * 1E3 / (60*60))
    print("To run %3.2f km/h, the time between each lamp has to be %3.2f sec"%(speed, time))
    for i in range(n_tours):
        for n in range(19):
            try:
                name = "P%d"%(n+1)
                l = b.lights_by_name[name]
                rgbl(l, 1.0,0.0,0.0, brightness=254)
                sleep(time)
                rgbl(l, 1.,1.,1., brightness=254)
                sleep(0.1)
            except Exception as e:
                print(e)



@click.command()
@click.option('--data', help='CSV file of the house solar production')
@click.option('--ip', default=None, help='IP address of the bridge')
@click.option('--cmap', default='jet', help='Colormap: [Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r]')
@click.option('--dt', default=0.01, help='Time step inbetween each color change')
def command(data, ip, cmap, dt):
    show(data, ip, cmap, dt)
    
            
if __name__ == '__main__':
    command() 
