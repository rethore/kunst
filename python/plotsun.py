
import pandas as pd
import click
# plotly
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *


def plot(csvfile):
    df = pd.read_csv(csvfile)
    date = csvfile.replace('.csv','').replace('svalin_','')
    # Now plotting
    import cufflinks as cf
    df.iplot(y=[k for k in df.keys() if 'House' in k], kind='line', layout={
        'yaxis': {'title': 'Power production [kW]'},
        'title': 'Power production of Svaline:%s'%(date)}, filename='svalin')
    #print(url)

@click.command()
@click.option('--data', help='CSV file of the house solar production')
def command(data):
    plot(data)
    
            
if __name__ == '__main__':
    command() 
