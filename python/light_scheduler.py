import time
import datetime
import schedule
from rest import download, on, off, sun
import random
import numpy as np

def job(t):
    print("I'm working...", t)

    today = datetime.date.today()
    print('today is {}/{}/{}'.format(today.day, today.month, today.year))

    download(str(today.day), str(today.month), str(today.year))
    return

cmaps = ["Accent", "Accent_r", "Blues", "Blues_r", "BrBG", "BrBG_r", "BuGn", "BuGn_r", "BuPu", "BuPu_r", "CMRmap", "CMRmap_r", "Dark2", "Dark2_r", "GnBu", "GnBu_r", "Greens", "Greens_r", "Greys", "Greys_r", "OrRd", "OrRd_r", "Oranges", "Oranges_r", "PRGn", "PRGn_r", "Paired", "Paired_r", "Pastel1", "Pastel1_r", "Pastel2", "Pastel2_r", "PiYG", "PiYG_r", "PuBu", "PuBuGn", "PuBuGn_r", "PuBu_r", "PuOr", "PuOr_r", "PuRd", "PuRd_r", "Purples", "Purples_r", "RdBu", "RdBu_r", "RdGy", "RdGy_r", "RdPu", "RdPu_r", "RdYlBu", "RdYlBu_r", "RdYlGn", "RdYlGn_r", "Reds", "Reds_r", "Set1", "Set1_r", "Set2", "Set2_r", "Set3", "Set3_r", "Spectral", "Spectral_r", "Wistia", "Wistia_r", "YlGn", "YlGnBu", "YlGnBu_r", "YlGn_r", "YlOrBr", "YlOrBr_r", "YlOrRd", "YlOrRd_r", "afmhot", "afmhot_r", "autumn", "autumn_r", "binary", "binary_r", "bone", "bone_r", "brg", "brg_r", "bwr", "bwr_r", "cool", "cool_r", "coolwarm", "coolwarm_r", "copper", "copper_r", "cubehelix", "cubehelix_r", "flag", "flag_r", "gist_earth", "gist_earth_r", "gist_gray", "gist_gray_r", "gist_heat", "gist_heat_r", "gist_ncar", "gist_ncar_r", "gist_rainbow", "gist_rainbow_r", "gist_stern", "gist_stern_r", "gist_yarg", "gist_yarg_r", "gnuplot", "gnuplot2", "gnuplot2_r", "gnuplot_r", "gray", "gray_r", "hot", "hot_r", "hsv", "hsv_r", "inferno", "inferno_r", "jet", "jet_r", "magma", "magma_r", "nipy_spectral", "nipy_spectral_r", "ocean", "ocean_r", "pink", "pink_r", "plasma", "plasma_r", "prism", "prism_r", "rainbow", "rainbow_r", "seismic", "seismic_r", "spectral", "spectral_r", "spring", "spring_r", "summer", "summer_r", "terrain", "terrain_r", "viridis", "viridis_r", "winter", "winter_r"]

schedule.every().day.at("23:50").do(job,'It is 23:50')

schedule.every().day.at("20:00").do(on)
schedule.every().day.at("7:30").do(off)

def random_show():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    print('yesterday was {}/{}/{}'.format(yesterday.day, yesterday.month, yesterday.year))
    cmap = random.choice(cmaps)
    print(cmap)
    sun(cmap, str(yesterday.day), str(yesterday.month), str(yesterday.year))


start = 20.0
for i in range(14):
    c = start + i * 0.25
    v = "{}:{:02d}".format(int(c), int((c-np.floor(c))*60.)+1)
    print(v)
    schedule.every().day.at(v).do(random_show)

if __name__ == "__main__":
    while True:
        print(time.ctime())
        schedule.run_pending()
        time.sleep(30) # wait one minute