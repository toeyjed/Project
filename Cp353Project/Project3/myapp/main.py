from flask import Blueprint, render_template ,request
from flask_login import login_required, current_user
from urllib.request import urlopen
import json
import plotly
import plotly.graph_objs as go
import requests


main = Blueprint('main', __name__)


# COVID_URL_TODAY = "https://covid19.th-stat.com/api/open/today"
# COVID_KEY = '6CEyYMpMvv2H44U6uVfTzX6TKuOaUKnU'

@main.route('/')
def covid():
    URL = "https://covid19.th-stat.com/api/open/today"
    response = requests.get(URL).json()
    covid = ""
    covid = {'cases': response['Confirmed'],
             'Recovered': response['Recovered'],
             'Hospitalized': response['Hospitalized'],
             'Died': response['Deaths'],
             'UpdateDate': response['UpdateDate'],
             'NewConfirm':response['NewConfirmed']
             }

    return render_template('covid19.html', covid=covid, user=current_user)


@main.route('/news')
def news():
    URL = "http://api.mediastack.com/v1/news?access_key=995688a6b0fe66cf9ec90d61040e20d7&languages=en&keywords=-covid"
    response = requests.get(URL).json()
    data = response['data']
    title=[]
    description=[]
    image=[]
    url=[]

    for i in range(len(data)):
        myarticles = data[i]

        title.append(myarticles['title'])
        description.append(myarticles['description'])
        image.append(myarticles['image'])
        url.append(myarticles['url'])

    mylist = zip(title, description, url)


    return render_template('news.html', user=current_user, context = mylist)

@main.route('/world')
def world():
    url = "https://api.covid19api.com/summary"
    data = urlopen(url).read()
    parsed = json.loads(data)
    Global = None
    if parsed.get('Global'):

        confirm = parsed['Global']['TotalConfirmed']
        recover = parsed['Global']['TotalRecovered']
        die = parsed['Global']['TotalDeaths']
        
        Global = {'confirm': confirm,
                'recover': recover,
                'die' : die
                }

    return render_template('covidworld.html', Global=Global, user=current_user)

@main.route('/date')
@login_required
def covid_date():
    day = request.args.get('day')
    URL = "https://covid19.th-stat.com/api/open/timeline"
    response = requests.get(URL).json()
    data = response['Data']
    date = []
    newconfirm = []
    confirm = []
    recovered = []
    hospitalized = []
    newdeaths = []
    deaths = []
    if day:
        for i in range(len(data)):
            ck_data = data[i]
            if ck_data['Date'] == day:
                date.append(ck_data['Date'])
                newconfirm.append(ck_data['NewConfirmed'])
                confirm.append(ck_data['Confirmed'])
                recovered.append(ck_data['NewRecovered'])
                hospitalized.append(ck_data['Hospitalized'])
                newdeaths.append(ck_data['NewDeaths'])
                deaths.append(ck_data['Deaths'])
                mylist = zip(date, newconfirm,confirm, recovered, hospitalized, newdeaths,deaths)
            else:
                continue
    if not day:
        day = '01/01/2020'
        for i in range(len(data)):
            data_date = data[i]
            date.append(data_date['Date'])
            newconfirm.append(data_date['NewConfirmed'])
            confirm.append(data_date['Confirmed'])
            recovered.append(data_date['NewRecovered'])
            hospitalized.append(data_date['Hospitalized'])
            newdeaths.append(data_date['NewDeaths'])
            deaths.append(data_date['Deaths'])
            mylist = zip(date, newconfirm,confirm, recovered, hospitalized,newdeaths, deaths)
 
    return render_template('covid_date.html', mylist=mylist, user=current_user)


@main.route('/province_casesum')
def province():
    URLPR = "https://covid19.th-stat.com/api/open/cases/sum"
    datapr = requests.get(URLPR).json()
    datapr = datapr['Province']
    province = []
    num = []
    for key in datapr:
        province.append(key)
        num.append(datapr[key])
    myprovince = zip(province,num)
    return render_template('covid_province.html',myprovince=myprovince, user=current_user)

@main.route('/covid19')
def index():
    return render_template('index.html', user=current_user)


