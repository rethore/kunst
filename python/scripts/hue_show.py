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
import os
from random import shuffle
from datetime import datetime
from flask import g
import click
from pymongo import MongoClient
mongo = MongoClient('mongo', 27017)
db_state = mongo.state_db
states = db_state.states

c = Converter()
mapxy = lambda colormap: lambda val: c.rgbToCIE1931(*plt.get_cmap(colormap)(val)[:3])


c02auth = os.environ['C02_AUTH'] if 'C02_AUTH' in os.environ else None

def get_effect_type():
    return states.find_one({'name':'effect_type'})['state']

def set_effect_type(effect_type):
    return states.find_one_and_update({'name':'effect_type'}, {"$set": {'state':effect_type}}, upsert=True)

def get_carbon_state():
    return states.find_one({'name':'carbon'})

def set_carbon_state(data):
    return states.find_one_and_update({'name':'carbon'}, {"$set": data}, upsert=True)

def set_state(name, key, value):
    states.find_one_and_update({'name':name}, {"$set": {key:value}}, upsert=True)

def set_xy(name, xy):
    set_state(name, 'xy', xy)

def get_state(name):
    return states.find_one({'name':name})

def get_xy(name):
    return get_state(name)['xy']

def clean_state():
    for i in range(19):
        name = 'P%d'%(i+1)
        states.delete_many({'name': name})

def is_in_state(name):
    return states.find({'name':name}).count() > 0

def check_state(b, DT=0.1):
    x = list(range(19))
    shuffle(x)
    for i in x:
        name = 'P%d'%(i+1)
        l = b.lights_by_name[name]
        if not is_in_state(name):
            set_xy(name, c.rgbToCIE1931(1., 1., 1.))
            l.brightness = 254
        l.xy =get_xy(name)
        sleep(DT)

def rgbl(l, R, G, B, transitiontime=0.1, brightness=254, DT=0.01):
    l.on = True
    l.brightness = brightness
    l.transitiontime = transitiontime
    l.xy = c.rgbToCIE1931(R, G, B)
    set_xy(l.name, c.rgbToCIE1931(1., 1., 1.))
    sleep(DT)


def all_rgb(b, R, G, B, transitiontime=0.1, brightness=254, DT=0.01):
    #for i in range(4):
    for j in range(19):
        name = 'P%d'%(j+1)
        rgbl(b.lights_by_name[name], R, G, B, transitiontime, brightness, DT)
        #sleep(0.5)

def normal(b, DT=0.01):
    all_rgb(b, 1.0, 1.0, 1.0, DT)

def init_bridge(ip=None, username=None):
    if ip == None:
        bridges = req.get('https://www.meethue.com/api/nupnp').json()
        selected = [x for x in bridges if '273a83' in x['id']][0]
        ip = selected['internalipaddress']
        print(selected)
    b = Bridge(ip, username) # Enter bridge IP here.

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
                set_xy(name, cmxy(df[P2H[name]].iloc[i]/df['House 2'].max()))
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

def get_carbon_color(c02auth=c02auth):
    g.carbon_time = datetime.now()
    response = req.get('https://api.co2signal.com/v1/latest?countryCode=DK', headers={'auth-token': c02auth})
    resp = response.json()
    data = resp['data']
    data['time'] = datetime.now()
    set_carbon_state(data)

    carbon = data['carbonIntensity']
    carbon_scaling = 650
    return carbon, min(carbon/carbon_scaling, 1.0)


def carbon_color(c02auth=c02auth, b=None, ip=None, username=None):
    if b == None:
        b = init_bridge(ip, username)
    carbon, carbon_scaled = get_carbon_color(c02auth)
    R, G, B, dumb = plt.get_cmap('hot')(1.0-carbon_scaled)
    all_rgb(b, R, G, B, transitiontime=0.1, brightness=254, DT=0.5)
    print('carbon', carbon, carbon_scaled)
    return carbon, carbon_scaled

def wave_effect(hn):
    """Make a wave effect starting from a house number
    Parameters
    ----------
    hn: int
        house number
    """
    # propagation speed
    speed = 20 # m/s
    distance = 7 #m between each lamp
    time = 7 / (speed * 1E3 / (60*60))
    for n in range(9):
        try:
            name = "P%d"%((hn+2*n+1)%(19))
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
