from flask import Flask
from hue_show import *
from sunny import *
from threading import Thread
from time import sleep
import os
import json
from flask_cors import CORS
from flask import g
from light_lib import env_or_else

app = Flask(__name__)
CORS(app)

mongo = MongoClient('mongo', 27017)
db_state = mongo.state_db
states = db_state.states

## Get environment variables

c02auth = env_or_else('C02_AUTH', None)
data_dir = env_or_else('DATA_DIR', '/data/')
sunny_login = env_or_else('SUNNY_LOGIN', None)
sunny_password = env_or_else('SUNNY_PASSWORD', None)
username = env_or_else('HUE_CRED', None)
ip = env_or_else('HUE_IP', None)

# Initialise the light bridge
b = init_bridge(ip, username)

# Load the sunny portal credential

if 'PLOTLY_CRED' not in os.environ:
    with open(os.environ['HOME']+'/.sunny_cred', 'r') as f:
        cred = json.load(f)
else:
    cred = os.environ['PLOTLY_CRED']

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/heartbeat')
def heartbeat():
    effect_type = get_effect_type()
    if effect_type == 'carbon':
        #Check if the time since last carbon check is longer than 3min
        carbon_time = get_carbon_state()['time']
        dt = datetime.now() - carbon_time
        if dt.total_seconds() > 120.0:
            carbon, carbon_scaled = carbon_color(c02auth, b)
        check_state(b)
    if effect_type == 'none':
        check_state(b)
    return "alive"

@app.route('/get_state')
def get_state():
    return json.dumps([{'name':post['name'], 'xy':post['xy']} for post in states.find() if 'xy' in post])

@app.route('/clean_state')
def clean_state_api():
    clean_state()
    return get_state()


@app.route('/sun/<cmap>/<day>/<month>/<year>')
def sun(cmap, day, month, year):
    set_effect_type('show')
    data = data_dir+'svalin_{}_{}_{}.csv'.format(day,month,year)
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
    set_effect_type('none')
    for i in range(4):
        for j in range(19):
            name = 'P%d'%(j+1)
            if name in b.lights_by_name:
                b.lights_by_name[name].on = True
            else:
                print('missing:', name)
            sleep(0.1)
        normal(b)
        time.sleep(0.5)
    return "done"

@app.route('/off')
def off():
    set_effect_type('off')
    for i in range(4):
        for j in range(19):
            name = 'P%d'%(j+1)
            b.lights_by_name[name].on = False
            sleep(0.1)
        sleep(0.5)
    return "done"

@app.route('/effect/<effect_type>')
def effect(effect_type):
    set_effect_type(effect_type)
    if effect_type == 'carbon':
        carbon, carbon_scaled = carbon_color(c02auth, b)
        return json.dumps({'status':"done", 'carbon':carbon, 'carbon_scaled':carbon_scaled})
    else:
        for j in range(19):
            name = 'P%d'%(j+1)
            b.lights_by_name[name].effect = effect_type
            sleep(0.4)
        normal(b)
    return json.dumps({'status':"done"})



@app.route('/download/<day>/<month>/<year>')
def download(day, month, year):
    # if the file is already there, read the file
    file_name = data_dir+'svalin_%s_%s_%s.csv'%(day, month, year)
    date = "%s/%s/%s"%(day, month, year)
    print(file_name)
    if os.path.exists(file_name):
        # The file exists, so no need to download it again
        print('file exists')
        df = pd.read_csv(file_name)
        print('file loaded')
    else:
        # The file doesn-t exist, so we will download the info from Sunny portal
        s = Sunny(login = sunny_login, password = sunny_password)
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
