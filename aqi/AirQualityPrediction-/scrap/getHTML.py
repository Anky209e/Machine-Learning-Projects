import requests
import os
import sys
import time

def get_HTML():
    years = list(range(2010,2019))
    months = ["%02d"%x for x in range(1, 13)]

    for year in years:
        for month in months:
            url='http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month ,year)

            
            r = requests.get(url)
            text_utf = r.text.encode('utf=8')


            if not os.path.exists("Data/Html_Data/{}".format(year)):
                os.makedirs("Data/Html_Data/{}".format(year))
            with open("Data/Html_Data/{}/{}.html".format(year,month),"wb") as output:
                output.write(text_utf)
    
    sys.stdout.flush()
    return

if __name__ == '__main__':
    
    sTime = time.time()
    get_HTML()
    sTime = time.time()
    
    print("Time taken {}".format(stop_time-start_time))