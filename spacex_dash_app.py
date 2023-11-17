import pandas as pd
import numpy as np
from dash import dcc 
from dash import html
import dash
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Record Dashboard', style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),
                                html.Div(dcc.Dropdown(id='site-dropdown', 
                                             options = [{'label' : 'All Sites', 'value' : 'ALL'},
                                                        {'label' : 'CCAFS LC-40', 'value' : 'CCAFS LC-40'},
                                                        {'label' : 'VAFB SLC-4E', 'value' : 'VAFB SLC-4E'},
                                                        {'label' : 'KSC LC-39A', 'value' : 'KSC LC-39A'},
                                                        {'label' : 'CCAFS SLC-40', 'value' : 'CCAFS SLC-40'}],
                                            value='ALL',
                                            placeholder='Choose Site',
                                            searchable=True),),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.Div(children = [html.P('Payload range (Kg):'), 
                                        dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                        marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                                        value=[min_payload, max_payload])]),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # data = spacex_df[spacex_df['class']==1]
        data = pd.DataFrame(spacex_df[spacex_df['class']==1]['Launch Site'].value_counts()).reset_index()
        fig = px.pie(data, values='count', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        data = pd.DataFrame(spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts()).reset_index()
        fig = px.pie(data, values='count', names='class', title=f'Total Success Launches for site {entered_site}')
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, entered_payload):
    if entered_site == 'ALL':
        data = spacex_df.loc[(spacex_df['Payload Mass (kg)']>=entered_payload[0]) & (spacex_df['Payload Mass (kg)']<=entered_payload[1])]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        data = spacex_df.loc[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>=entered_payload[0]) & (spacex_df['Payload Mass (kg)']<=entered_payload[1])]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Correlation between Payload and Success for {entered_site}')
        return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)