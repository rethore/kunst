import time
import datetime
import schedule
from rest import download, on, off

def job(t):
    print("I'm working...", t)
    today = datetime.date.today()
    print('today is {}/{}/{}'.format(today.day, today.month, today.year))
    download(str(today.day), str(today.month), str(today.year))
    return



schedule.every().day.at("23:50").do(job,'It is 23:50')

schedule.every().day.at("20:00").do(on)
schedule.every().day.at("7:30").do(off)

while True:
    print(time.ctime())
    schedule.run_pending()
    time.sleep(30) # wait one minute