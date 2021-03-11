from flask import Blueprint, render_template
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
             'Died': response['Deaths']
             }

    URL = "https://covid19.th-stat.com/api/open/timeline"
    response = requests.get(URL).json()
    data = response['Data']
    date=[]
    confirm=[]

    for i in range(len(data)):
        data_date = data[i]
        date.append(data_date['Date'])
        confirm.append(data_date['Confirmed'])

    fig = go.Figure([
        go.Scatter(
            name='revenue',
            x=date,
            y=confirm,

            mode='lines',
            marker=dict(color='red', size=2),
            showlegend=True
        )
    ])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('covid19.html', covid=covid,plot=graphJSON, user=current_user)

@main.route('/news')
def news():
    return render_template('news.html', user=current_user)
    
@main.route('/date')
def covid_date():
    URL = "https://covid19.th-stat.com/api/open/timeline"
    response = requests.get(URL).json()
    data = response['Data']
    date = []
    confirm = []
    for i in range(len(data)):
        data_date = data[i]
        date.append(data_date['Date'])
        confirm.append(data_date['Confirmed'])
    mylist = zip(date, confirm)
    return render_template('covid_date.html', mylist=mylist, user=current_user)


# @main.route('/plot')
# def graph():
#     URL = "https://covid19.th-stat.com/api/open/timeline"
#     response = requests.get(URL).json()
#     data = response['Data']
#     date=[]
#     confirm=[]

#     for i in range(200,400):
#         data_date = data[i]
#         date.append(data_date['Date'])
#         confirm.append(data_date['Confirmed'])

#     fig = go.Figure([
#         go.Scatter(
#             name='revenue',
#             x=date,
#             y=confirm,

#             mode='lines',
#             marker=dict(color='red', size=2),
#             showlegend=True
#         )
#     ])

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return render_template('graph.html', plot=graphJSON, user=current_user)
