import time
from time import sleep
import pandas as pd
from io import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from seleniumrequests import Firefox

from pyvirtualdisplay import Display

from IPython.display import Image

# plotly
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

import os

current_dir = os.getcwd()

houses = {
    #1: 'Svalin_229',
    2: 'Svalin_227',
    3: 'Svalin_225',
    4: 'Toppen 223',
    #5: 'Svalin_221',
    6: 'Svalin_219',
    #7: 'Svalin_217',
    8: 'Svalin_215',
    9: 'Svalin_213',
    10: 'Svalin_211',
    11: 'Svalin_209',
    12: 'Svalin_207',
    13: 'Svalin_205',
    #14: 'Svalin_203',
    #15: 'Svalin_201',
    16: 'Svalin_199',
    #17: 'Svalin_197',
    #18: 'Svalin_195',
    #19: 'Svalin_193',
    20: 'Top-20',
}

id_hover = "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_OpenButtonsDivImg"
id_click = "ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_ImageButtonDownload"
id_day = 'ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_LinkButton_TabFront3'
id_info = 'ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_ImageButtonValuesSingle'
id_date = 'ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1__datePicker_textBox'
url_data_graph = 'https://www.sunnyportal.com/Templates/DownloadDiagram.aspx?down=diag'

TIME_DELAY = 20 # [sec]

class Sunny(object):
    def __init__(self, login, password):
        self.start_display()
        
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', current_dir)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/csv,application/vnd.ms-excel")
        #profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/plain")

        self.driver = Firefox(profile)
        self.login(login, password)
        self._login = login
        self._password = password
        
    def start_display(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

    def close(self):
        self.driver.close()
        self.display.stop()

    def login(self, login=None, password=None):
        """Login on the Sunny portal website using the credentials

        Parameters
        ----------

        login: str
            The login credential to sunnyportal

        password: str
            The password credential of sunnyportal
        """
        if not login:
            login = self._login
            password = self._password

        self.driver.get("https://www.sunnyportal.com/Templates/Start.aspx?ReturnUrl=%2f")
        self.driver.find_element_by_id("txtUserName").clear()
        self.driver.find_element_by_id("txtUserName").send_keys(login)
        self.driver.find_element_by_id("txtPassword").clear()
        self.driver.find_element_by_id("txtPassword").send_keys(password)
        self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_Logincontrol1_LoginBtn").click()
        #time.sleep(0.5)

    def wait_n_get(self, element_type, value):
        """ Wait for an element to be present and get it

        Paramters
        ---------
        element_type: By.ID | By.LINK_TEXT...
            The type of value to identify the element to get
        value: str
            the value describing the element to get

        Returns
        -------
        el: element
            The driver element requested
        """
        return WebDriverWait(self.driver, TIME_DELAY).until(EC.presence_of_element_located((element_type, value)))

    def goto(self, n_house):
        """Go to the page of an house given it's number, from the plant list page

        Parameters
        ----------

        n_house: int
            The number of the house to go to
        """
        el = self.wait_n_get(By.LINK_TEXT, houses[n_house])
        el.click()


    def goto_2(self, n_house):
        """Go to a house from the plant pannel on the Dashboard page

        Parameters
        ----------

        n_house: int
            The number of the house to go to

        """
        self.wait_n_get(By.CLASS_NAME, 'plantselect').click()
        self.wait_n_get(By.LINK_TEXT, houses[n_house]).click()


    def hover_over(self, id):
        """Hover over an element of the page given its id

        Parameter
        ---------

        id: str
            The id of the element to hover over
        """
        el = self.wait_n_get(By.ID, id)
        hover = ActionChains(self.driver).move_to_element(el)
        hover.perform()

    def click(self, id):
        """Click on an element of the page given its id

        Parameter
        ---------

        id: str
            The id of the element to click on
        """
        el = self.wait_n_get(By.ID, id)
        el.click()
        
    def select_date(self, day, month, year):
        id_date =    'ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1__datePicker_textBox'
        id_before =  'ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_btn_prev'
        id_after =   'ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_btn_next'
        try:
            el = self.wait_n_get(By.ID, id_date)
            self.driver.execute_script('$("#%s").val("%d/%d/%d")'%(id_date, month, day, year))
            sleep(0.2)
            self.click(id_before)
            sleep(0.2)
            self.click(id_after)
            sleep(0.2)
        except Exception as e:
            if "Element is not clickable at point" in str(e):
                print(e)
                print('trying again!')
                self.select_date(day, month, year)
                             
        

    def download(self, day=None, month=None, year=None):
        """Download the CSV file
        """
        # Make sure we see the "Day" pannel
        tabactive = self.wait_n_get(By.CLASS_NAME, 'tabactive')
        if not tabactive.text == 'Day':
            self.click(id_day)
            
        # Select the right day
        if day:
            self.select_date(day, month, year)

        # Hover over the download button
        try:
            self.hover_over(id_hover)
            self.click(id_click)
        except Exception as e_1:
            # Check if the data is available for that day by looking for the info bubble
            try:
                el = self.wait_n_get(By.ID, id_info)
                if 'info.png' in el.get_attribute('src'):
                    print('no data available for this day')
                    return None
                else:
                    # Not sure what just happen there
                    raise(e_1)
            except Exception as e_2:
                if 'Unable to locate element' in str(e_2):
                    # The info icon isn't available
                    print(e_2)
                    raise(e_1)
                else:
                    # Not sure what just happen there
                    print(e_1)
                    print(e_2)
                    #raise (e1, e2)

        # Download the data for the day
        res = self.driver.request('GET', url_data_graph)
        if res.status_code == 200:
            print('sucess')
        else:
            raise Exception('Error:', res.text)
        return res


    def download_house(self, n, day=None, month=None, year=None):
        """ Download the house power production of the day
        Parameters
        ----------
        driver: WebDriver
            The WebDriver instance to action

        n_house: int
            The number of the house to go to

        Return
        ------
        df: pandas.DataFrame | None
            A dataframe containing the house day power production, or None if there isn't any data available
        """

        try:
            # Check what is the starting point
            if 'Start.aspx' in self.driver.current_url:
                # We are on the login screen, we first need to login
                print('-- login in main screen')
                self.login()
                print('-- accessing house', n)
                self.goto(n)
            elif 'sunnyportal.com/Plants' in self.driver.current_url:
                # We are on the plant list, lets
                self.goto(n)
            elif 'sunnyportal.com/FixedPages/Dashboard.aspx' in self.driver.current_url:
                # We are on a dashboard, so we should be able to click on the left hand pannel to go to the new house
                self.goto_2(n)
            else:
                # No idea where we are
                raise Exception('I dont know where we are:', self.driver.current_url)
            print('-- downloading house', n, 'power data')
            res = self.download(day, month, year)
            self.date = self.wait_n_get(By.ID, id_date).get_attribute('value')
            if day:
                if not self.date == "%d/%d/%d"%(month, day, year):
                    print('Error the date wasnt fixed correctly: '+self.date)

            if res:
                # There seems to be a positive response, so let's put it in a pandas dataframe
                df = pd.read_csv(StringIO(res.text), sep=';', names=['power', 'avg'], skiprows=1)
                print('-- download sucessful')
                return df
            else:
                print('-- download failed')
                # No response, we return a None object
                return res

        except Exception as e_1:
            # Something whent wrong
            try:
                # Check if sunny portal has banned us for some time
                text = self.wait_n_get(By.ID, 'ctl00_ContentPlaceHolder1_Logincontrol1_DivLogin').text
                if 'Login failed! Login will be blocked for' in text:
                    # It does seem like we have been banned for some time
                    print(text)
                    n_sec = int(text.split('for')[1].split(' seconds')[0])
                    print('going to sleep for %d sec'%(n_sec))
                    time.sleep(n_sec)
                    print('retrying this house')
                    return self.download_house(n, day, month, year)
            except Exception as e_2:
                # I don't know what went wrong
                print(e_1)
                print(e_2)
                raise(e_1)

    def img(self):
        """A simple screenshot function to show on the notebook"""
        return Image(self.driver.get_screenshot_as_png())
    
    def download_all(self, day=None, month=None, year=None):
        df_dict = {}
        for k, v in houses.items():
            print(k)
            df = self.download_house(k, day, month, year)
            if isinstance(df, pd.DataFrame):
                df_dict['House %d'%(k)] = df
        # Save the data into a DataFrame
        self.data = pd.DataFrame({k:v.power for k, v in df_dict.items() if isinstance(v, pd.DataFrame)}, index=df.index)
        
        # Save the data into a file
        m,d,y = self.date.split('/')
        self.data.to_csv('svalin_%s_%s_%s.csv'%(d,m,y))
        return self.data

#time.sleep(5)
#self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_UserControlShowDashboard1_UserControlShowEnergyAndPower1_ImageButtonDownload")


if __name__ == '__main__':
    cdir = os.path.dirname(os.path.realpath(__file__))
    with open(cdir+'/.sunny_cred', 'r') as f:
        cred = json.load(f)
        
    s = Sunny(login = cred['login'], password = cred['password'])
    
    df = s.download_all()
    s.close()
    
    # Now plotting
    import cufflinks as cf
    df.iplot(y=[k for k in df.keys() if 'House' in k], kind='line', layout={
        'yaxis': {'title': 'Power production [kW]'},
        'title': 'Power production of Svalin %s'%(s.date)}, filename='svalin/%s'%(s.date.replace('/','_')))
    #print(url)
