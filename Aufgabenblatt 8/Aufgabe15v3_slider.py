#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import plotly.express as px
import pandas as pd
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output



app = dash.Dash(__name__)

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
df.replace('', 0, inplace=True)
df.replace(np.NaN, 0, inplace=True)

newestDate = df["date"].max()

app.layout = html.Div([
    html.H1('COVID-19 Datenset'),
    html.P ('unser eigenes dynamisches User Interface'),
    
    dcc.Dropdown(id='continent',
                options = [
                    {"label": "Nordamerika", "value": 'North America'},
                    {"label": "Südamerika", "value": 'South America'},
                    {"label": "Ozeanien", "value": 'Oceania'},
                    {"label": "Afrika", "value": 'Africa'},
                    {"label": "Europa", "value": 'Europe'},
                    {"label": "nicht zugeordnet", "value": 0},
                    {"label": "Asien", "value": 'Asia'}],
                multi = False,
                value = 'Europe',
                style = {"width": "40%"}),
    
    dcc.Slider(id='slider',
               min=df['date'].min(),
               max=df['date'].max(),
               value=df['date'].min(),
               marks={str(year): str(year) for year in df['date'].unique()},
               step=None
    ),
    
    
    
    html.Div(id='output_container', children=[]),
    html.Br(),   
    
    dcc.Graph(id='covidplot', figure = {}, style = {'display': 'inline-block'}),
    
    dcc.Graph(id='covidplot2', figure = {}, style = {'display': 'inline-block'}),
    
    dcc.Graph(id='covidplot3', figure = {}, style = {'display': 'inline-block'}),
    
    dcc.Graph(id='covidplot4', figure = {}, style = {'display': 'inline-block'}),
    
])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='covidplot', component_property='figure'),
     Output(component_id='covidplot2', component_property='figure'),
     Output(component_id='covidplot3', component_property='figure'),
     Output(component_id='covidplot4', component_property='figure')],
    [Input(component_id='continent', component_property='value'),
     Input(component_id='slider', component_property='value')],
)


def update_graph(option_slctd, selected_year):
    print(option_slctd)
    print(type(option_slctd))
    filtered_df = df[df.date == selected_year]
   

    dff = df.copy()
    dff = dff[dff["continent"] == option_slctd]
    
    dff2 = dff[dff["date"] > "2021-01-01"]
    
    dff3 = dff[dff["date"] == newestDate]
    


    
# Plotly Express
    
    fig = px.scatter(dff, x="new_cases", y="new_deaths", 
                     color = "location", size = "gdp_per_capita",
                     marginal_x = "box", marginal_y = "box", trendline = "lowess",
                     width = 800,
                     title = "Neue Fälle in Relation mit neuen Todesfällen")
    
    
    fig2 = px.bar(dff2, x = "date", y = "total_vaccinations", color = "location",
                  width = 600,
                  title = "Impfverlauf seit Beginn des Jahres 2021")
    

    fig3 = px.treemap(dff3, path = ['location', 'total_cases'],
                      values = 'total_cases',
                      width = 700,
                      title = "Summe aller Fälle nach Land zum aktuellen Zeitpunkt")
    
    fig4 = px.line(filtered_df, x = "date", y = "new_cases", color = 'location',
                   width = 700,
                   title = "Zeitverlauf der neuen Ansteckungsfälle")

    #fig.update_layout(transition_duration=500)
    
    
    container = "Ausgabe"

    return container, fig, fig2, fig3, fig4
    


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[8]:





# In[ ]:




