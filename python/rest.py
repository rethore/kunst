from flask import Flask
from hue_show import *
from sunny import *
from threading import Thread
from time import sleep
import os
import json
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

# Initialise the light bridge
b = init_bridge()

# Load the sunny portal credential

with open(os.environ['HOME']+'/.sunny_cred', 'r') as f:
    cred = json.load(f)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/heartbeat')
def heartbeat():
    return "alive"

@app.route('/sun/<cmap>/<day>/<month>/<year>')
def sun(cmap, day, month, year):
    data = 'svalin_{}_{}_{}.csv'.format(day,month,year)
    #t = Thread(target=show, args=(data,))
    #t.start()
    print(data)
    show(data, cmap=cmap, b=b)
    return "done"

@app.route('/run/<speed>/<tours>')
def run(speed, tours):
    print(speed)
    on()
    run_game(float(speed), int(tours), b=b)
    return "done"

@app.route('/on')
def on():
    for i in range(4):
        for j in range(19):
            name = 'P%d'%(j+1)
            b.lights_by_name[name].on = True
            sleep(0.1)
        normal(b)
        time.sleep(0.5)
    return "done"

@app.route('/off')
def off():
    for i in range(4):
        for j in range(19):
            name = 'P%d'%(j+1)
            b.lights_by_name[name].on = False
            sleep(0.1)
        sleep(0.5)
    return "done"

@app.route('/effect/<effect_type>')
def effect(effect_type):
    for j in range(19):
        name = 'P%d'%(j+1)
        b.lights_by_name[name].effect = effect_type
        sleep(0.4)        
    return "done"


@app.route('/download/<day>/<month>/<year>')
def download(day, month, year):
    # if the file is already there, read the file
    file_name = 'svalin_%s_%s_%s.csv'%(day, month, year)
    date = "%s/%s/%s"%(day, month, year)
    print(file_name)
    if os.path.exists(file_name):
        # The file exists, so no need to download it again
        print('file exists')
        df = pd.read_csv(file_name)
        print('file loaded')
    else:
        # The file doesn-t exist, so we will download the info from Sunny portal
        s = Sunny(login = cred['login'], password = cred['password'])        
        df = s.download_all(int(day), int(month), int(year))
        s.close()
    
    # Now plotting
    import cufflinks as cf
    h = df.iplot(y=[k for k in df.keys() if 'House' in k], kind='line', layout={
            'yaxis': {'title': 'Power production [kW]'},
            'title': 'Power production of Svalin: %s'%(date)}, filename='svalin_%s_%s_%s'%(day, month, year))
    return h.resource        


if __name__ == '__main__':
    # Run the REST API: 
    #
    #    $ python3 rest.py
    
    app.run(debug=True, port=6001, host='0.0.0.0')
