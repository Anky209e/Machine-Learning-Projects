from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import sys

years = list(range(2010,2019))
months = ["%02d"%x for x in range(1, 13)]

for year in years:
    for month in months:
        file_html = open('Data/Html_Data/{}/{}.html'.format(year,month), 'rb')
        plain_text = file_html.read()

        soup = BeautifulSoup(plain_text, 'lxml')

        table = soup.find('table', class_ = 'medias mensuales numspan')
        tbody = table.find_all('tr')
        tcols = [table.find('tr').find_all('th')[i].text for i in range(15)]

        days_in_month = len(tbody) - 3                                       

        tdata_of_month = [[table.find_all('tr')[day].find_all('td')[i].text for i in range (15)] for day in range(1, days_in_month + 1)]

        df_month = pd.DataFrame(tdata_of_month, columns = tcols)

        df_month.drop(columns = ['VG', 'RA', 'SN', 'TS', 'FG'], inplace = True)
        df_month.replace('', np.nan, inplace = True)
        df_month.dropna(subset = tcols[1 : 9], inplace = True)
        
        if not os.path.exists("Data/Scrapped_Data/{}".format(year)):
            os.makedirs("Data/Scrapped_Data/{}".format(year))
        df_month.to_csv("Data/Scrapped_Data/{}/{}.csv".format(year, month), index = False)

        sys.stdout.flush()
