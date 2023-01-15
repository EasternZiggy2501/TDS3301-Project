from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import time
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.point import Point

df = pd.read_csv('completed.csv')


'''geolocator = Nominatim(user_agent="test")
city = []

for i in range(df.shape[0]):
    location = geolocator.reverse(
        Point(df.loc[i]['latitude'], df.loc[i]['longitude']))

    if 'Petaling' in location.raw['display_name']:
        if 'Kuala Lumpur' in location.raw['display_name']:
            city.append('Kuala Lumpur')
        elif 'Petaling' in location.raw['display_name'] and 'Petaling Jaya' in location.raw['display_name']:
            city.append('Petaling Jaya')
        else:
            city.append('Petaling')

    elif 'Shah Alam' in location.raw['display_name']:
        if('Kuala Lumpur' in location.raw['display_name']):
            city.append('Kuala Lumpur')
        else:
            city.append('Shah Alam')

    elif 'Ampang' in location.raw['display_name']:
        if('Kuala Lumpur' in location.raw['display_name']):
            city.append('Kuala Lumpur')
        else:
            city.append('Ampang')

    elif 'Cyberjaya' in location.raw['display_name']:
        city.append('Cyberjaya')

    elif 'Putrajaya' in location.raw['display_name']:
        city.append('Putrajaya')

    else:
        city.append('Kuala Lumpur')

# make a new column for city
city = pd.DataFrame(city, columns=['City'])
complete = pd.concat([df, city], axis=1)
complete.to_csv('completed.csv', index=False)'''

#location = geolocator.reverse(Point(df['latitude'], df['longitude']))
# print(location.raw['display_name'])


'''url = 'https://www.timeanddate.com/holidays/malaysia/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'}

holiday = []

for i in range(df.shape[0]):
    oridate = df.loc[i]['Date'].split('-')
    day = oridate[2]
    month = oridate[1]
    year = oridate[0]

    # change the month number to the month name e.g: 01 to Jan
    month = datetime.strptime(month, '%m').strftime('%b')

    dayMonth = day + ' ' + month

    # print(dayMonth)

    pageno = 1

    link = url + year
    # print(link)
    page = requests.get(link, headers=headers)
    soupDayMonth = BeautifulSoup(page.text, 'html.parser')

    # for table in soupDayMonth.find_all('th'):
    #    print(table.get('class'))

    table = soupDayMonth.find_all('th', class_='nw')

    # strip the <th> tag
    table = [x.text for x in table]
    # find table that contains the same value as dayMonth
    if dayMonth in table:
        if dayMonth == '1 Jan':
            holiday.append('New Year')

        elif dayMonth == '3 Jan':
            holiday.append('Prophet Muhammad Birthday')

        elif dayMonth == '1 Feb' or dayMonth == '2 Feb':
            holiday.append('Federal Territory Day')

        elif dayMonth == '3 Feb' or (dayMonth == '4 Feb' and year == '2016'):
            holiday.append('Thaipusam')

        elif (dayMonth == '19 Feb' or dayMonth == '20 Feb') or (dayMonth == '8 Feb' and year == '2016') or (dayMonth == '9 Feb' and year == '2016'):
            holiday.append('Chinese New Year')

        elif dayMonth == '1 May':
            holiday.append('Labour Day')

        elif dayMonth == '3 May' or (dayMonth == '21 May' and year == '2016'):
            holiday.append('Wesak Day')

        elif dayMonth == '16 May':
            holiday.append('Israk Mikraj')

        elif dayMonth == '6 Jun' or (dayMonth == '4 Jun' and year == '2016'):
            holiday.append('Agong\' Birthday')

        elif dayMonth == '18 Jun' or (dayMonth == '7 Jun' and year == '2016'):
            holiday.append('Beginning of Ramadan')

        elif dayMonth == '4 Jul':
            holiday.append('Nuzul Quran')

        elif dayMonth == '17 Jul' or dayMonth == '18 Jul' or (dayMonth == '6 Jul' and year == '2016') or (dayMonth == '7 Jul' and year == '2016') or (dayMonth == '8 Jul' and year == '2016'):
            holiday.append('Eidul Fitr')

        elif dayMonth == '31 Aug':
            holiday.append('Malaysia Independence Day')

        elif dayMonth == '16 Sep':
            holiday.append('Malaysia Day')

        elif dayMonth == '24 Sep' or dayMonth == '25 Sep' or (dayMonth == '12 Sep' and year == '2016') or (dayMonth == '13 Sep' and year == '2016'):
            holiday.append('Eidul Adha')

        elif dayMonth == '14 Oct' or (dayMonth == '2 Oct' and year == '2016'):
            holiday.append('Awal Muharram')

        elif dayMonth == '10 Nov' or (dayMonth == '29 Oct' and year == '2016'):
            holiday.append('Deepavali')

        elif dayMonth == '11 Dec':
            holiday.append('Sultan Selangor Birthday')

        elif dayMonth == '24 Dec':
            holiday.append('Christmas Eve')

        elif dayMonth == '25 Dec':
            holiday.append('Christmas')

        elif dayMonth == '31 Dec':
            holiday.append('New Year Eve')

        else:
            holiday.append('Normal Day')
    else:
        holiday.append('Normal Day')

holiday = pd.DataFrame(holiday, columns=['Occasion'])
complete = pd.concat([df, holiday], axis=1)
complete.to_csv('completed2.csv', index=False)'''

# soupDayMonth = soupDayMonth.find('th', class_='nw')
# soupDayMonth = soupDayMonth.text
# print(soupDayMonth)

# holiday.append(soupDayMonth)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'}

cityDict = {'Kuala Lumpur': 'kuala-lumpur', 'Cyberjaya': '@6930887', 'Putrajaya': '@1996552',
            'Petaling Jaya': '@1735158', 'Petaling': '@1735156', 'Shah Alam': 'shah-alam', 'Ampang': '@1735168'}

url = 'https://www.timeanddate.com/weather/'


weather = []
temperature = []
humidity = []
link = ''

for x in range(df.shape[0]):
    oridate = df.loc[x]['Date'].split('-')
    oritime = df.loc[x]['Time'].split(':')
    # print(oritime[0])
    month = oridate[1]
    year = oridate[0]

    date = oridate[0] + oridate[1] + oridate[2]

    location = df.loc[x]['City']

    pageno = 1

    url1 = url
    url2 = 'malaysia/'
    url3 = cityDict.get(location)
    url4 = '/historic?month='
    url5 = '&year='
    url6 = '&hd='
    if cityDict.get(location) == 'kuala-lumpur' or cityDict.get(location) == 'shah-alam':
        link = url1 + url2 + url3 + url4 + month + url5 + year + url6 + date
    else:
        link = url1 + url3 + url4 + month + url5 + year + url6 + date
    # print(link)
    page = requests.get(link, headers=headers)
    soupWeather = BeautifulSoup(page.content, 'html.parser')
    soupTemperature = BeautifulSoup(page.content, 'html.parser')
    soupHumidity = BeautifulSoup(page.content, 'html.parser')

    # print(soupTime)

    soupWeather = soupWeather.find('td', class_='small')
    soupTemperature = soupTemperature.find('tr', class_='sep-t')
    soupHumidity = soupHumidity.find('tr', class_='sep-t')

    # get the first <td>
    soupTemperature = soupTemperature.find('td')
    # get the second <td>
    soupHumidity = soupHumidity.find_next('td', class_='sep')


# from '<td class="small">Dense fog.</td>' take only the 'dense fog'
    soupWeather = soupWeather.text.split('.')[0]
    soupTemperature = soupTemperature.text.split('°')[0]
    soupHumidity = soupHumidity.text.split('%')[0]

    soupTemperature = int(soupTemperature)
    soupHumidity = int(soupHumidity)

    # print(soupWeather)
    # print(soupTemperature)
    # print(soupHumidity)

    # append to weather list
    weather.append(soupWeather)
    temperature.append(soupTemperature)
    humidity.append(soupHumidity)

# convert it into a dataframe
weather = pd.DataFrame(weather, columns=['Weather'])
humidity = pd.DataFrame(humidity, columns=['Humidity'])
temperature = pd.DataFrame(temperature, columns=['Temperature'])

# merge the weather dataframe with the original dataframe
complete = pd.concat([df, weather, temperature, humidity], axis=1)


# save it to a csv file
complete.to_csv('completed.csv', index=False)
