import time
import datetime
import schedule
from rest import download, on, off, sun
import random
import numpy as np

def download_PV_data():
    """Download today's PV data"""
    print('Downloading PV data')

    # Get today's date
    today = datetime.date.today()
    print('today is {}/{}/{}'.format(today.day, today.month, today.year))

    try:
        # Download the PV data
        download(str(today.day), str(today.month), str(today.year))
    except Exception as e:
        print('Download house failed: {}', str(e))
    return

# All the color maps
cmaps = ["Accent", "Accent_r", "Blues", "Blues_r", "BrBG", "BrBG_r", "BuGn",
         "BuGn_r", "BuPu", "BuPu_r", "CMRmap", "CMRmap_r", "Dark2", "Dark2_r",
         "GnBu", "GnBu_r", "Greens", "Greens_r", "Greys", "Greys_r", "OrRd",
         "OrRd_r", "Oranges", "Oranges_r", "PRGn", "PRGn_r", "Paired", "Paired_r",
         "Pastel1", "Pastel1_r", "Pastel2", "Pastel2_r", "PiYG", "PiYG_r", "PuBu",
         "PuBuGn", "PuBuGn_r", "PuBu_r", "PuOr", "PuOr_r", "PuRd", "PuRd_r",
         "Purples", "Purples_r", "RdBu", "RdBu_r", "RdGy", "RdGy_r", "RdPu",
         "RdPu_r", "RdYlBu", "RdYlBu_r", "RdYlGn", "RdYlGn_r", "Reds", "Reds_r",
         "Set1", "Set1_r", "Set2", "Set2_r", "Set3", "Set3_r", "Spectral",
         "Spectral_r", "Wistia", "Wistia_r", "YlGn", "YlGnBu", "YlGnBu_r",
         "YlGn_r", "YlOrBr", "YlOrBr_r", "YlOrRd", "YlOrRd_r", "afmhot",
         "afmhot_r", "autumn", "autumn_r", "binary", "binary_r", "bone",
         "bone_r", "brg", "brg_r", "bwr", "bwr_r", "cool", "cool_r", "coolwarm",
         "coolwarm_r", "copper", "copper_r", "cubehelix", "cubehelix_r", "flag",
         "flag_r", "gist_earth", "gist_earth_r", "gist_gray", "gist_gray_r",
         "gist_heat", "gist_heat_r", "gist_ncar", "gist_ncar_r", "gist_rainbow",
         "gist_rainbow_r", "gist_stern", "gist_stern_r", "gist_yarg", "gist_yarg_r",
         "gnuplot", "gnuplot2", "gnuplot2_r", "gnuplot_r", "gray", "gray_r",
         "hot", "hot_r", "hsv", "hsv_r", "inferno", "inferno_r", "jet", "jet_r",
         "magma", "magma_r", "nipy_spectral", "nipy_spectral_r", "ocean",
         "ocean_r", "pink", "pink_r", "plasma", "plasma_r", "prism", "prism_r",
         "rainbow", "rainbow_r", "seismic", "seismic_r", "spectral", "spectral_r",
         "spring", "spring_r", "summer", "summer_r", "terrain", "terrain_r",
         "viridis", "viridis_r", "winter", "winter_r"]

def random_show():
    """Start a light show with yesterday's PV data with a random colormap"""

    # Get yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    print('yesterday was {}/{}/{}'.format(yesterday.day,
                                          yesterday.month,
                                          yesterday.year))

    # Get a random colormap
    cmap = random.choice(cmaps)
    print('Selected colormap:', cmap)

    try:
        # Starting the show
        sun(cmap, str(yesterday.day), str(yesterday.month), str(yesterday.year))
    except Exception as e:
        print('Sunshow failed: {}', str(e))
    return

### Setting up all the schedules -----------------------------------------------

# Schedule to download the PV data
schedule.every().day.at("23:50").do(download_PV_data)

# Schedule light to switch on
schedule.every().day.at("20:00").do(on)

# Schedule light to switch off
schedule.every().day.at("7:30").do(off)

# Add all the shows
start = 20.0
for i in range(7):
    # Run every half an hour
    c = start + i * 0.5
    v = "{}:{:02d}".format(int(c), int((c-np.floor(c))*60.)+1)
    print('Scheduling show for:',v)
    schedule.every().day.at(v).do(random_show)


if __name__ == "__main__":
    while True:
        print(time.ctime())
        schedule.run_pending()
        time.sleep(30) # wait 30sec
